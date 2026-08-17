"""The Daedalus prompt's incremental Vim editing adapter."""

from __future__ import annotations

from rich.segment import Segment
from rich.style import Style
from textual import events
from textual.strip import Strip
from textual.widgets.text_area import Selection

from vimkeys_input import VimMode, VimTextArea

from .clipboard import paste_from_system_clipboard

# Textual names `$` `dollar_sign`; vimkeys-input looks for `dollar`.
_LINE_END_KEYS = {"dollar", "dollar_sign", "$"}
# Use a left-aligned one-eighth block so the caret sits on the left edge of
# the character cell at the insertion point instead of in its visual center.
_INSERT_CURSOR_BAR = "▏"


class DaedalusVimTextArea(VimTextArea):
    """VimTextArea with multiline prompt behavior and system clipboard sync."""

    DEFAULT_CSS = """
    DaedalusVimTextArea.insert-mode .text-area--cursor {
        color: $text;
        background: transparent;
        text-style: none;
    }

    DaedalusVimTextArea.operator-pending .text-area--cursor {
        color: $text;
        background: transparent;
        text-style: underline;
    }
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # Keep the cursor visible continuously; blinking is distracting while
        # composing a prompt.
        self.cursor_blink = False

    @property
    def cursor_shape(self) -> str:
        """Return bar, underline, or block for the current Vim state."""
        operator_pending = getattr(self, "operator_pending", None)
        if operator_pending is not None and operator_pending.is_pending():
            return "underline"
        vim_mode = getattr(self, "vim_mode", VimMode.INSERT)
        if vim_mode == VimMode.INSERT:
            return "bar"
        return "block"

    @property
    def _draw_cursor(self) -> bool:
        # Insert mode paints a thin bar in render_line instead of a block.
        if self.cursor_shape == "bar" and not self.read_only:
            return False
        return super()._draw_cursor

    def enter_insert_mode(self) -> None:
        """Return to Insert mode after programmatic prompt operations."""
        self._enter_insert_mode()

    def _enter_insert_mode(self) -> None:
        self.operator_pending.clear()
        super()._enter_insert_mode()

    def _enter_command_mode(self) -> None:
        self.operator_pending.clear()
        super()._enter_command_mode()

    def _update_mode_display(self) -> None:
        super()._update_mode_display()
        self._sync_cursor_classes()

    def _sync_cursor_classes(self) -> None:
        """Expose operator-pending so the caret can become an underline."""
        self.set_class(self.operator_pending.is_pending(), "operator-pending")

    def nav_word_end(self) -> None:
        """Move to the end of the current word, or the next word when needed."""
        lines = [str(self.get_line(row)) for row in range(self.document.line_count)]
        characters: list[tuple[str, tuple[int, int]]] = []
        for row, line in enumerate(lines):
            characters.extend((character, (row, column)) for column, character in enumerate(line))
            if row < len(lines) - 1:
                characters.append(("\n", (row, len(line))))

        row, column = self.cursor_location
        index = sum(len(line) + 1 for line in lines[:row]) + column
        if index >= len(characters):
            return

        def kind(character: str) -> str | None:
            if character.isspace():
                return None
            return "word" if character.isalnum() or character == "_" else "punctuation"

        current_kind = kind(characters[index][0])
        if current_kind is not None:
            end = index
            while end + 1 < len(characters) and kind(characters[end + 1][0]) == current_kind:
                end += 1
            if end > index:
                self.cursor_location = characters[end][1]
                return
            index = end + 1

        while index < len(characters) and kind(characters[index][0]) is None:
            index += 1
        if index >= len(characters):
            return

        target_kind = kind(characters[index][0])
        end = index
        while end + 1 < len(characters) and kind(characters[end + 1][0]) == target_kind:
            end += 1
        self.cursor_location = characters[end][1]

    def _handle_insert_mode(self, event: events.Key) -> None:
        """Keep Enter as a newline; Ctrl+Enter remains the app submit key."""
        if event.key == "enter":
            return
        super()._handle_insert_mode(event)

    def on_key(self, event: events.Key) -> None:
        """Route visual-line mode and mirror new yanks to the host clipboard."""
        if event.key == "ctrl+k":
            # VimTextArea handles several Ctrl keys itself, so route the
            # application's shortcut before its mode-specific processing.
            self.app.action_show_shortcuts()
            event.stop()
            return
        previous_register = self.yank_register
        if event.key == "escape":
            super().on_key(event)
            # Vim mode transitions do not clear TextArea's native selection.
            # Collapse it so Escape reliably stops all highlighting.
            self.selection = Selection.cursor(self.cursor_location)
        elif self.vim_mode == VimMode.VISUAL_LINE:
            self._handle_visual_line_mode(event)
        else:
            super().on_key(event)
        if self.yank_register and self.yank_register != previous_register:
            self.app.copy_to_clipboard(self.yank_register)

    def edit_paste_after(self) -> None:
        """Paste Vim's register, falling back to the system clipboard."""
        if not self.yank_register:
            clipboard_text = paste_from_system_clipboard()
            if clipboard_text:
                self.yank_register = clipboard_text
        super().edit_paste_after()

    def edit_paste_before(self) -> None:
        """Paste before the cursor, including from the system clipboard."""
        if not self.yank_register:
            clipboard_text = paste_from_system_clipboard()
            if clipboard_text:
                self.yank_register = clipboard_text
        super().edit_paste_before()

    def _handle_command_mode(self, event: events.Key) -> None:
        """Add Daedalus prompt commands that the dependency does not provide."""
        if event.key == "V":
            self._enter_visual_line_mode()
            event.prevent_default()
            return
        if event.key == "space":
            self.nav_right()
            event.prevent_default()
            return
        if event.key in _LINE_END_KEYS:
            # Textual reports `$` as dollar_sign; vimkeys-input listens for dollar.
            event.key = "dollar"
        super()._handle_command_mode(event)
        self._sync_cursor_classes()

    def render_line(self, y: int) -> Strip:
        strip = super().render_line(y)
        if self.cursor_shape != "bar" or not self.has_focus or self.read_only:
            return strip
        cursor_x, cursor_y = self._cursor_offset
        scroll_x, scroll_y = self.scroll_offset
        if y + scroll_y != cursor_y:
            return strip
        bar_x = cursor_x - scroll_x + self.gutter_width
        return self._overlay_insert_bar(strip, bar_x)

    def _overlay_insert_bar(self, strip: Strip, x: int) -> Strip:
        """Paint a thin left-aligned caret at the insertion point."""
        if strip.cell_length <= 0:
            return strip
        # Replace the cell at the insertion point instead of joining an
        # additional caret cell. This keeps text to the right from shifting
        # while the underlying TextArea document remains unchanged.
        x = max(0, min(x, strip.cell_length - 1))
        parts = strip.divide([x, x + 1, strip.cell_length])
        if len(parts) < 2:
            return strip
        cursor_style = self.get_component_rich_style("text-area--cursor")
        bar_style = Style(color="white", bgcolor=cursor_style.bgcolor)
        bar = Strip([Segment(_INSERT_CURSOR_BAR, bar_style)], 1)
        trailing = parts[2:] if len(parts) > 2 else []
        return Strip.join([parts[0], bar, *trailing])

    def _enter_visual_line_mode(self) -> None:
        """Select the current line and enter Vim visual-line mode."""
        self.vim_mode = VimMode.VISUAL_LINE
        self.visual_start = self.cursor_location
        self._set_visual_line_selection()
        self._update_mode_display()

    def _set_visual_line_selection(self) -> None:
        """Select every character in the lines between the start and cursor."""
        start_row = self.visual_start[0] if self.visual_start else self.cursor_location[0]
        cursor_row = self.cursor_location[0]
        first_row = min(start_row, cursor_row)
        last_row = max(start_row, cursor_row)
        if last_row < self.document.line_count - 1:
            end = (last_row + 1, 0)
        else:
            end = (last_row, len(str(self.get_line(last_row))))
        self.selection = Selection(start=(first_row, 0), end=end)

    def _handle_visual_line_mode(self, event: events.Key) -> None:
        """Handle movement and operators while whole lines are selected."""
        key = event.key
        if self.pending_command == "g" and key == "g":
            self.nav_document_start()
            self.pending_command = None
        elif key == "j":
            self.nav_down()
        elif key == "k":
            self.nav_up()
        elif key == "G":
            self.nav_document_end()
        elif key == "g":
            self.pending_command = "g"
            event.prevent_default()
            return
        elif key == "y":
            self.visual_yank()
            self._enter_command_mode()
        elif key in {"d", "x"}:
            self.visual_delete()
            self._enter_command_mode()
        elif key == "c":
            self.visual_change()
        elif key == "V":
            self._enter_command_mode()
        else:
            event.prevent_default()
            return
        if self.vim_mode == VimMode.VISUAL_LINE:
            self._set_visual_line_selection()
        event.prevent_default()


__all__ = ["DaedalusVimTextArea", "VimMode"]
