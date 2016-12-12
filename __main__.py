import Tkinter # TODO python 3
import drawwidgets
import widgets

top = Tkinter.Tk()
top.attributes('-zoomed', 1)
top['bg'] = '#ededed'
ca = widgets.ExtendedCanvas(
	top, bg='#ededed'
)
ca.pack(expand='yes', fill='both')
v = drawwidgets.DrawWindow(
	ca,
	radius=[10]*4,
	title='sensor'
)

drawwidgets.DrawWindow(
	ca,
	radius=[10]*4,
	title='sensor 1'
)
top.mainloop()