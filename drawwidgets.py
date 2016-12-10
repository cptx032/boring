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
            width=200, height=100, **kws):

        self.__close_btn_radius = kws.pop(
            'close_btn_radius', 10
        )
        self.__close_btn_padding = kws.pop(
            'close_btn_padding', 5
        )
        self.__close_btn_theme = kws.pop(
            'close_btn_theme', DEFAULT_CLOSE_BTN_THEME
        )
        self.__title = kws.pop(
            'title', ''
        )
        draw.RoundedRectangleDraw.__init__(
            self, master,
            [x, y, x+width, y+height],
            fill='#dbdbdb',
            **kws
        )

        drag.draggable(
            self,
            update=self.__update_close_btn
        )

        self.__close_btn = draw.OvalDraw(
            master,
            self.x+self.__close_btn_padding,
            self.y+self.__close_btn_padding,
            self.__close_btn_radius,
            self.__close_btn_radius,
            **DEFAULT_CLOSE_BTN_THEME
        )

        self.__title = draw.TextDraw(
            master,
            self.width/2,
            self.__close_btn_padding * 2,
            self.__title,
            anchor='center',
            fill='#888888'
        )

    def __update_close_btn(self, event):
        self.__close_btn.x = self.x+self.__close_btn_padding
        self.__close_btn.y = self.y+self.__close_btn_padding
        self.__close_btn.width = self.__close_btn_radius
        self.__close_btn.height = self.__close_btn_radius

        self.__title.x = self.x + self.width / 2
        self.__title.y = self.y + self.__close_btn_padding * 2