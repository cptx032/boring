# Boring

import sys
PYTHON_3 = sys.version_info.major == 3
if PYTHON_3:
    import tkinter as Tkinter
    from tkinter import font as tkFont
    from tkinter import colorchooser as tkColorChooser
else:
    import Tkinter
    import tkFont
    import tkColorChooser

BG_COLOR = '#ededed'

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
            self.__menu = Tkinter.Menu(
                self,
                relief='flat'
            )
            self.__menus = {}
        for menu in _list:
            self.__menus[menu[0]] = Tkinter.Menu(
                self.__menu,
                tearoff=0,
                relief='flat'
            )
            for item in menu[1]:
                self.__menus[menu[0]].add_command(
                    label=item['title'],
                    command=item['command'],
                    underline=0, # TODO: auto
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
                underline=0 # TODO: identificar a letra automaticamente
            )
        self.config(
            menu=self.__menu
        )

class SubWindow(Tkinter.Toplevel, GenericWindow):
    def __init__(self, *args, **kws):
        Tkinter.Toplevel.__init__(self, *args, **kws)
        GenericWindow.__init__(self)

class Window(Tkinter.Tk, GenericWindow):
    def __init__(self, title='', bg='#ededed'):
        Tkinter.Tk.__init__(self)
        GenericWindow.__init__(self)
        self.caption = title
        self.config(
            bg=bg
        )

    def enable_escape(self):
        self.bind('<Escape>', lambda *args, **kws : self.destroy(), '+')