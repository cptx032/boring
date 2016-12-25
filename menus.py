# menu
import widgets
from window import *

class CommandChooserWindow(SubWindow):
    INSTANCE = None
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

        self.add_items(self.__items)

        self.entry.bind('<Escape>', lambda e: self.hide(), '+')
        self.bind('<Any-KeyRelease>', self.__key_handler, '+')
        self.entry.bind('<Return>', self.__run_selected_command_handler, '+')
        self.entry.bind('<Down>', lambda event: self.commands.down_selection(), '+')
        self.entry.bind('<Up>', lambda event: self.commands.up_selection(), '+')

        if not CommandChooserWindow.INSTANCE:
            CommandChooserWindow.INSTANCE = self

    @staticmethod
    def popup(items):
        CommandChooserWindow.INSTANCE.items = items
        CommandChooserWindow.INSTANCE.show_items(items)
        CommandChooserWindow.INSTANCE.show()

    def add_command(self, item):
        self.__items.append(item)

    def add_commands(self, items):
        self.__items.extend(item)

    def add_items(self, items):
        for i in items:
            self.commands.add_item(
                i.get('name'),
                before_click=self.__item_click_handler(
                    i.get('command', None)
                ),
                subtitle=i.get('subtitle', None),
                icon=i.get('icon', None)
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

        self.show_items(final_items)

    def show_items(self, items):
        self.commands.delete_all()
        self.add_items(items)
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
        self.master.focus_force()

    @property
    def items(self):
        return self.__items

    @items.setter
    def items(self, value):
        self.__items = value

class OptionMenu(widgets.Button):
    def __init__(self, master, options=[], initial_index=0, get_items_func=None, **kws):
        '''
        options = [
            {
                'name': 'Title',
                'icon': 'Icon',
                'subtitle': 'Subtitle'
            },
            {}, {} ...
        ]

        If get_items_func is provided the items will be the result of call
        of this function
        '''
        self.__options = options
        self.get_items_func = get_items_func
        widgets.Button.__init__(self, master, **kws)

        self.bind('<1>', self.__click, '+')
        self.options = self.__options

        self.select_by_index(initial_index)

    def __click(self, event=None):
        self.show()

    def select_by_index(self, index):
        if (index >= 0) and (index < len(self.options)):
            self.text = self.options[index]['name']

    @property
    def options(self):
        return self.__options

    def __gen_command(self, item):
        def __final_handler(*args):
            self.text = item.get('name')
        return __final_handler

    @options.setter
    def options(self, value):
        for i in value:
            i['command'] = self.__gen_command(i)
        self.__options = value

    def show(self, options=None):
        if options:
            self.options = options
        if self.get_items_func:
            self.options = self.get_items_func()
        CommandChooserWindow.popup(self.options)

    @property
    def value(self):
        return self.text

    @value.setter
    def value(self, value):
        self.text = value

if __name__ == '__main__':
    top = Window()
    # Just to create a instance
    CommandChooserWindow(top).hide()
    options = []
    for i in range(30):
        options.append({
            'name': 'Option %d' % (i),
            'subtitle': 'Options %d subtitle' % (i)
        })
    optionmenu = OptionMenu(top, options=options)
    optionmenu.pack(pady=5, padx=5)
    top.mainloop()