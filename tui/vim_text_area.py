"""The Daedalus prompt's incremental Vim editing adapter."""

from __future__ import annotations

from textual import events
from textual.widgets.text_area import Selection

from vimkeys_input import VimMode, VimTextArea

from .clipboard import paste_from_system_clipboard


class DaedalusVimTextArea(VimTextArea):
    """VimTextArea with multiline prompt behavior and system clipboard sync."""

    def enter_insert_mode(self) -> None:
        """Return to Insert mode after programmatic prompt operations."""
        self._enter_insert_mode()

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
        super()._handle_command_mode(event)

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
