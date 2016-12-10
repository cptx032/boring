import draw
import widgets

DEFAULT_IOS_CHECKBUTTON_THEME = {
    'checked': {
        'bgcolor': '#6ede5f',
        'circlecolor': '#ffffff'
    },
    'unchecked': {
        'bgcolor': '#dbdbdb',
        'circlecolor': '#ffffff'
    }
}

class IOSCheckbox(widgets.ExtendedCanvas):
    def __init__(self, master,
        width=50, height=30, checked=False,
        theme=DEFAULT_IOS_CHECKBUTTON_THEME,
        circlepadding=-1):
        self.__theme = theme
        self.__checked = checked
        self.__circlepadding = circlepadding
        widgets.ExtendedCanvas.__init__(
            self, master,
            width=width, height=height,
            bd=0, highlightthickness=0,
            relief='flat',
            bg=master['bg']
        )
        radius = self.height / 2
        self.__bg = draw.RoundedRectangleDraw(
            self, [0, 0, self.width, self.height],
            fill=self.bgcolor, outline=self.bgcolor,
            radius=[radius]*4
        )
        self.__bg.style['width'] = 0
        self.__bg.update() # x, y, width, height, **kws

        self.__circle = draw.OvalDraw(
            self, self.__x(), self.__y(),
            self.__get_circle_height(), # width = height
            self.__get_circle_height(),
            fill=self.circlecolor,
            outline=self.circlecolor
        )
        self.__circle.style['width'] = 0
        self.__circle.update()

        self.checked = self.__checked # just for update

        self.__bg.bind('<1>', self.__click_handler, '+')
        self.__circle.bind('<1>', self.__click_handler, '+')

    def __click_handler(self, event):
        self.checked = not self.checked

    @property
    def checked(self):
        return self.__checked

    def update(self):
        widgets.ExtendedCanvas.update(self)
        self.__bg.width = self.width
        self.__bg.height = self.height

        self.__circle.width = self.__get_circle_height()
        self.__circle.height = self.__get_circle_height()

        self.checked = self.checked # just for update

    @checked.setter
    def checked(self, value):
        self.__checked = bool(value)
        self.__bg.style['fill'] = self.bgcolor
        self.__bg.style['outline'] = self.bgcolor
        self.__bg.update()
        self.__circle.style['fill'] = self.circlecolor
        self.__circle.style['outline'] = self.circlecolor
        self.__circle.x = self.__x()
        self.__circle.y = self.__y()

    @property
    def bgcolor(self):
        return self.__theme['checked' if self.checked else 'unchecked']['bgcolor']

    @property
    def circlecolor(self):
        return self.__theme['checked' if self.checked else 'unchecked']['circlecolor']

    def __x(self):
        '''
        returns the x coord of circle
        '''
        return self.width - self.__get_circle_height() - self.__circlepadding if self.checked else self.__circlepadding

    def __y(self):
        '''
        returns the y coord of circle
        '''
        return self.__circlepadding

    def __get_circle_height(self):
        return self.height-(self.__circlepadding*2)