import math
import ImageTk

class BaseCanvasDraw(object):
    def __init__(self, canvas, coords, **kws):
        self.canvas = canvas
        self.coords = coords
        self.style = kws
        # override this to Canvas.create_something
        # self.draw_func = None
        self.__index = self.generate_canvas_index()(*self.coords, **self.style)

    def generate_canvas_index(self):
        return self.get_drawing_function()

    def get_drawing_function(self):
        raise NotImplementedError

    def update(self):
        self.canvas.coords(self.__index, *self.coords)
        self.canvas.itemconfig(self.__index, **self.style)

    def delete(self):
        self.canvas.delete(self.__index)

    def bind(self, *args, **kws):
        self.canvas.tag_bind(self.__index, *args, **kws)

    def up(self):
        self.canvas.tag_raise(self.__index)

    def down(self):
        self.canvas.tag_lower(self.__index)

    def scroll(self, x, y):
        '''
        increments decrements the components
        '''
        for i in range(0, len(self.coords), 2):
            self.coords[i] += x
            self.coords[i+1] += y
        self.update()

    def reset(self):
        '''
        redraws and change the index
        '''
        self.delete()
        self.__index = self.generate_canvas_index()(*self.coords, **self.style)

    def configure(self, **kws):
        self.style.update(**kws)
        self.update()


class LineDraw(BaseCanvasDraw):
    def __init__(self, canvas, x1, y1, x2, y2, **kws):
        BaseCanvasDraw.__init__(
            self,
            canvas, [x1, y1, x2, y2],
            **kws
        )

    def get_drawing_function(self):
        return self.canvas.create_line

    @property
    def p1(self):
        return self.coords[:2]

    @p1.setter
    def p1(self, value):
        self.coords[0] = value[0]
        self.coords[1] = value[1]
        self.update()

    @property
    def p2(self):
        return self.coords[2:]

    @p2.setter
    def p2(self, value):
        self.coords[2] = value[0]
        self.coords[3] = value[1]
        self.update()


class ArcDraw(BaseCanvasDraw):
    def __init__(self, canvas, coords, **kws):
        BaseCanvasDraw.__init__(self, canvas, coords, **kws)

    def get_drawing_function(self):
        return self.canvas.create_arc

    @property
    def x(self):
        return self.coords[0]

    @x.setter
    def x(self, value):
        self.coords[0] = value
        self.update()

    @property
    def y(self):
        return self.coords[1]

    @y.setter
    def y(self, value):
        self.coords[1] = value
        self.update()

    @property
    def xy(self):
        return self.coords[:2]

    @xy.setter
    def xy(self, value):
        self.coords[0] = value[0]
        self.coords[1] = value[1]
        self.update()

    @property
    def width(self):
        return self.coords[2] - self.coords[0]

    @width.setter
    def width(self, value):
        self.coords[2] = self.coords[0] + value
        self.update()

    @property
    def height(self):
        return self.coords[3] - self.coords[1]

    @height.setter
    def height(self, value):
        self.coords[3] = self.coords[1] + value
        self.update()

    @property
    def arcstyle(self):
        return self.style.get('style')

    @arcstyle.setter
    def arcstyle(self, value):
        # if value not in ('arc', 'chord', '')
        self.configure(style=value)

    @property
    def arcwidth(self):
        return self.style.get('width')

    @arcwidth.setter
    def arcwidth(self, value):
        self.configure(width=value)

    @property
    def startangle(self):
        return self.style.get('start')

    @startangle.setter
    def startangle(self, value):
        self.configure(start=value)

    @property
    def endangle(self):
        return self.style.get('extent')

    @endangle.setter
    def endangle(self, value):
        self.configure(extent=value)

    @property
    def fill(self):
        return self.style.get('fill')

    @fill.setter
    def fill(self, value):
        self.configure(fill=value)

    @property
    def outline(self):
        return self.style.get('outline')

    @outline.setter
    def outline(self, value):
        self.configure(outline=value)


class SimpleCurveDraw(BaseCanvasDraw):
    pass # TODO

