"""Selectable transcript rendering with semantic assistant-message emphasis."""

from __future__ import annotations

from rich.style import Style
from rich.text import Text
from rich.cells import cell_len
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

    @property
    def line_tones(self) -> tuple[str, ...]:
        """Return the tone assigned to each rendered transcript line."""
        return tuple(self._line_tones.get(index, "generic") for index in range(len(self._lines)))

    def clear(self) -> "TranscriptLog":
        self._line_tones.clear()
        return super().clear()

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
        block = message if message.endswith("\n") else f"{message}\n"
        # Log keeps one trailing blank line as the insertion point for the
        # next write, so a subsequent message starts one line before len().
        first_line = max(0, len(self._lines) - 1)
        super().write(block)
        last_line = len(self._lines) - (1 if block.endswith("\n") else 0)
        tone = "final" if final else "generic"
        for line_number in range(first_line, last_line):
            self._line_tones[line_number] = tone
        self._render_line_cache.clear()
        return self

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
