class Tween(object):
	def __init__(self, obj, **kws):
		self.__obj = obj
		self.__on_start = kws.pop('on_start', None)
		self.__on_end = kws.pop('on_end', None)
		self.__on_animation = kws.pop('on_animation', None)
		self.__effect = kws.pop('effect', None)
		self.__ticker = kws.pop('ticker', 100)