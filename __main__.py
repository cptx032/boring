import Tkinter # TODO python 3
import ios
import drawwidgets
import widgets

top = Tkinter.Tk()
top['bg'] = '#ededed'
ioscheck = ios.IOSCheckbox(top)
ioscheck.grid(pady=100, padx=100)

ca = widgets.ExtendedCanvas(top, bg='#ededed')
ca.grid()
v = drawwidgets.DrawWindow(ca, radius=[10]*4, title='keyboard')
top.mainloop()