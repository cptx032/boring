# coding: utf-8
import copy
import sys
sys.path.extend(['..', '.', '../..'])

from boring.window import Window, tk
from boring.buttonthemes import SHADOWED_WHITE
from boring.widgets import Frame
from boring.button import SimpleButton

top = Window(title=u'Calc')
top.enable_escape()
top.resizable(0, 0)
top['bg'] = '#47565a'
top_frame = Frame(
    top, bg='#47565a').grid(row=0, column=0, padx=0, pady=0)
bottom_frame = Frame(top).grid(row=1, column=0)
entry = tk.Entry(
    top_frame,
    font=('arial', 20),
    bd=0, highlightthickness=0,
    bg='#47565a', fg='#ddd',
    justify='right')
entry.grid(pady=40, padx=20)
entry.insert(0, '3.1415')

buttons = [
    ['7', '8', '9', '/'],
    ['4', '5', '6', '*'],
    ['1', '2', '3', '-'],
    ['0', ',', '=', '+'],
]
numbers = [str(i) for i in range(10)]
DARK_THEME = copy.deepcopy(SHADOWED_WHITE)
DARK_THEME['shadow']['states']['normal']['normal']['fill'] = '#bbb'
DARK_THEME['shadow']['states']['normal']['over']['fill'] = '#aaa'
DARK_THEME['shadow']['states']['normal']['click']['fill'] = '#999'
DARK_THEME['shadow']['states']['normal']['normal']['radius'] = [0] * 4

frames = []
for i, line in enumerate(buttons):
    frame = Frame(bottom_frame).grid(row=i, column=0)
    frames.append(frame)
    column = 0
    for text in line:
        column += 1
        theme = SHADOWED_WHITE

        if text not in numbers:
            theme = DARK_THEME

        SimpleButton(
            frame,
            text=text,
            elems=theme,
            width=90, height=90).grid(
                row=0, column=column)

top.mainloop()
