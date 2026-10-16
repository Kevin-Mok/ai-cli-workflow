"""Bounded Markdown link parsing for the AI workflow audit."""

from __future__ import annotations

import re
import string
from bisect import bisect_right


INLINE_LINK_START_RE = re.compile(r"!?\[[^\]\n]*\]\(")
REFERENCE_LINK_RE = re.compile(r"^\s*\[[^\]]+\]:\s*(.+?)\s*$")


def unfenced_lines(text: str) -> list[tuple[int, str]]:
    output: list[tuple[int, str]] = []
    fence: tuple[str, int] | None = None
    for line_number, line in enumerate(text.splitlines(), start=1):
        indentation = len(line) - len(line.lstrip(" "))
        stripped = line[indentation:] if indentation <= 3 else line
        marker_character = stripped[:1] if indentation <= 3 else ""
        marker_length = (
            len(stripped) - len(stripped.lstrip(marker_character))
            if marker_character in (chr(96), "~")
            else 0
        )
        if fence is not None:
            trailing = stripped[marker_length:]
            if (
                marker_character == fence[0]
                and marker_length >= fence[1]
                and not trailing.strip(" \t")
            ):
                fence = None
            continue
        if (
            marker_length >= 3
            and indentation <= 3
            and not (marker_character == "`" and "`" in stripped[marker_length:])
        ):
            fence = (marker_character, marker_length)
            continue
        output.append((line_number, line))
    return output


def unescape_destination_character(
    value: str, cursor: int
) -> tuple[str, int] | None:
    if (
        value[cursor] == "\\"
        and cursor + 1 < len(value)
        and value[cursor + 1] in string.punctuation
    ):
        return value[cursor + 1], cursor + 2
    return None


def inline_links(line: str) -> list[tuple[int, int, int, str]]:
    """Return label start, destination start/end, and the unescaped target."""
    targets: list[tuple[int, int, int, str]] = []
    for match in INLINE_LINK_START_RE.finditer(line):
        cursor = match.end()
        if cursor < len(line) and line[cursor] == "<":
            cursor += 1
            buffer: list[str] = []
            while cursor < len(line):
                escaped = unescape_destination_character(line, cursor)
                if escaped:
                    character, cursor = escaped
                    buffer.append(character)
                    continue
                if line[cursor] == ">":
                    targets.append(
                        (match.start(), match.end(), cursor + 1, "".join(buffer))
                    )
                    break
                buffer.append(line[cursor])
                cursor += 1
            continue

        buffer = []
        parenthesis_depth = 0
        while cursor < len(line):
            escaped = unescape_destination_character(line, cursor)
            if escaped:
                character, cursor = escaped
                buffer.append(character)
                continue
            character = line[cursor]
            if character == "(":
                parenthesis_depth += 1
            elif character == ")":
                if parenthesis_depth == 0:
                    targets.append(
                        (match.start(), match.end(), cursor, "".join(buffer).strip())
                    )
                    break
                parenthesis_depth -= 1
            elif character.isspace() and parenthesis_depth == 0:
                targets.append(
                    (match.start(), match.end(), cursor, "".join(buffer).strip())
                )
                break
            buffer.append(character)
            cursor += 1
    return targets


def reference_link_target(value: str) -> str:
    value = value.strip()
    if value.startswith("<"):
        buffer: list[str] = []
        cursor = 1
        while cursor < len(value):
            escaped = unescape_destination_character(value, cursor)
            if escaped:
                character, cursor = escaped
                buffer.append(character)
                continue
            if value[cursor] == ">":
                return "".join(buffer)
            buffer.append(value[cursor])
            cursor += 1
        return ""

    buffer = []
    cursor = 0
    while cursor < len(value) and not value[cursor].isspace():
        escaped = unescape_destination_character(value, cursor)
        if escaped:
            character, cursor = escaped
            buffer.append(character)
            continue
        buffer.append(value[cursor])
        cursor += 1
    return "".join(buffer)


