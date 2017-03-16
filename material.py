from widgets import ExtendedCanvas
import draw
import window
from window import BG_COLOR

def format_color(c):
    return min(max(c, 0), 255)

def darken_color(color, offset=-20):
    color = color.replace('#', '')
    r,g,b = [None]*3
    if len(color) == 3:
        r, g, b = [int(i, 16)+offset for i in color]
    elif len(color) == 6:
        r, g, b = [int(i, 16)+offset for i in [color[:2], color[2:4], color[4:6]]]
    else:
        raise ValueError(u'Wrong color format %s' % (color))
    r, g, b = [format_color(i) for i in [r, g, b]]
    return '#%02x%02x%02x' % (r, g, b)

class RaisedButton(ExtendedCanvas):
    def __init__(self, *args, **kwargs):
        _wi, _he = kwargs.pop('width', 100), kwargs.pop('height', 25)
        self.radius = kwargs.pop('radius', [2, 2, 2, 2])
        self.level = 1
        self.__bg_color = kwargs.pop('bgcolor', BG_COLOR)
        self.__font = kwargs.pop('font', ('TkDefaultFont', 10))
        self.__bottom_offset = kwargs.pop('bottomoffset', 5)
        _fg_color = kwargs.pop('fgcolor', 'black')

        _text = kwargs.pop('text', '')
        self.command = kwargs.pop('command', None)

        kwargs.update(width=_wi, height=_he, bg=BG_COLOR)
        kwargs.update(cursor='hand1')
        ExtendedCanvas.__init__(self, *args, **kwargs)
        self.update_idletasks()

        self.__shadow = draw.RoundedRectangleDraw(
            self, [0,0,self.width, self.height],
            radius=self.radius, fill=darken_color(self.__bg_color),
            outline=darken_color(self.__bg_color)
        )

        self.__bg = draw.RoundedRectangleDraw(
            self, [0, 0, self.width, self.height-self.__bottom_offset],
            radius=self.radius, fill=self.__bg_color,
            outline=self.__bg_color,
            width=0
        )

        self.__text = draw.TextDraw(
            self,
            self.width / 2,
            self.height / 2,
            _text,
            fill=_fg_color,
            font=self.__font
        )

        self.__bind_command(self.command)

        self.config(bg=self.master['bg'],
            relief='flat', bd=0,
            highlightthickness=0)

    def __bind_command(self, cmd):
        if not cmd:
            return
        self.bind('<1>', lambda *args : cmd(), '+')

    @property
    def text(self):
        return self.__text.text

    @text.setter
    def text(self, value):
        self.__text.text = value

    @property
    def fgcolor(self):
        return self.__text.style['fill']

    @fgcolor.setter
    def fgcolor(self, value):
        self.__text.fill = value

    @property
    def bgcolor(self):
        return self.__bg.style['fill']

    @bgcolor.setter
    def bgcolor(self, value):
        self.__bg.fill = value
        self.__shadow.fill = darken_color(value)

    @property
    def font(self):
        return self.__text.font

    @font.setter
    def font(self, value):
        self.__text.font = value

    def update(self):
        ExtendedCanvas.update(self)
        self.__bg.width = self.width
        self.__bg.height = self.height
        self.__text.xy = [self.width/2, self.height/2]


if __name__ == '__main__':
    top = window.Window(bg='#ffffff')
    top.enable_escape()
    RaisedButton(
        top,
        text='Create project',
        bgcolor='#3498db',
        fgcolor='white',
        width=150,
        height=40).grid(pady=5, padx=5, row=0, column=0)
    r = RaisedButton(
        top,
        text='Do something',
        bgcolor='#ecf0f1',
        fgcolor='#888',
        width=150,
        height=40)
    r.bgcolor = '#990000'
    r.grid(pady=5, padx=5, row=0, column=1)
    top.mainloop()