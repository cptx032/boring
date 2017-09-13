# coding: utf-8
import copy
import packer
import buttonthemes


# states needed: active, normal, disabled
# elem needed: text
class SimpleButton(packer.StatePacker):
    def __init__(self, *args, **kwargs):
        if 'state' not in kwargs:
            kwargs['state'] = 'normal'
        if 'width' not in kwargs:
            kwargs['width'] = 100
        if 'height' not in kwargs:
            kwargs['height'] = 40
        kwargs.update(
            bd=0, highlightthickness=0
        )

        text = kwargs.pop('text', '')
        if 'elems' not in kwargs:
            kwargs['elems'] = copy.deepcopy(buttonthemes.SHADOWED_WHITE)
        packer.StatePacker.__init__(self, *args, **kwargs)
        self.set_text(text)

    def set_text(self, text):
        self.items.get('text').get('draw').text = text

if __name__ == '__main__':
    import window
    from widgets import Label, Frame
    top = window.Window(title=u'Button')
    top.enable_escape()

    fr = Frame(top, bg='red').grid(pady=100, padx=100)
    Label(fr,
          font=('TkDefaultFont', 12),
          text='Button themes').grid(
        row=0, column=0, sticky='nw',
        pady=5, columnspan=2,
        padx=5)
    SimpleButton(fr, text='ok', state='active').grid(
        pady=5, padx=5, row=2, column=0)
    SimpleButton(fr, text='ok').grid(
        pady=5, padx=5, row=2, column=1)
    top.mainloop()
