def lerp(a, b, x):
    return a + ((b-a)*x)

METHODS = {
    'lerp': lerp
}

class Tween(object):
    def __init__(self, after, obj, **kws):
        self.__after = after
        self.__obj = obj
        self.__on_start = kws.pop('on_start', None)
        self.__on_end = kws.pop('on_end', None)
        self.__on_animation = kws.pop('on_animation', None)
        self.__effect = kws.pop('effect', None)

        self.__ticker = kws.pop('ticker', 100)
        self.__loop = kws.pop('loop', False)

        self.__method = kws.pop('method', 'lerp')

        self.__increase_factor = kws.pop('ifactor', 0.01)
        self.__lerp = 0.0

    def animate(self, _property, to, _from=None):
        if self.__lerp == 0.0 and self.__on_start:
            self.__on_start()
        ## DO ANIMATION
        if self.__lerp == 0.0 and _from != None:
            setattr(self.__obj, _property, _from)
        new_value = METHODS[self.__method](getattr(self.__obj, _property), to, self.__lerp)
        setattr(self.__obj, _property, new_value)
        ##
        self.__lerp += self.__increase_factor
        if (self.__lerp <= 1.0) or self.__loop:
            self.__after(self.__ticker, lambda : self.animate(_property, to, _from))
        if self.__lerp < 1.0 and self.__on_animation:
            self.__on_animation()
        if self.__lerp >= 1.0 and self.__on_end:
            self.__on_end()
        if self.__lerp >= 1.0 and self.__loop:
            self.__lerp = 0.0

# TODO: override + operator