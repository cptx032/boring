# coding: utf-8

import cbthemes
import copy
import packer


class SimpleCheckbox(packer.StatePacker):
    CHECKED_STATE = 'checked'
    UNCHECKED_STATE = 'unchecked'

    def __init__(self, *args, **kwargs):
        if 'state' not in kwargs:
            kwargs['state'] = SimpleCheckbox.UNCHECKED_STATE
        if 'width' not in kwargs:
            kwargs['width'] = 30
        if 'height' not in kwargs:
            kwargs['height'] = 30
        kwargs.update(
            bd=0, highlightthickness=0
        )
        if 'elems' not in kwargs:
            kwargs['elems'] = copy.deepcopy(cbthemes.SQUARE_WHITE_THEME)
        packer.StatePacker.__init__(self, *args, **kwargs)
        self.bind('<ButtonRelease-1>', self.check_handler, '+')
        self.bind('<Configure>', self.__update, '+')

        self.hide_bg()

    def __update(self, event=None):
        if self['state'] == 'disabled':
            self.switch_state('disabled')
            self.update_items('normal')

    def check(self):
        self.switch_state(SimpleCheckbox.CHECKED_STATE)

    def uncheck(self):
        self.switch_state(SimpleCheckbox.UNCHECKED_STATE)

    def is_checked(self):
        return self.actual_state == SimpleCheckbox.CHECKED_STATE

    def check_handler(self, event=None):
        if self['state'] == 'normal':
            if self.actual_state == SimpleCheckbox.CHECKED_STATE:
                self.switch_state(SimpleCheckbox.UNCHECKED_STATE)
            elif self.actual_state == SimpleCheckbox.UNCHECKED_STATE:
                self.switch_state(SimpleCheckbox.CHECKED_STATE)


if __name__ == '__main__':
    import window
    from widgets import Label, Frame
    top = window.Window(title='SimpleCheckbox')
    top.enable_escape()
    fr = Frame(top, bg='red').grid(pady=100, padx=100)
    Label(fr,
          font=('TkDefaultFont', 12),
          text='Checkbutton themes').grid(
        row=0, column=0, sticky='nw',
        pady=5, columnspan=2,
        padx=5)

    Label(fr,
          font=('TkDefaultFont', 10),
          text='Disabled check').grid(
        row=1, column=0, sticky='nw',
        pady=5,
        padx=5)

    c = SimpleCheckbox(fr).grid(
        row=2, column=0, pady=5, padx=5, sticky='nw')
    c['state'] = 'disabled'
    c.check()

    Label(fr,
          font=('TkDefaultFont', 10),
          text='White circle').grid(
        row=1, column=1, sticky='nw',
        pady=5,
        padx=5)
    SimpleCheckbox(fr).grid(
        row=2, column=1, pady=5, padx=5, sticky='nw').check()

    Label(fr,
          font=('TkDefaultFont', 10),
          text='Square green').grid(
        row=1, column=2, sticky='nw',
        pady=5,
        padx=5)
    SimpleCheckbox(
        fr,
        elems=cbthemes.SQUARE_GREEN_THEME
    ).grid(
        row=2, column=2, pady=5, padx=5, sticky='nw').check()
    Label(fr,
          font=('TkDefaultFont', 10),
          text='Big white').grid(
        row=1, column=3, sticky='nw',
        pady=5,
        padx=5)
    SimpleCheckbox(fr, elems=cbthemes.BIG_WHITE_THEME).grid(
        pady=5, padx=5, column=3, row=2, sticky='nw').check()
    top.mainloop()
