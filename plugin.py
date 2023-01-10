import os
from pathlib import Path

import sublime
import sublime_plugin


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

        return [create_item(window) for window in sublime.windows()]


class SwitchWindowCommand(sublime_plugin.ApplicationCommand):
    def input_description(self):
        return "Switch Window"

    def input(self, args):
        if args.get("window_id") is None:
            return WindowInputHandler()
        return None

    def run(self, window_id=None):
        for window in sublime.windows():
            if window.id() == window_id:
                window.bring_to_front()
                break
