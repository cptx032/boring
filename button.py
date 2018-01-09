# coding: utf-8
import copy
from boring import packer
from boring import buttonthemes
from boring.widgets import Frame


# states needed: active, normal, disabled
# elem needed: text
class SimpleButton(packer.StatePacker):
    def __init__(self, *args, **kwargs):
        if 'state' not in kwargs:
            kwargs['state'] = 'normal'
        if 'width' not in kwargs:
            kwargs['width'] = 100
        if 'height' not in kwargs:
            kwargs['height'] = 25
        kwargs.update(
            bd=0, highlightthickness=0
        )

        text = kwargs.pop('text', '')
        if 'elems' not in kwargs:
            kwargs['elems'] = copy.deepcopy(buttonthemes.SHADOWED_WHITE)
        packer.StatePacker.__init__(self, *args, **kwargs)
        self.set_text(text)

    def set_text(self, text):
        self.items.get('text').get('draw').text = text

    def get_text(self):
        return self.items.get('text').get('draw').text


class RadioButton(Frame):
    def __init__(self, *args, **kwargs):
        self.__options = kwargs.pop('options')
        self.__button_class = kwargs.pop('button_class', SimpleButton)
        self.__orient = kwargs.pop('orient', 'horizontal')
        self.__buttons = list()
        self.__grid_options = kwargs.pop(
            'grid_optiosn', {'pady': 5, 'padx': 5})
        self.after_change = kwargs.pop('after_change', None)
        self.unselectable = kwargs.pop('unselectable', False)
        super(RadioButton, self).__init__(*args, **kwargs)
        self.__create_buttons()
        self.__grid_buttons()

    def unselect(self):
        if self.unselectable:
            for i in self.__buttons:
                if i.actual_state == 'active':
                    i.switch_state('normal')
                    break
        else:
            raise ValueError('This RadioButton cant be unselected')

    def get_option(self):
        for i in self.__buttons:
            if i.actual_state == 'active':
                return i.get_text()

    def __grid_buttons(self):
        count = 0
        for i, btn in enumerate(self.__buttons):
            if self.__orient == 'horizontal':
                btn.grid(row=0, column=count, **self.__grid_options)
            elif self.__orient == 'vertical':
                btn.grid(row=count, column=0, **self.__grid_options)
            count += 1

    def __gen_radio_button_handler(self, btn):
        def handler(event=None):
            old_option = self.get_option()
            for i in self.__buttons:
                if i == btn:
                    i.switch_state('active')
                else:
                    i.switch_state('normal')
            if self.after_change and old_option != self.get_option():
                self.after_change(old_option, self.get_option())
            if old_option == self.get_option() and self.unselectable:
                self.unselect()
        return handler

    def __create_buttons(self):
        for i in self.__options:
            btn = self.__button_class(self, text=i)
            btn.bind('<1>', self.__gen_radio_button_handler(btn), '+')
            self.__buttons.append(btn)


if __name__ == '__main__':
    import window
    from widgets import Label, Frame
    top = window.Window(title=u'Button')
    top.enable_escape()

    fr = Frame(top, bg='red').grid(pady=100, padx=100)
    Label(fr,
          font=('TkDefaultFont', 12),
          text='Button themes').grid(
        row=0, column=0, sticky='nw',
        pady=5, columnspan=2,
        padx=5)
    SimpleButton(fr, text='ok', state='active').grid(
        pady=5, padx=5, row=2, column=0)
    SimpleButton(fr, text='ok').grid(
        pady=5, padx=5, row=2, column=1)
    top.mainloop()
