import Tkinter # TODO python 3
import ios

top = Tkinter.Tk()
top['bg'] = '#ededed'
ioscheck = ios.IOSCheckbox(top)
ioscheck.grid(pady=100, padx=100)
top.mainloop()