import math
import ImageTk

class BaseCanvasDraw(object):
    def __init__(self, canvas, coords, **kws):
        self.canvas = canvas
        self.coords = coords
        self.style = kws
        # override this to Canvas.create_something
        # self.draw_func = None
        self.__index = self.draw()

    def draw(self):
        return self.draw_func(*self.coords, **self.style)

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

    def reset(self):
        '''
        redraws and change the index
        '''
        self.delete()
        self.__index = self.draw()

class TextDraw(BaseCanvasDraw):
    def __init__(self, canvas, x, y, text, **kws):
        self.draw_func = canvas.create_text
        BaseCanvasDraw.__init__(self, canvas, [x, y], text=text, **kws)

    @property
    def text(self):
        return self.style['text']

    @text.setter
    def text(self, value):
        self.style['text'] = unicode(value)
        self.update()

class ImageDraw(BaseCanvasDraw):
    def __init__(self, canvas, x, y, image, **kws):
        '''
        image: can be string or ImageTk.PhotoImage instance
        '''
        self.draw_func = canvas.create_image
        BaseCanvasDraw.__init__(self, canvas,
            [x, y],
            image=ImageTk.PhotoImage(file=image) if type(image) in (str, unicode) else image, **kws)

    @property
    def image(self):
        return self.style['image']

    @image.setter
    def image(self, value):
        self.style['image'] = value
        self.update()

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
        self.draw_func = canvas.create_rectangle
        BaseCanvasDraw.__init__(self, canvas, [x, y, x + width, y + height], **kws)

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


class OvalDraw(RectangleDraw):
    def __init__(self, canvas, x, y, width, height, **kws):
        RectangleDraw.__init__(self, canvas, x, y, width, height, **kws)
        self.draw_func = canvas.create_oval
        self.reset()

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
        raise NotImplementedError


class PolygonDraw(BaseCanvasDraw):
    def __init__(self, canvas, coords, **kws):
        self.draw_func = canvas.create_polygon
        BaseCanvasDraw.__init__(self, canvas, coords, **kws)

class RoundedRectangleDraw(PolygonDraw):
    def __init__(self, canvas, coords, radius=[2, 2, 2, 2], **kws):
        self.__coords = coords
        self.radius = radius
        PolygonDraw.__init__(self, canvas, self.__coords, **kws)

    def get_circle_point(self, cx, cy, radius, angle):
        '''
        Returns the position of a vertex2D of a circle
        which center is in [cx,cy] position and radius 'radius'
        in the angle 'angle'
        '''
        # angle in degree
        angle = math.radians(angle)
        y = math.sin(angle) * radius
        x = math.cos(angle) * radius
        x += cx
        y = cy - y
        return [x, y]

    @property
    def coords(self):
        pts = []
        # NW
        if self.radius[0]:
            cx = self.__coords[0] + self.radius[0]
            cy = self.__coords[1] + self.radius[0]
            for i in range(90, 180):
                pts.extend(self.get_circle_point(cx,cy,
                    self.radius[0], i))
        else:
            pts.extend([self.__coords[0], self.__coords[1]])
        # SW
        if self.radius[1]:
            cx = self.__coords[0] + self.radius[1]
            cy = self.__coords[3] - self.radius[1]
            for i in range(180, 270):
                pts.extend(self.get_circle_point(cx, cy,
                    self.radius[1], i))
        else:
            pts.extend([self.__coords[0], self.__coords[3]])

        # SE
        if self.radius[2]:
            cx = self.__coords[2] - self.radius[2]
            cy = self.__coords[3] - self.radius[2]
            for i in range(270, 360):
                pts.extend(self.get_circle_point(cx,cy,
                    self.radius[2],i))
        else:
            pts.extend([self.__coords[2],
                self.__coords[3]])
        # NE
        if self.radius[3]:
            cx = self.__coords[2] - self.radius[3]
            cy = self.__coords[1] + self.radius[3]
            for i in range(0, 90):
                pts.extend(self.get_circle_point(cx,cy,
                    self.radius[3],i))
        else:
            pts.extend([self.__coords[2],
                self.__coords[1]])
        return pts

    @coords.setter
    def coords(self, value):
        self.__coords = value

    @property
    def width(self):
        raise NotImplementedError # TODO

    @width.setter
    def width(self, value):
        raise NotImplementedError

    @property
    def height(self):
        raise NotImplementedError

    @height.setter
    def height(self, value):
        raise NotImplementedError