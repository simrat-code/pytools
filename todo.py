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
    lines.sort(key=lambda x: "[x]" in x)  # Sort tasks with done tasks at the end
    TODO_FILE.write_text("\n".join(lines) + "\n")

class TodoApp:
    def __init__(self):
        self.header = urwid.Text(" TODO Manager — q to quit, a to add, f to filter, space to toggle")
        self.tasks = []
        self.category_filter = None
        self.listbox = urwid.ListBox(urwid.SimpleFocusListWalker([]))
        self.frame = urwid.Frame(header=urwid.AttrWrap(self.header, 'header'), body=self.listbox)
        self.refresh()
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

    def refresh(self):
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
        save_tasks(self.tasks)
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
            save_tasks(self.tasks)
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

    def unhandled_input(self, key):
        if key in ('q', 'Q'):
            save_tasks(self.tasks)
            raise urwid.ExitMainLoop()
        elif key == 'a':
            self.add_task_popup()
        elif key == 'f':
            self.filter_popup()
        elif key == 'r':
            self.refresh()

    def run(self):
        self.loop.run()

if __name__ == "__main__":
    TodoApp().run()
