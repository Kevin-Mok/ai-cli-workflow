# shadcn patterns and workflows

Use this reference when choosing components, adding or updating them, or changing
presets. Read project context first, follow the matching workflow, then inspect
the resulting files and preserve local changes.

## Key Patterns

These are the most common patterns that differentiate correct shadcn/ui code. For edge cases, see the linked rule files above.

```tsx
// Form layout: FieldGroup + Field, not div + Label.
<FieldGroup>
  <Field>
    <FieldLabel htmlFor="email">Email</FieldLabel>
    <Input id="email" />
  </Field>
</FieldGroup>

// Validation: data-invalid on Field, aria-invalid on the control.
<Field data-invalid>
  <FieldLabel>Email</FieldLabel>
  <Input aria-invalid />
  <FieldDescription>Invalid email.</FieldDescription>
</Field>

// Icons in buttons: data-icon, no sizing classes.
<Button>
  <SearchIcon data-icon="inline-start" />
  Search
</Button>

// Spacing: gap-*, not space-y-*.
<div className="flex flex-col gap-4">  // correct
<div className="space-y-4">           // wrong

// Equal dimensions: size-*, not w-* h-*.
<Avatar className="size-10">   // correct
<Avatar className="w-10 h-10"> // wrong

// Status colors: Badge variants or semantic tokens, not raw colors.
<Badge variant="secondary">+20.1%</Badge>    // correct
<span className="text-emerald-600">+20.1%</span> // wrong
```

## Component Selection

| Need                       | Use                                                                                                 |
| -------------------------- | --------------------------------------------------------------------------------------------------- |
| Button/action              | `Button` with appropriate variant                                                                   |
| Form inputs                | `Input`, `Select`, `Combobox`, `Switch`, `Checkbox`, `RadioGroup`, `Textarea`, `InputOTP`, `Slider` |
| Toggle between 2–5 options | `ToggleGroup` + `ToggleGroupItem`                                                                   |
| Data display               | `Table`, `Card`, `Badge`, `Avatar`                                                                  |
| Navigation                 | `Sidebar`, `NavigationMenu`, `Breadcrumb`, `Tabs`, `Pagination`                                     |
| Overlays                   | `Dialog` (modal), `Sheet` (side panel), `Drawer` (bottom sheet), `AlertDialog` (confirmation)       |
| Feedback                   | `toast` (Base UI), `sonner` (Radix/Aria), `Alert`, `Progress`, `Skeleton`, `Spinner`                 |
| Command palette            | `Command` inside `Dialog`                                                                           |
| Charts                     | `Chart` (wraps Recharts)                                                                            |
| Layout                     | `Card`, `Separator`, `Resizable`, `ScrollArea`, `Accordion`, `Collapsible`                          |
| Empty states               | `Empty`                                                                                             |
| Menus                      | `DropdownMenu`, `ContextMenu`, `Menubar`                                                            |
| Tooltips/info              | `Tooltip`, `HoverCard`, `Popover`                                                                   |
| Chat / conversation UI     | `MessageScroller`, `Message`, `Bubble`, `Attachment`, `Marker`, `Trace`                             |

## Key Fields

The `info --json` project context contains these key fields:

- **`aliases`** → use the actual alias prefix for imports (e.g. `@/`, `~/`), never hardcode.
- **`isRSC`** → when `true`, components using `useState`, `useEffect`, event handlers, or browser APIs need `"use client"` at the top of the file. Always reference this field when advising on the directive.
- **`tailwindVersion`** → `"v4"` uses `@theme inline` blocks; `"v3"` uses `tailwind.config.js`.
- **`tailwindCssFile`** → the global CSS file where custom CSS variables are defined. Always edit this file, never create a new one.
- **`style`** → component visual treatment (e.g. `nova`, `vega`).
- **`base`** → primitive library (`radix` or `base`). Affects component APIs and available props.
- **`iconLibrary`** → determines icon imports. Use `lucide-react` for `lucide`, `@tabler/icons-react` for `tabler`, etc. Never assume `lucide-react`.
- **`resolvedPaths`** → exact file-system destinations for components, utils, hooks, etc.
- **`framework`** → routing and file conventions (e.g. Next.js App Router vs Vite SPA).
- **`packageManager`** → use this for any non-shadcn dependency installs (e.g. `pnpm add date-fns` vs `npm install date-fns`).
- **`preset`** → resolved preset code and values for the current project. Use `npx shadcn@4.21.5 preset resolve --json` when you only need preset information.

