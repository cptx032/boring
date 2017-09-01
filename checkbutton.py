# coding: utf-8

import cbthemes
import copy
import packer


class StatePacker(packer.Packer):
    def __init__(self, *args, **kwargs):
        self.actual_state = kwargs.pop('state')
        self.elems = kwargs.pop('elems')
        packer.Packer.__init__(self, *args, **kwargs)
        self.__init_states()

    def __init_states(self):
        for key in self.elems:
            definition = self.elems.get(key).get('def')
            definition['name'] = key
            definition['theme'] = self.elems.get(key).get(
                'states').get(self.actual_state)
            self.add_item(definition)

    def switch_state(self, state):
        self.actual_state = state
        for key in self.items:
            self.items[key]['settings']['theme'] = self.elems.get(
                key).get('states').get(self.actual_state)
        self.update_items('over')


class SimpleCheckbox(StatePacker):
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
        StatePacker.__init__(self, *args, **kwargs)
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
    top = window.Window(title='SimpleCheckbox')
    top.enable_escape()
    top.geometry('200x100')
    c = SimpleCheckbox(top).pack(side='left', pady=5, padx=5)
    c['state'] = 'disabled'
    c.check()
    SimpleCheckbox(top).pack(side='left', pady=5, padx=5)
    SimpleCheckbox(top, elems=cbthemes.SQUARE_GREEN_THEME).pack(
        side='left', pady=5, padx=5)
    SimpleCheckbox(top, elems=cbthemes.CIRCLE_WHITE_THEME).pack(
        side='left', pady=5, padx=5)
    top.mainloop()