class TextDraw(BaseCanvasDraw):
    def __init__(self, canvas, x, y, **kws):
        BaseCanvasDraw.__init__(self, canvas, [x, y], **kws)

    def get_drawing_function(self):
        return self.canvas.create_text

    @property
    def text(self):
        return self.style['text']

    @text.setter
    def text(self, value):
        self.configure(text=unicode(value))

    @property
    def x(self):
        return self.coords[0]

    @x.setter
    def x(self, value):
        self.coords[0] = value
        self.update()

    @property
    def y(self):
        return self.coords[1]

    @y.setter
    def y(self, value):
        self.coords[1] = value
        self.update()

    @property
    def xy(self):
        return self.coords

    @xy.setter
    def xy(self, value):
        self.coords = value
        self.update()

    @property
    def fill(self):
        return self.style['fill']

    @fill.setter
    def fill(self, value):
        self.configure(fill=value)

    @property
    def font(self):
        return self.style['font']

    @font.setter
    def font(self, value):
        self.configure(font=value)


class WidgetDraw(BaseCanvasDraw):
    def __init__(self, canvas, x, y, widget, **kws):
        BaseCanvasDraw.__init__(
            self,
            canvas,
            [x, y],
            window=widget,
            **kws
        )

    def get_drawing_function(self):
        return self.canvas.create_window

    @property
    def x(self):
        return self.coords[0]

    @x.setter
    def x(self, value):
        self.coords[0] = value
        self.update()

    @property
    def y(self):
        return self.coords[1]

    @y.setter
    def y(self, value):
        self.coords[1] = value
        self.update()

    @property
    def widget(self):
        return self.style['window']

    @widget.setter
    def widget(self, value):
        self.configure(window=value)


class ImageDraw(BaseCanvasDraw):
    def __init__(self, canvas, x, y, image, **kws):
        '''
        image: can be string or ImageTk.PhotoImage instance
        '''
        # fixme: verify types
        BaseCanvasDraw.__init__(
            self, canvas,
            [x, y],
            image=ImageTk.PhotoImage(file=image) if type(image) in (str, unicode) else image, **kws)

    def get_drawing_function(self):
        return self.canvas.create_image

    @property
    def image(self):
        return self.style['image']

    @image.setter
    def image(self, value):
        self.configure(image=value)

    @property
    def x(self):
        return self.coords[0]

    @x.setter
    def x(self, value):
        self.coords = [value, self.y]
        self.update()

    @property
    def y(self):
        return self.coords[1]

    @y.setter
    def y(self, value):
        self.coords = [self.x, value]
        self.update()

    @property
    def width(self):
        return self.style.get('image').width()

    @width.setter
    def width(self, value):
        # does nothing
        self.update()

    @property
    def height(self):
        return self.style.get('image').height()

    @height.setter
    def height(self, value):
        # does nothing
        self.update()


class RectangleDraw(BaseCanvasDraw):
    def __init__(self, canvas, x, y, width, height, **kws):
        self.__coords = [x, y, x + width, y + height]
        BaseCanvasDraw.__init__(self, canvas, self.__coords, **kws)

    def get_drawing_function(self):
        return self.canvas.create_rectangle

    @property
    def coords(self):
        return self.__coords

    @coords.setter
    def coords(self, coords):
        self.__coords = [
            coords[0], coords[1],
            coords[0] + coords[2],
            coords[1] + coords[3]
        ]

    @property
    def x(self):
        return self.coords[0]

    @x.setter
    def x(self, value):
        self.coords = [value, self.y, value+self.width, self.y+self.height]
        self.update()

    @property
    def y(self):
        return self.coords[1]

    @y.setter
    def y(self, value):
        self.coords = [self.x, value, self.x+self.width, value+self.height]
        self.update()

    @property
    def width(self):
        return self.coords[2] - self.coords[0]

    @width.setter
    def width(self, value):
        self.coords = [self.x, self.y, self.x+value, self.y+self.height]
        self.update()

    @property
    def height(self):
        return self.coords[3] - self.coords[1]

    @height.setter
    def height(self, value):
        self.coords = [self.x, self.y, self.x + self.width, self.y + value]
        self.update()

    def is_inside(self, x, y):
        '''
        returns true if a point(x, y)
        is inside oval
        '''
        in_x = (x >= self.x) and (x <= (self.x + self.width))
        in_y = (y >= self.y) and (y <= (self.y  +self.height))
        return in_x and in_y


class OvalDraw(RectangleDraw):

    def get_drawing_function(self):
        return self.create_oval

    @property
    def radius(self):
        if self.width == self.height:
            return self.width / 2
        raise Exception('Oval is not a circle')

    @radius.setter
    def radius(self, value):
        self.width = value
        self.height = value

    # TODO: implements to set the center
    @property
    def center_x(self):
        return self.x + (self.width/2)

    @property
    def center_y(self):
        return self.y + (self.height / 2)

    # def is_inside(self, x, y):
    #     '''
    #     returns true if a point(x, y)
    #     is inside oval
    #     '''
    #     # rectangle mode: TODO: radius mode
    #     return NotImplementedError


