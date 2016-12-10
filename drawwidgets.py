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
