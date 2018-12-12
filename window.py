# Boring

import sys


def import_tkinter():
    """Import the correct version of Tkinter."""
    try:
        import Tkinter as tk
    except ImportError:
        try:
            import tkinter as tk
        except ImportError:
            print('You must have Tkinter installed')
            sys.exit(-1)
    return tk

tk = import_tkinter()


def get_photo_class():
    try:
        from PIL import ImageTk
        return ImageTk.PhotoImage
    except ImportError:
        return tk.PhotoImage


class GenericWindow(object):
    '''
    Generic for Tk and Toplevel
    '''
    @property
    def caption(self):
        return self.title()

    @caption.setter
    def caption(self, value):
        self.title(value)

    @property
    def width(self):
        return int(self.winfo_width())

    @width.setter
    def width(self, value):
        self['width'] = value

    @property
    def height(self):
        return int(self.winfo_height())

    @height.setter
    def height(self, value):
        self['height'] = value

    def maximize(self):
        # TODO: Windows
        self.attributes('-zoomed', 1)

    def enable_kmap(self):
        self.kmap = dict()
        self.bind('<Any-Key>', self._update_kmap_press, '+')
        self.bind('<Any-KeyRelease>', self._update_kmap_release, '+')

    def _update_kmap_press(self, event):
        self.kmap[event.keysym] = True

    def _update_kmap_release(self, event):
        self.kmap[event.keysym] = False

    def center(self):
        '''
        centralizes the window in the screen
        '''
        self.update_idletasks()
        sw = int(self.winfo_screenwidth())
        sh = int(self.winfo_screenheight())
        ww = int(self.winfo_width())
        wh = int(self.winfo_height())
        xpos = (sw / 2) - (ww / 2)
        ypos = (sh / 2) - (wh / 2)
        self.geometry('+%d+%d' % (xpos, ypos))

    def enable_escape(self):
        u"""Close the window when Escape Key is pressed."""
        self.bind('<Escape>', lambda *args, **kws: self.destroy(), '+')

    def add_menu(self, _list):
        '''
        [
            [
                'File', [
                    {
                        'title': 'Open Project',
                        'command': self.__open_project,
                        'shortcut': 'Control-O'
                    }
                ]
            ]
        ]
        '''
        if not hasattr(self, '__menu'):
            self.__menu = tk.Menu(
                self,
                relief='flat'
            )
            self.__menus = {}
        for menu in _list:
            self.__menus[menu[0]] = tk.Menu(
                self.__menu,
                tearoff=0,
                relief='flat'
            )
            for item in menu[1]:
                self.__menus[menu[0]].add_command(
                    label=item['title'],
                    command=item['command'],
                    underline=0,  # TODO: auto
                    accelerator=item.get('shortcut', None)
                )
                # TODO: error
                if item.get('shortcut', None):
                    self.bind(
                        '<%s>' % (item['shortcut']),
                        item['command'],
                        '+'
                    )
            self.__menu.add_cascade(
                label=menu[0],
                menu=self.__menus[menu[0]],
                underline=0  # TODO: identificar a letra automaticamente
            )
        self.config(
            menu=self.__menu
        )


class SubWindow(tk.Toplevel, GenericWindow):
    def __init__(self, *args, **kws):
        tk.Toplevel.__init__(self, *args, **kws)
        GenericWindow.__init__(self)


class Window(tk.Tk, GenericWindow):
    def __init__(self, title='', bg='#ededed'):
        tk.Tk.__init__(self)
        GenericWindow.__init__(self)
        self.caption = title
        self.config(
            bg=bg
        )


if __name__ == '__main__':
    top = Window(title='Enable escape')
    top.enable_escape()

    def _handler(event=None):
        print('handler called')

    top.add_menu(
        [
            [
                'File', [
                    {
                        'title': 'Open Project',
                        'command': _handler,
                        'shortcut': 'Control-o'
                    }
                ]
            ]
        ]
    )
    top.mainloop()
