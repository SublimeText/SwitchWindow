import os

import sublime
import sublime_plugin


class WindowInputHandler(sublime_plugin.ListInputHandler):

    def name(self):
        return "window_id"

    def placeholder(self):
        return "Chosse a window"

    def list_items(self):
        items = []

        kind_project = [sublime.KIND_ID_NAMESPACE, "🗔", "Project"]
        kind_file = [sublime.KIND_ID_NAVIGATION, "🗔", "File"]

        for window in sublime.windows():
            active_file_name = "untitled"
            view = window.active_view()
            if view:
                file_name = view.file_name()
                if file_name:
                    active_file_name = os.path.basename(file_name)
                elif view.name():
                    active_file_name = view.name()

            project_file_name = window.project_file_name()
            if project_file_name:
                title = f"Project: {os.path.splitext(os.path.basename(project_file_name))[0]}"
                kind = kind_project
                details = [
                    f"Active File: {active_file_name}"
                ]
            else:
                title = f"File: {active_file_name}"
                kind = kind_file
                details = [
                    f"Project: none"
                ]

            items.append(
                sublime.ListInputItem(
                    text=title,
                    value=window.id(),
                    annotation=f"Window {window.id()}",
                    kind=kind,
                    details=details
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
