# menu
import widgets
from . import *

class CommandChooserWindow(SubWindow):
    def __init__(self, master,
            width=800, height=300,
            items=[], search_words=False,
            verify_case=False):
        self.__width = int(width)
        self.__height = int(height)
        self.__items = items
        self.search_words = search_words
        self.verify_case = verify_case
        SubWindow.__init__(self, master)

        self.entry = widgets.Entry(self)
        pad = 8
        self.entry.pack(
            fill='x',
            pady=pad,
            padx=pad
        )
        self.commands = widgets.ScrollableExtendedListbox(
            self,
            width=self.__width,
            height=self.__height
        )
        self.commands.pack(
            expand='yes',
            fill='both',
            pady=0,
            padx=pad
        )
        self.center()

        self.overrideredirect(True)

        self.__add_items(self.__items)

        self.entry.bind('<Escape>', lambda e: self.hide(), '+')
        self.bind('<Any-KeyRelease>', self.__key_handler, '+')
        self.entry.bind('<Return>', self.__run_selected_command_handler ,'+')
        self.entry.bind('<Down>', lambda event: self.commands.down_selection(), '+')
        self.entry.bind('<Up>', lambda event: self.commands.up_selection(), '+')

    def __add_items(self, items):
        for i in items:
            self.commands.add_item(
                i.get('name'),
                before_click=self.__item_click_handler(
                    i.get('command', None)
                )
            )

    def __key_handler(self, event):
        if event.keysym in ('Up', 'Down', 'Return', 'Escape'):
            return
        final_items = []
        entry_text = self.entry.text
        if not self.verify_case:
            entry_text = entry_text.lower()
        words = set(entry_text.split(' '))

        for menu in self.__items:
            menu_title = menu.get('name')
            if not self.verify_case:
                menu_title = menu_title.lower()

            if self.search_words:
                menu_words = set(menu_title.split(' '))
                if words.issubset(menu_words):
                    final_items.append(menu)
            else:
                if entry_text in menu_title:
                    final_items.append(menu)

        self.commands.delete_all()
        self.__add_items(final_items)
        self.commands.select_first()


    def __run_selected_command_handler(self, event):
        selected = self.commands.get_selected()
        if selected:
            selected.before_click(None)
            self.entry.text = ''

    def __item_click_handler(self, function):
        def __final_function(*args):
            self.hide()
            if function:
                function(*args)
        return __final_function

    def show(self):
        self.deiconify()
        self.center()
        # passing keyboardfocus to the window:
        self.grab_set()
        self.entry.focus_force()

    def hide(self):
        self.grab_release()
        self.withdraw()
        self.master.grab_set()
        self.master.focus_force()