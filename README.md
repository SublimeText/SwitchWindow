# Switch Window

A Sublime Text plugin which lets you 
quickly switch between open Sublime Text windows 
via Command Palette without having to press <kbd>cmd+~</kbd> on MacOS 
or <kbd>alt+tab</kbd> on Linuy/Windows.

![](preview.png)
## Installation

### Package Control

The easiest way to install is using [Package Control](https://packagecontrol.io). It's listed as `Switch Window`.

1. Open `Command Palette` using <kbd>ctrl+shift+P</kbd> or menu item `Tools → Command Palette...`
2. Choose `Package Control: Install Package`
3. Find `Switch Window` and hit <kbd>Enter</kbd>

### Manual Install

1. Download [Switch Window.sublime-package](https://github.com/SublimeText/SwitchWindow/releases).
2. Copy it into _Installed Packages_ directory
   
> To find _Installed Packages_...
>
> 1. call _Menu > Preferences > Browse Packages.._
> 2. Navigate to parent folder

## Usage

1. Open `Command Palette` using <kbd>ctrl+shift+P</kbd> or menu item `Tools → Command Palette...`
2. Type `Switch: Window` and hit <kbd>enter</kbd>

or hit <kbd>ctrl+k</kbd>, <kbd>ctrl+tab</kbd> in sequence
to show the `Switch Window` Quick Panel directly.

## Kind Info

The kind of a window is displayed via icon.

| icon | description
|:----:|:---
| P    | A project/workspace is opened in the window
| F    | One or more folders are opened in the window. The best matching one according to the active file is displayed in description line.
| f    | A file is displayed in active view of a window, which has no project or folder open.
| S    | An unsaved view is displayed in active view of a window, which has no project or folder open.