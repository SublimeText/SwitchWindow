import os

import sublime
import sublime_plugin


class WindowInputHandler(sublime_plugin.ListInputHandler):

    def name(self):
        return "window_id"

    def placeholder(self):
        return "Choose a window"

    def list_items(self):
        items = []

        kind_project = [sublime.KIND_ID_NAMESPACE, "P", "Project"]
        kind_folder = [sublime.KIND_ID_NAMESPACE, "F", "Folder"]
        kind_file = [sublime.KIND_ID_NAVIGATION, "f", "File"]
        kind_scratch = [sublime.KIND_ID_AMBIGUOUS, "S", "Scratch"]

        active_window = sublime.active_window()
        for window in sublime.windows():
            if window == active_window:
                continue

            active_file_location = None
            active_file_name = "untitled"
            view = window.active_view()
            if view:
                file_name = view.file_name()
                if file_name:
                    active_file_location, active_file_name = os.path.split(file_name)
                elif view.name():
                    active_file_name = view.name()

            project_file_name = window.workspace_file_name()
            if project_file_name:
                title = os.path.splitext(os.path.basename(project_file_name))[0]
                kind = kind_project
                second_line = f"Active File: {active_file_name}"

            else:
                title = active_file_name

                folders = window.folders()
                if folders:
                    kind = kind_folder
                    for folder in window.folders():
                        if active_file_name.startswith(folder):
                            second_line = f"Folder: {folder}"
                            break
                    else:
                        second_line = f"Folder: {folders[0]}"
                elif active_file_location:
                    kind = kind_file
                    second_line = f"Location: {active_file_location}"
                else:
                    kind = kind_scratch
                    second_line = "Scratch Window"

            items.append(
                sublime.ListInputItem(
                    text=title,
                    value=window.id(),
                    annotation=f"Window {window.id()}",
                    kind=kind,
                    details=[second_line]
                )
            )

        return items


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

    def is_enabled(self):
        return len(sublime.windows()) > 1
