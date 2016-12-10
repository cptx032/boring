# Boring

import sys
PYTHON_3 = sys.version_info.major == 3
if PYTHON_3:
    import tkinter as Tkinter
    from tkinter import font as tkFont
    from tkinter import colorchooser as tkColorChooser
else:
    import Tkinter
    import tkFont
    import tkColorChooser

BG_COLOR = '#ededed'

def center(widget):
    widget.update_idletasks()
    sw = int(widget.winfo_screenwidth())
    sh = int(widget.winfo_screenheight())
    ww = int(widget.winfo_width())
    wh = int(widget.winfo_height())
    xpos = (sw / 2) - (ww / 2)
    ypos = (sh / 2) - (wh / 2)
    widget.geometry('%dx%d+%d+%d' % (ww, wh, xpos, ypos))