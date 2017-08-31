# coding: utf-8

import copy
import draw
import packer

CHECK_MARK = u'\u2713'

CHECKBOX_DEFAULT_THEME = {
    'bg': {
        'def': {
            'class': draw.RoundedRectangleDraw,
            'x': 0,
            'y': 0,
            'width': 1.0,
            'height': 1.0
        },
        'states': {
            'checked': {
                'normal': {
                    'fill': '#5cb85c',
                    'width': 0,
                    'radius': [0] * 4,
                },
                'over': {
                    'fill': '#4ca84c',
                    'width': 0,
                    'radius': [0] * 4,
                },
                'click': {
                    'fill': '#3c983c',
                    'width': 0,
                    'radius': [0] * 4,
                }
            },
            'unchecked': {
                'normal': {
                    'fill': '#5cb85c',
                    'width': 0,
                    'radius': [0] * 4,
                },
                'over': {
                    'fill': '#4ca84c',
                    'width': 0,
                    'radius': [0] * 4,
                },
                'click': {
                    'fill': '#3c983c',
                    'width': 0,
                    'radius': [0] * 4,
                }
            },
            'disabled': {
                'normal': {
                    'fill': '#dedede',
                },
                'over': {
                    'fill': '#dcdcdc'
                },
                'click': {
                    'fill': '#dadada'
                }
            }
        }
    },
    'fg': {
        'def': {
            'class': draw.TextDraw,
            'x': 0.5,
            'y': 0.5,
            'anchor': 'center'
        },
        'states': {
            'checked': {
                'normal': {
                    'text': CHECK_MARK,
                    'fill': '#ffffff',
                    'font': ('helvetica', 12, 'bold'),
                },
                'over': {
                    'text': CHECK_MARK,
                },
                'click': {
                    'text': CHECK_MARK,
                }
            },
            'unchecked': {
                'normal': {
                    'text': '',
                    'fill': '#ffffff',
                    'font': ('helvetica', 12, 'bold'),
                },
                'over': {
                    'text': '',
                },
                'click': {
                    'text': '',
                }
            },
            'disabled': {
                'normal': {
                    'fill': '#aaa',
                },
                'over': {
                    'fill': '#aaa',
                },
                'click': {
                    'fill': '#aaa',
                },
            }
        }
    }
}


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
            kwargs['elems'] = copy.deepcopy(CHECKBOX_DEFAULT_THEME)
        StatePacker.__init__(self, *args, **kwargs)
        self.bind('<ButtonRelease-1>', self.check_handler, '+')
        self.bind('<Configure>', self.__update, '+')

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
    top.geometry('100x100')
    c = SimpleCheckbox(top).pack(side='left')
    c['state'] = 'disabled'
    c.check()
    SimpleCheckbox(top).pack(side='left')
    top.mainloop()