See [cli.md — `info` command](./cli.md) for the full field reference.

## Component Docs, Examples, and Usage

Run `npx shadcn@4.21.5 docs <component>` to get the URLs for a component's documentation, examples, and API reference. Fetch these URLs to get the actual content.

```bash
npx shadcn@4.21.5 docs button dialog select
```

**When creating, fixing, debugging, or using a component, always run `npx shadcn@4.21.5 docs` and fetch the URLs first.** This ensures you're working with the correct API and usage patterns rather than guessing.

## Workflow

1. **Get project context** — run the explicit `info --json` step above. Run `npx shadcn@4.21.5 info` again if you need to refresh.
2. **Check installed components first** — before running `add`, always check the `components` list from project context or list the `resolvedPaths.ui` directory. Don't import components that haven't been added, and don't re-add ones already installed.
3. **Find components** — `npx shadcn@4.21.5 search`.
4. **Get docs and examples** — run `npx shadcn@4.21.5 docs <component>` to get URLs, then fetch them. Use `npx shadcn@4.21.5 view` to browse registry items you haven't installed. To preview changes to installed components, use `npx shadcn@4.21.5 add --diff`.
5. **Install or update** — `npx shadcn@4.21.5 add`. When updating existing components, use `--dry-run` and `--diff` to preview changes first (see [Updating Components](#updating-components) below).
6. **Fix imports in third-party components** — After adding components from community registries (e.g. `@bundui`, `@magicui`), check the added non-UI files for hardcoded import paths like `@/components/ui/...`. These won't match the project's actual aliases. Use `npx shadcn@4.21.5 info` to get the correct `ui` alias (e.g. `@workspace/ui/components`) and rewrite the imports accordingly. The CLI rewrites imports for its own UI files, but third-party registry components may use default paths that don't match the project.
7. **Review added components** — After adding a component or block from any registry, **always read the added files and verify they are correct**. Check for missing sub-components (e.g. `SelectItem` without `SelectGroup`), missing imports, incorrect composition, or violations of the [Critical Rules](SKILL.md#critical-rules). Also replace any icon imports with the project's `iconLibrary` from the project context (e.g. if the registry item uses `lucide-react` but the project uses `hugeicons`, swap the imports and icon names accordingly). Fix all issues before moving on.
8. **Registry must be explicit** — When the user asks to add a block or component, **do not guess the registry**. If no registry is specified (e.g. user says "add a login block" without specifying `@shadcn`, `@tailark`, `owner/repo`, etc.), ask which registry to use. Never default to a registry on behalf of the user.
9. **Switching presets** — Ask the user first: **overwrite**, **partial**, **merge**, or **skip**?
   - **Inspect current preset**: `npx shadcn@4.21.5 preset resolve`. Use `--json` when you need structured values.
   - **Inspect incoming preset**: `npx shadcn@4.21.5 preset decode <code>`. Use `preset url <code>` or `preset open <code>` to share or open the preset builder.
   - **Overwrite**: `npx shadcn@4.21.5 apply <code>`. Overwrites detected components, fonts, and CSS variables.
   - **Partial**: `npx shadcn@4.21.5 apply <code> --only theme,font`. Updates only the selected preset parts without reinstalling UI components. Supported values are `theme` and `font`; comma-separated combinations are allowed. `icon` is intentionally not supported, because icon changes may require full component reinstall and transforms.
   - **Merge**: `npx shadcn@4.21.5 init --preset <code> --force --no-reinstall`, then run `npx shadcn@4.21.5 info` to list installed components, then for each installed component use `--dry-run` and `--diff` to [smart merge](#updating-components) it individually.
   - **Skip**: `npx shadcn@4.21.5 init --preset <code> --force --no-reinstall`. Only updates config and CSS, leaves components as-is.
   - **Important**: Always run preset commands inside the user's project directory. `apply` only works in an existing project with a `components.json` file. The CLI automatically preserves the current base (`base` vs `radix`) from `components.json`. If you must use a scratch/temp directory (e.g. for `--dry-run` comparisons), pass `--base <current-base>` explicitly — preset codes do not encode the base.

## Updating Components

When the user asks to update a component from upstream while keeping their local changes, use `--dry-run` and `--diff` to intelligently merge. **NEVER fetch raw files from GitHub manually — always use the CLI.**

1. Run `npx shadcn@4.21.5 add <component> --dry-run` to see all files that would be affected.
2. For each file, run `npx shadcn@4.21.5 add <component> --diff <file>` to see what changed upstream vs local.
3. Decide per file based on the diff:
   - No local changes → safe to overwrite.
   - Has local changes → read the local file, analyze the diff, and apply upstream updates while preserving local modifications.
   - User says "just update everything" → use `--overwrite`, but confirm first.
4. **Never use `--overwrite` without the user's explicit approval.**

## Quick Reference

```bash
# Create a new project.
npx shadcn@4.21.5 init --name my-app --preset base-nova
npx shadcn@4.21.5 init --name my-app --preset a2r6bw --template vite

# Create a monorepo project.
npx shadcn@4.21.5 init --name my-app --preset base-nova --monorepo
npx shadcn@4.21.5 init --name my-app --preset base-nova --template next --monorepo

# Initialize existing project.
npx shadcn@4.21.5 init --preset base-nova
npx shadcn@4.21.5 init --defaults  # shortcut: --template=next --preset=nova (base style implied)

# Apply a preset to an existing project.
npx shadcn@4.21.5 apply a2r6bw
npx shadcn@4.21.5 apply a2r6bw --only theme
npx shadcn@4.21.5 apply a2r6bw --only font
npx shadcn@4.21.5 apply a2r6bw --only theme,font

# Inspect preset codes and project preset state.
npx shadcn@4.21.5 preset decode a2r6bw
npx shadcn@4.21.5 preset url a2r6bw
npx shadcn@4.21.5 preset open a2r6bw
npx shadcn@4.21.5 preset resolve
npx shadcn@4.21.5 preset resolve --json

# Add components.
npx shadcn@4.21.5 add button card dialog
npx shadcn@4.21.5 add @magicui/shimmer-button
npx shadcn@4.21.5 add owner/repo/item
npx shadcn@4.21.5 add --all

# Preview changes before adding/updating.
npx shadcn@4.21.5 add button --dry-run
npx shadcn@4.21.5 add button --diff button.tsx
npx shadcn@4.21.5 add @acme/form --view button.tsx
npx shadcn@4.21.5 add owner/repo/item --dry-run

# Search registries.
npx shadcn@4.21.5 search @shadcn -q "sidebar"
npx shadcn@4.21.5 search @tailark -q "stats"
npx shadcn@4.21.5 search owner/repo -q "login"
npx shadcn@4.21.5 search                          # all configured registries
npx shadcn@4.21.5 search @shadcn -q "menu" -t ui  # filter by item type

# Get component docs and example URLs.
npx shadcn@4.21.5 docs button dialog select

# View registry item details (for items not yet installed).
npx shadcn@4.21.5 view @shadcn/button
npx shadcn@4.21.5 view owner/repo/item
```

**Named presets:** `nova`, `vega`, `maia`, `lyra`, `mira`, `luma`
**Templates:** `next`, `vite`, `start`, `react-router`, `astro` (all support `--monorepo`) and `laravel` (not supported for monorepo)
**Preset codes:** Version-prefixed base62 strings (e.g. `a2r6bw` or `b0`), from [ui.shadcn.com](https://ui.shadcn.com).
