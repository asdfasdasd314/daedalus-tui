"""Selectable transcript rendering with semantic assistant-message emphasis."""

from __future__ import annotations

from rich.style import Style
from rich.text import Text
from rich.cells import cell_len
from textual import events
from textual.strip import Strip
from textual.widgets import Log


class TranscriptLog(Log):
    """A selectable log that can emphasize a task's final assistant message.

    ``Log`` deliberately stores plain strings, so its normal CSS color applies
    to every line. Keeping the line tone separately lets the transcript retain
    Log's native selection behavior while giving the final task summary a
    brighter color.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._line_tones: dict[int, str] = {}
        self._final_color = None
        self._messages: list[tuple[str, bool]] = []

    @property
    def line_tones(self) -> tuple[str, ...]:
        """Return the tone assigned to each rendered transcript line."""
        return tuple(self._line_tones.get(index, "generic") for index in range(len(self._lines)))

    def clear(self) -> "TranscriptLog":
        self._line_tones.clear()
        self._messages.clear()
        return super().clear()

    def on_resize(self, event: events.Resize) -> None:
        """Reflow stored messages when the output box changes width."""
        if self._messages:
            self._rebuild_lines(scroll_end=self.auto_scroll)

    def set_final_color(self, color) -> None:
        """Use the prompt's normal text color for the final transcript tone."""
        self._final_color = color
        self.invalidate_render_cache()

    def invalidate_render_cache(self) -> None:
        """Re-render lines after a surrounding widget's color state changes."""
        self._render_line_cache.clear()
        self.refresh()

    def write_message(self, message: str, *, final: bool = False) -> "TranscriptLog":
        """Append one assistant message and assign its semantic tone."""
        if not message:
            return self
        self._messages.append((message, final))
        self._rebuild_lines(scroll_end=self.auto_scroll)
        return self

    def _rebuild_lines(self, *, scroll_end: bool) -> None:
        """Render logical messages as wrapped, selectable Log lines."""
        width = self._content_width()
        rendered_lines: list[str] = []
        tones: list[str] = []
        for message_index, (message, final) in enumerate(self._messages):
            if message_index:
                # Keep one complete blank line between streamed messages.
                rendered_lines.append("")
                tones.append("generic")

            tone = "final" if final else "generic"
            for source_line in message.split("\n"):
                wrapped_lines = self._wrap_line(source_line, width)
                rendered_lines.extend(wrapped_lines)
                tones.extend([tone] * len(wrapped_lines))

        block = "\n".join(rendered_lines)
        if block:
            # Log keeps a trailing empty entry as the insertion point for its
            # next write; it is not included in line_count.
            block += "\n"
        super().clear()
        super().write(block, scroll_end=scroll_end)
        self._line_tones = {
            line_number: tone for line_number, tone in enumerate(tones)
        }
        self._render_line_cache.clear()

    def _content_width(self) -> int:
        """Return the width available for transcript text inside the Log."""
        # ``size.width`` includes the output border and padding. Wrapping to
        # that outer width lets the final characters run into the box chrome,
        # so use Textual's content region for the actual text width.
        content_region = self.content_region
        width = content_region.width
        if width <= 0:
            # Messages can arrive before the first layout pass. Keep them
            # temporarily unwrapped; the first resize/layout event will
            # rebuild them using the content region.
            width = self.size.width
        return max(0, width)

    def _wrap_line(self, line: str, width: int) -> list[str]:
        """Wrap one logical line without changing its selectable text."""
        processed_line = self._process_line(line)
        if not processed_line or width <= 0 or cell_len(processed_line) <= width:
            return [processed_line]
        wrapped = Text(processed_line).wrap(
            self.app.console,
            width=width,
            overflow="fold",
        )
        return [wrapped_line.plain for wrapped_line in wrapped] or [""]

    def _render_line_strip(self, y: int, rich_style: Style) -> Strip:
        """Render a line with the final-message color before selection styling."""
        selection = self.text_selection
        if y in self._render_line_cache and selection is None:
            return self._render_line_cache[y]

        line = self._process_line(self._lines[y])
        line_text = Text(line, no_wrap=True)
        line_text.stylize(rich_style)
        if self._line_tones.get(y) == "final" and self._final_color is not None:
            line_text.stylize(Style(color=self._final_color))

        if self.highlight:
            line_text = self.highlighter(line_text)
        if selection is not None:
            if (select_span := selection.get_span(y - self._clear_y)) is not None:
                start, end = select_span
                if end == -1:
                    end = len(line_text)
                selection_style = self.screen.get_component_rich_style("screen--selection")
                line_text.stylize(selection_style, start, end)

        rendered_line = Strip(line_text.render(self.app.console), cell_len(line))
        if selection is not None:
            self._render_line_cache[y] = rendered_line
        return rendered_line
