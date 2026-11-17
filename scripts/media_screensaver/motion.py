"""In-memory X11 motion sampling, with visible i3 bars masked before comparison."""
import time

from PIL import Image, ImageChops, ImageDraw, ImageGrab
from Xlib import X, display, error


class ScreenMotion:
    def __init__(self):
        self.connection = None
        self.reset()

    def reset(self):
        self.previous = None
        self.geometry = None
        self.last_motion = None
        self.quiet_seconds = 0

    def close(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None
        self.reset()

    def _capture(self, middle):
        if self.connection is None:
            self.connection = display.Display()
        connection = self.connection
        root = connection.screen().root
        width, height = middle['width'], middle['height']
        if width <= 0 or height <= 0:
            raise ValueError('invalid monitor geometry')
        bars = []
        windows = list(root.query_tree().children)
        for window in list(windows):
            try:
                if 'i3-frame' in (window.get_wm_class() or ()):
                    windows.extend(window.query_tree().children)
            except error.BadWindow:
                continue
        for window in windows:
            try:
                if not any('i3bar' in value.lower() for value in (window.get_wm_class() or ())):
                    continue
                if window.get_attributes().map_state != X.IsViewable:
                    continue
                geometry = window.get_geometry()
                origin = root.translate_coords(window, 0, 0)
                left = max(0, origin.x - middle['x'])
                top = max(0, origin.y - middle['y'])
                right = min(width, origin.x + geometry.width - middle['x'])
                bottom = min(height, origin.y + geometry.height - middle['y'])
                if left < right and top < bottom:
                    bars.append((left, top, right, bottom))
            except error.BadWindow:
                continue
        bounds = (middle['x'], middle['y'], middle['x'] + width, middle['y'] + height)
        image = ImageGrab.grab(bbox=bounds, xdisplay=connection.get_display_name())
        if image.size != (width, height):
            raise ValueError('incomplete X11 screen capture')
        return image, sorted(bars)


    def sample(self, middle):
        now = time.monotonic()
        try:
            image, bars = self._capture(middle)
            geometry = tuple(middle[key] for key in ('x', 'y', 'width', 'height')), tuple(bars)
            draw = ImageDraw.Draw(image)
            for left, top, right, bottom in bars:
                draw.rectangle((left, top, right - 1, bottom - 1), fill=0)
            frame = image.convert('L').resize((160, 90), Image.Resampling.BOX)
            changed = self.previous is None or geometry != self.geometry
            if not changed:
                difference = ImageChops.difference(self.previous, frame).histogram()
                # shortcut: motion approximates playback; use player detection if still scenes must block.
                changed = sum(difference[8:]) >= 8
            if changed:
                self.last_motion = now
                self.previous = frame
            self.geometry = geometry
            self.quiet_seconds = max(0, now - self.last_motion)
            if self.quiet_seconds >= 300:
                return True, f'screen quiet for {int(self.quiet_seconds)}s; i3 bar excluded'
            return False, f'screen motion quiet for {int(self.quiet_seconds)}s of 300s; i3 bar excluded'
        except Exception:
            self.reset()
            self.close()
            return False, 'screen motion detection unavailable; check X11 screen capture'
