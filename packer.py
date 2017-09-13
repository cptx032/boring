# coding: utf-8
import widgets
import uuid


class Packer(widgets.ExtendedCanvas):
    u"""Classe que permite isso e aquilo."""

    def __init__(self, *args, **kwargs):
        self.items = dict()
        self.update_on_resize = kwargs.pop('update_on_resize', False)
        widgets.ExtendedCanvas.__init__(self, *args, **kwargs)
        self.bind('<Configure>', lambda e: self.update_items('normal'), '+')
        self.bind('<Button-1>', lambda e: self.update_items('click'), '+')
        self.bind(
            '<ButtonRelease-1>',
            lambda e: self.update_items('over'),
            '+'
        )
        self.bind('<Enter>', lambda e: self.update_items('over'), '+')
        self.bind('<Leave>', lambda e: self.update_items('normal'), '+')
        self.bind('<Motion>', lambda e: self.update_items('over'), '+')
        self.bind('<B1-Motion>', lambda e: self.update_items('click'), '+')

    def update_items(self, theme_state):
        # if self.update_on_resize:
        for name in self.items:
            draw = self.items.get(name).get('draw')
            draw.coords = self.get_draw_coords(
                self.items.get(name).get('settings')
            )
            # configure call update
            draw.configure(
                **self.items.get(name).get('settings').get('theme', {}).get(
                    theme_state, {}))

    def get_draw_coords(self, item):
        u""""Return the 'args' part of draw object's constructor."""
        coords = [
            self.width * item.get('x'),
            self.height * item.get('y')
        ]
        if item.get('width'):
            coords.append(self.width * item.get('width'))
            coords.append(self.height * item.get('height'))
        return coords

    def add_item(self, item):
        draw = item.get('class')(
            self,
            *self.get_draw_coords(item),
            **item.get('theme').get('normal', {})
        )
        name = item.get('name', uuid.uuid4().hex.upper())
        self.items[name] = {
            'draw': draw,
            'settings': item
        }
        self.update_items('normal')
        return self.items[name]

    def add_items(self, items):
        _items = []
        for item in items:
            _items.append(self.add_item(items))
        return _items


class StatePacker(Packer):
    def __init__(self, *args, **kwargs):
        self.actual_state = kwargs.pop('state')
        self.elems = kwargs.pop('elems')
        Packer.__init__(self, *args, **kwargs)
        self.__init_states()

    def __init_states(self):
        for key in self.elems.keys():
            definition = self.elems.get(key).get('def')
            definition['name'] = key
            definition['theme'] = self.elems.get(key).get(
                'states').get(self.actual_state)
            self.add_item(definition)

    def switch_state(self, state):
        self.actual_state = state
        for key in self.items.keys():
            self.items[key]['settings']['theme'] = self.elems.get(
                key).get('states').get(self.actual_state)
        self.update_items('over')

    def change_elems(self, elems, state=None):
        self.elems = elems
        if state:
            self.actual_state = state
        self.switch_state(self.actual_state)

if __name__ == '__main__':
    import draw
    import window
    import widgets
    top = window.Window('Packer')
    widgets.Label(
        top,
        text='Resize window to see draw change your size automagically').pack()
    top.enable_escape()
    packer = Packer(
        top,
        width=100,
        height=100).pack(
            expand='yes',
            fill='both')
    packer.add_item({
        'class': draw.RectangleDraw,
        'theme': {
            'normal': {
                'fill': '#eee',
                'outline': '#eee'
            }
        },
        'x': 0.75,
        'width': 0.2,
        'y': 0.25,
        'height': 0.5
    })
    top.mainloop()
