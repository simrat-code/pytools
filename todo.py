#!/usr/bin/env python3
import urwid
import logging
from pathlib import Path
from datetime import date

TODO_FILE = Path.home() / "todo" / "todo.txt"
LOG_FILE = Path.home() / "todo" / "debug.log"
CATEGORIES = {"work", "chatops", "ai", "other"}

TODO_FILE.parent.mkdir(parents=True, exist_ok=True)
TODO_FILE.touch()

LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
_logger = logging.getLogger(__name__)


def load_tasks():
    return TODO_FILE.read_text().strip().splitlines()

def save_tasks(lines):
    _logger.info(f"writing to file {len(lines)} tasks")
    lines.sort(key=lambda x: "[x]" in x)  # Sort tasks with done tasks at the end
    TODO_FILE.write_text("\n".join(lines) + "\n")

class TodoApp:
    def __init__(self):
        self.header = urwid.Text(" TODO Manager — q: quit, a: add, e: edit, f: filter, s: save, space: toggle")
        self.tasks = []
        self.category_filter = None
        self.dirty = False
        self.listbox = urwid.ListBox(urwid.SimpleFocusListWalker([]))
        self.frame = urwid.Frame(header=urwid.AttrWrap(self.header, 'header'), body=self.listbox)
        self.refresh(reload=True)
        self.loop = urwid.MainLoop(self.frame, palette=[('header', 'black', 'light gray')],
                                   unhandled_input=self.unhandled_input)

    def parse_task(self, line):
        #
        # [x] [category] YYYY-MM-DD description
        #
        status = "[x]" in line
        
        first_bracket = line.find("[")
        cat_start = line.find("[", first_bracket+1) + 1
        cat_end = line.find("]", cat_start)

        category = line[cat_start:cat_end] if cat_start != -1 and cat_end != -1 else "unknown"
        # Try to extract date
        rest = line[cat_end + 1:].strip()
        try:
            task_date = rest.split()[0]
            description = " ".join(rest.split()[1:])
        except IndexError:
            task_date = "unknown"
            description = rest
        return status, category, task_date, description

    def format_category(self, cat):
        return f"{cat[:10]:<10}"

    def build_task_widget(self, i, line):
        status, category, task_date, text = self.parse_task(line)
        if self.category_filter and category != self.category_filter:
            return None
        label = f"[{self.format_category(category)}] {task_date}: {text}"
        chk = urwid.CheckBox(label, state=status, user_data=i)
        urwid.connect_signal(chk, name='change', callback=self.on_toggle, user_args=[i])
        return chk

    def refresh(self, reload=False):
        if reload:
            self.tasks = load_tasks()
        self.tasks.sort(key=lambda x: "[x]" in x)

        widgets = []
        done_widgets = []
        for i, line in enumerate(self.tasks):            
            w = self.build_task_widget(i, line)
            if w:
                widgets.append(w)
        self.listbox.body[:] = widgets

    def on_toggle(self, index, widget, new_state):
        line = self.tasks[index]
        if new_state:
            self.tasks[index] = line.replace("[ ]", "[x]", 1)
        else:
            self.tasks[index] = line.replace("[x]", "[ ]", 1)
        # save_tasks(self.tasks)
        self.dirty = True
        self.refresh()

    def add_task_popup(self):
        def on_submit(button):            
            cat = selected_cat[0]
            txt = task_edit.edit_text.strip()

            if not txt:
                error.set_text("Task description cannot be empty.")
                return
            today = date.today().isoformat()
            formatted = f"[ ] [{cat}] {today} {txt}"
            self.tasks.append(formatted)
            # save_tasks(self.tasks)
            self.dirty = True
            self.loop.widget = self.frame
            self.refresh()

        selected_cat = [list(CATEGORIES)[0]]  # Default selected category
        # Create RadioButtons for each category
        radio_group = []
        cat_buttons = []
        for cat in sorted(CATEGORIES):
            btn = urwid.RadioButton(radio_group, cat, state=(cat == selected_cat[0]))
            urwid.connect_signal(btn, 'change', lambda button, state: selected_cat.__setitem__(0, button.label) if state else None)
            cat_buttons.append(btn)

        task_edit = urwid.Edit("Task: ")
        # category_edit = urwid.Edit("Category: ")
        error = urwid.Text("")
        pile = urwid.Pile(cat_buttons + [task_edit, error, urwid.Button("Add", on_press=on_submit)])
        fill = urwid.Filler(pile)
        self.loop.widget = urwid.Overlay(fill, self.frame, 'center', ('relative', 50), 'middle', ('relative', 30))

    def edit_selected_task(self):
        # focus_widget, pos = self.listbox.get_focus() # deprecated
        # body = self.listbox.body
        focus_widget = self.listbox.focus
        pos = self.listbox.focus_position

        if focus_widget is None:
            return

        index = pos
        status, category, task_date, description = self.parse_task(self.tasks[index])

        category_edit = urwid.Edit("Category: ", edit_text=category)
        description_edit = urwid.Edit("Description: ", edit_text=description)
        error = urwid.Text("")

        def on_save(button):
            new_cat = category_edit.edit_text.strip()
            new_desc = description_edit.edit_text.strip()

            if new_cat not in CATEGORIES:
                error.set_text(f"Invalid category. Choose: {', '.join(CATEGORIES)}")
                return

            new_line = f"[{'x' if status else ' '}] [{new_cat}] {task_date} {new_desc}"
            self.tasks[index] = new_line
            self.dirty = True
            self.loop.widget = self.frame
            self.refresh()

        save_btn = urwid.Button("Save", on_press=on_save)
        cancel_btn = urwid.Button("Cancel", on_press=lambda btn: setattr(self.loop, "widget", self.frame))

        pile = urwid.Pile([category_edit, description_edit, error, urwid.Columns([save_btn, cancel_btn])])
        overlay = urwid.Overlay(urwid.LineBox(pile), self.frame, 'center', ('relative', 50), 'middle', ('relative', 30))
        self.loop.widget = overlay

    def filter_popup(self):
        def on_select(button, cat):
            self.category_filter = cat if cat != "All" else None
            self.loop.widget = self.frame
            self.refresh()

        buttons = [urwid.Button("All", on_press=on_select, user_data="All")]
        buttons += [urwid.Button(cat, on_press=on_select, user_data=cat) for cat in sorted(CATEGORIES)]
        menu = urwid.ListBox(urwid.SimpleFocusListWalker(buttons))
        overlay = urwid.Overlay(urwid.LineBox(menu), self.frame, 'center', 20, 'middle', 10)
        self.loop.widget = overlay

    def confirm_exit(self):
        def on_choice(button, choice):
            if choice == "Save":
                save_tasks(self.tasks)
            raise urwid.ExitMainLoop()

        save_btn = urwid.Button("Save", on_press=on_choice, user_data="Save")
        discard_btn = urwid.Button("Discard", on_press=on_choice, user_data="Discard")
        cancel_btn = urwid.Button("Cancel", on_press=lambda btn: setattr(self.loop, "widget", self.frame))

        pile = urwid.Pile([
            urwid.Text("You have unsaved changes.\nSave before quitting?"),
            urwid.Columns([save_btn, discard_btn, cancel_btn], dividechars=2)
        ])
        overlay = urwid.Overlay(urwid.LineBox(pile), self.frame, 'center', 40, 'middle', 7)
        self.loop.widget = overlay

    def unhandled_input(self, key):
        if key in ('q', 'Q'):
            if self.dirty:
                self.confirm_exit()
                # save_tasks(self.tasks)
            else:
                raise urwid.ExitMainLoop()

        elif key == 'a':
            self.add_task_popup()
        
        elif key == 'e':
            self.edit_selected_task()

        elif key == 'f':
            self.filter_popup()
        
        elif key == 'r':
            self.refresh()
        
        elif key == 's':
            save_tasks(self.tasks)
            self.dirty = False

    def run(self):
        self.loop.run()

if __name__ == "__main__":
    TodoApp().run()