class PolygonDraw(BaseCanvasDraw):
    def __init__(self, canvas, *coords, **kws):
        BaseCanvasDraw.__init__(self, canvas, coords, **kws)

    def get_drawing_function(self):
        return self.canvas.create_polygon

    @property
    def fill(self):
        return self.style['fill']

    @fill.setter
    def fill(self, value):
        self.configure(fill=value)


class RoundedRectangleDraw(PolygonDraw):
    def __init__(self, canvas, x, y, _width, height, radius=[2, 2, 2, 2], **kws):
        self.__coords = [x, y, x + _width, y + height]
        self.__radius = radius
        PolygonDraw.__init__(self, canvas, *self.__coords, **kws)

    @property
    def radius(self):
        return self.__radius

    @radius.setter
    def radius(self, value):
        self.__radius = value
        self.update()

    # override
    def scroll(self, x, y):
        self.x += x
        self.y += y

    @property
    def coords(self):
        pts = []
        # NW
        if self.radius[0]:
            cx = self.__coords[0] + self.radius[0]
            cy = self.__coords[1] + self.radius[0]
            for i in range(90, 180):
                pts.extend(self.canvas.get_circle_point(cx,cy,
                    self.radius[0], i))
        else:
            pts.extend([self.__coords[0], self.__coords[1]])
        # SW
        if self.radius[1]:
            cx = self.__coords[0] + self.radius[1]
            cy = self.__coords[3] - self.radius[1]
            for i in range(180, 270):
                pts.extend(self.canvas.get_circle_point(cx, cy,
                    self.radius[1], i))
        else:
            pts.extend([self.__coords[0], self.__coords[3]])

        # SE
        if self.radius[2]:
            cx = self.__coords[2] - self.radius[2]
            cy = self.__coords[3] - self.radius[2]
            for i in range(270, 360):
                pts.extend(self.canvas.get_circle_point(cx,cy,
                    self.radius[2],i))
        else:
            pts.extend([self.__coords[2],
                self.__coords[3]])
        # NE
        if self.radius[3]:
            cx = self.__coords[2] - self.radius[3]
            cy = self.__coords[1] + self.radius[3]
            for i in range(0, 90):
                pts.extend(self.canvas.get_circle_point(cx,cy,
                    self.radius[3],i))
        else:
            pts.extend([self.__coords[2],
                self.__coords[1]])
        return pts

    @coords.setter
    def coords(self, value):
        self.__coords = [
            value[0], value[1],
            value[0] + value[2],
            value[1] + value[3]
        ]
        # self.update()

    @property
    def x(self):
        return self.__coords[0]

    @property
    def y(self):
        return self.__coords[1]

    @property
    def width(self):
        return self.__coords[2] - self.__coords[0]

    @property
    def height(self):
        return self.__coords[3] - self.__coords[1]

    @x.setter
    def x(self, value):
        width = self.width
        self.__coords[0] = value
        self.__coords[2] = value + width
        self.update()

    @y.setter
    def y(self, value):
        height = self.height
        self.__coords[1] = value
        self.__coords[3] = value + height
        self.update()

    @width.setter
    def width(self, value):
        self.__coords[2] = self.__coords[0] + value
        self.update()

    @height.setter
    def height(self, value):
        self.__coords[3] = self.__coords[1] + value
        self.update()

    @property
    def fill(self):
        return self.style['fill']

    @fill.setter
    def fill(self, value):
        self.configure(fill=value)

    @property
    def outline(self):
        return self.style['outline']

    @outline.setter
    def outline(self, value):
        self.configure(outline=value)

    def configure(self, **kws):
        if 'radius' in kws:
            self.radius = kws.pop('radius')
        PolygonDraw.configure(self, **kws)

if __name__ == '__main__':
    import window, widgets
    top = window.Window()
    ca = widgets.ExtendedCanvas(top)
    ca.grid()
    v = ArcDraw(ca, [10,10,110,110])
    v.arcwidth = 2
    v.arcstyle = 'arc'
    v.outline = '#00aacc'
    v.startangle = 0
    v.endangle = 180
    def _T(*Args):
        v.startangle += 20
        # print 'pass heres'
    ca.bind('<Up>', _T, '+')
    ca.focus_force()
    top.mainloop()