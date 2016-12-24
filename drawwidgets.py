import draw
import drag

class CanvasGrid(object):
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.__x = x
        self.__y = y
        self.update()

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        self.__x = value
        self.update()

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, value):
        self.__y = value
        self.update()

    def __draw_grid(self):
        if (not self.x) or (not self.y):
            return
        for i in range(0, self.canvas.width, self.canvas.width / self.x):
            self.canvas.create_line(i, 0, i, self.canvas.height-1, fill='red',
                tag=('_-_grid-_-'), dash=(5,))
        for i in range(0, self.canvas.height, self.canvas.height / self.y):
            self.canvas.create_line(0, i, self.canvas.width-1, i, fill='red',
                tag=('_-_grid-_-'), dash=(5,))

    def update(self):
        self.canvas.delete('_-_grid-_-')
        self.__draw_grid()

DEFAULT_CLOSE_BTN_THEME = {
    'outline': '#bbbbbb',
    'fill': '#bbbbbb'
}

class DrawWindow(draw.RoundedRectangleDraw):
    def __init__(self, master, x=0, y=0,
            width=200, height=20,
            widget=None, **kws):

        self.__widget = widget

        # kws.update(fill=kws.get('fill', '#dbdbdb'))

        self.__close_btn_radius = kws.pop(
            'close_btn_radius', 10
        )
        self.__close_btn_padding = kws.pop(
            'close_btn_padding', 5
        )
        self.__close_btn_theme = kws.pop(
            'close_btn_theme',
            DEFAULT_CLOSE_BTN_THEME
        )
        self.__title = kws.pop(
            'title', ''
        )
        self.__close_function = kws.pop(
            'close_function',
            None
        )
        draw.RoundedRectangleDraw.__init__(
            self, master,
            [x, y, x+width, y+height],
            **kws
        )

        drag.draggable(
            self,
            update=lambda event: self.update()
        )

        self.__close_btn = draw.OvalDraw(
            master,
            self.x+self.__close_btn_padding,
            self.y+self.__close_btn_padding,
            self.__close_btn_radius,
            self.__close_btn_radius,
            **self.__close_btn_theme
        )
        if self.__close_function:
            self.__close_btn.bind('<1>', self.__close_function, '+')
        self.__close_btn.bind('<1>', lambda event: self.delete(), '+')

        self.__title = draw.TextDraw(
            master,
            self.width/2,
            self.__close_btn_padding * 2,
            self.__title,
            anchor='center',
            fill='#ddd'
        )

        if self.__widget:
            self.__widget_draw = draw.WidgetDraw(
                self.canvas, self.x, self.y+10,
                self.__widget, anchor='nw'
            )
            self.canvas.update_idletasks()
            self.adjust_size_widget()

    def update(self):
        draw.RoundedRectangleDraw.update(self)
        self.__close_btn.x = self.x+self.__close_btn_padding
        self.__close_btn.y = self.y+self.__close_btn_padding
        self.__close_btn.width = self.__close_btn_radius
        self.__close_btn.height = self.__close_btn_radius

        self.__title.x = self.x + self.width / 2
        self.__title.y = self.y + self.__close_btn_padding * 2

        if self.__widget:
            self.__widget_draw.x = self.x + 2
            self.__widget_draw.y = self.y + 20

    def adjust_size_widget(self):
        # forcar o widget a se adaptar ao tamahno da janela (e nao o contrario)
        # self.width = self.__widget.winfo_width() + 4
        # self.height = 22 + self.__widget.winfo_height()
        pass

    def delete(self):
        draw.RoundedRectangleDraw.delete(self)
        self.__close_btn.delete()
        self.__title.delete()
        if self.__widget:
            self.__widget_draw.delete()

    def center(self):
        self.x = (self.canvas.winfo_width() / 2) - (self.width / 2)
        self.y = (self.canvas.winfo_height() / 2) - (self.height / 2)
        self.update()

    @property
    def title(self):
        return self.__title.text

    @title.setter
    def title(self, value):
        self.__title.text = value

    def contract(self):
        pass

    def expand(self):
        pass

    @property
    def widget(self):
        return self.__widget