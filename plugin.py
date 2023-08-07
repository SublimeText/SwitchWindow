import os
from pathlib import Path

import sublime
import sublime_plugin

_history = []


class WindowInputHandler(sublime_plugin.ListInputHandler):
    def name(self):
        return "window_id"

    def placeholder(self):
        return "Choose a window"

    def list_items(self):
        def active_file(window):
            view = window.active_view()
            if not view:
                return (None, None)
            try:
                file = Path(view.file_name())
                return (file.parent, file.name)
            except:
                return (None, view.name())

        def active_folder(folders, active_file_path):
            if active_file_path:
                for folder in folders:
                    try:
                        folder = Path(folder)
                        active_file_path.relative_to(folder)
                        return folder
                    except ValueError:
                        continue
            return Path(folders[0])

        def transform_folder(folder):
            try:
                home = "USERPROFILE" if os.name == "nt" else "HOME"
                return f"~{os.sep}{folder.relative_to(os.getenv(home, ''))}"
            except ValueError:
                return folder

        def create_item(window):
            active_file_path, active_file_name = active_file(window)
            folders = window.folders()
            workspace = window.workspace_file_name()

            if workspace:
                title = Path(workspace).stem
                kind = [sublime.KIND_ID_NAMESPACE, "P", "Project"]
                if folders:
                    second_line = transform_folder(
                        active_folder(folders, active_file_path)
                    )
                else:
                    second_line = "No folders in project yet!"

            elif folders:
                folder = active_folder(folders, active_file_path)
                title = folder.name
                kind = [sublime.KIND_ID_NAVIGATION, "F", "Folder"]
                second_line = transform_folder(folder)

            elif active_file_path:
                title = active_file_name
                kind = [sublime.KIND_ID_NAVIGATION, "f", "File"]
                second_line = transform_folder(active_file_path)

            else:
                title = active_file_name
                kind = [sublime.KIND_ID_AMBIGUOUS, "S", "Scratch"]
                second_line = "Scratch Window"

            return sublime.ListInputItem(
                text=title or "untitled",
                value=window.id(),
                annotation=f"Window {window.id()}",
                kind=kind,
                details=[f"<i>{second_line}</i>"],
            )

        # add current window to the end of the selection list
        return [create_item(window) for window in _history[1:]] + [create_item(_history[0])]


class SwitchWindowCommand(sublime_plugin.ApplicationCommand):
    def input_description(self):
        return "Switch Window"

    def input(self, args):
        if 'previous_window' not in args and args.get("window_id") is None:
            return WindowInputHandler()
        return None

    def run(self, previous_window=False, window_id=None):
        """
        Execute `switch_window` command

        :param previous_window:
            If ``true`` directly switch to previous window.
        :param window_id:
            The window identifier of the window to switch to.
        """
        if previous_window:
            if len(_history) >= 2:
                _history[1].bring_to_front()
            return

        for window in sublime.windows():
            if window.id() == window_id:
                window.bring_to_front()
                break


class SwitchWindowListener(sublime_plugin.EventListener):
    def on_activated(self, view):
        global _history

        window = view.window()
        if not window:
            return

        windows = sublime.windows()

        # add missing windows to stack
        for w in windows:
            if w not in _history:
                _history.append(w)

        # remove closed windows from stack
        for w in _history:
            if w not in windows:
                _history.remove(w)

        # abort on empty stack
        if not _history:
            return

        # abort if active window is already on top
        if window == _history[0]:
            return

        # move active window to top
        try:
            _history.remove(window)
        except:
            pass
        _history.insert(0, window)