def inline_link_end(text: str, destination_end: int) -> int:
    """Extend a destination's literal context through a complete link title."""
    cursor = destination_end
    while cursor < len(text) and text[cursor].isspace():
        cursor += 1
    if cursor < len(text) and text[cursor] == ")":
        return cursor + 1
    if cursor == destination_end or cursor == len(text):
        return destination_end
    delimiter = text[cursor]
    closer = {"\"": "\"", "'": "'", "(": ")"}.get(delimiter)
    if closer is None:
        return destination_end
    cursor += 1
    while cursor < len(text):
        escaped = unescape_destination_character(text, cursor)
        if escaped:
            _, cursor = escaped
            continue
        if text[cursor] == closer:
            cursor += 1
            while cursor < len(text) and text[cursor].isspace():
                cursor += 1
            if cursor < len(text) and text[cursor] == ")":
                return cursor + 1
            return destination_end
        if delimiter == "(" and text[cursor] == "(":
            return destination_end
        cursor += 1
    return destination_end


def mask_inline_code(text: str) -> str:
    """Mask complete equal-run spans without changing offsets or line breaks.

    Unmatched runs stay literal. Escapes apply to openers, while backslashes
    inside a span do not escape its closer. Link destinations and titles are
    literal too; their backticks must not open spans that hide later links.
    """
    destinations: dict[int, tuple[int, int]] = {}
    offset = 0
    for line in text.split("\n"):
        for label, start, end, _ in inline_links(line):
            destinations[offset + start] = (
                inline_link_end(text, offset + end), offset + label
            )
        definition = REFERENCE_LINK_RE.match(line)
        if definition:
            label = len(line) - len(line.lstrip())
            destinations[offset + definition.start(1)] = (
                offset + len(line), offset + label
            )
        offset += len(line) + 1

    runs = list(re.finditer(r"`+", text))
    by_length: dict[int, list[int]] = {}
    for index, run in enumerate(runs):
        by_length.setdefault(run.end() - run.start(), []).append(index)
    destination_starts = sorted(destinations)
    masked = list(text)
    index = 0
    while index < len(runs):
        run = runs[index]
        start = run.start()
        destination_index = bisect_right(destination_starts, start) - 1
        if destination_index >= 0:
            end, label = destinations[destination_starts[destination_index]]
            if start < end and masked[label] != " ":
                index += 1
                continue
        slash_start = start
        while slash_start > 0 and text[slash_start - 1] == "\\":
            slash_start -= 1
        start += (start - slash_start) % 2
        candidates = by_length.get(run.end() - start, [])
        next_index = bisect_right(candidates, index)
        if next_index == len(candidates):
            index += 1
            continue
        closer = candidates[next_index]
        for position in range(start, runs[closer].end()):
            if text[position] != "\n":
                masked[position] = " "
        index = closer + 1
    return "".join(masked)


def link_targets(text: str) -> list[tuple[int, str]]:
    targets: list[tuple[int, str]] = []
    block: list[tuple[int, str]] = []
    previous_quote_depth = 0

    def collect_block() -> None:
        if not block:
            return
        masked = mask_inline_code("\n".join(line for _, line in block))
        for (line_number, line), visible in zip(block, masked.split("\n")):
            for start, destination, _, target in inline_links(line):
                if visible[start] != " " and visible[start:destination].endswith("]("):
                    targets.append((line_number, target))
            definition = REFERENCE_LINK_RE.match(line)
            if definition and visible.lstrip().startswith("["):
                targets.append(
                    (line_number, reference_link_target(definition.group(1)))
                )
        block.clear()

    for line_number, line in unfenced_lines(text):
        quoted = re.match(r"^ {0,3}(?:>[ \t]*)*", line)
        prefix = quoted.group() if quoted else ""
        quote_depth = prefix.count(">")
        content = line[len(prefix) :]
        heading = bool(re.match(r"^ {0,3}#{1,6}(?:[ \t]|$)", content))
        list_item = bool(
            re.match(r"^ {0,3}(?:[-+*]|\d{1,9}[.)])[ \t]+", content)
        )
        separator = bool(
            re.fullmatch(r" {0,3}(?:=+|-+)[ \t]*", content)
            or re.fullmatch(
                r" {0,3}(?:(?:\*[ \t]*){3,}|(?:_[ \t]*){3,}|(?:-[ \t]*){3,})",
                content,
            )
        )
        if (
            not content.strip()
            or heading
            or list_item
            or separator
            or quote_depth != previous_quote_depth
            or (block and line_number != block[-1][0] + 1)
        ):
            collect_block()
        if content.strip() and not separator:
            block.append((line_number, line))
        if heading:
            collect_block()
        previous_quote_depth = quote_depth
    collect_block()
    return targets
