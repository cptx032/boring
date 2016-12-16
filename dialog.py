from . import *
import widgets

class DefaultDialog(SubWindow):
    '''
    Class to open dialogs.
    This class is intended as a base class for custom dialogs
    '''
    def __init__(self, parent, title=None, show_in_start=True):
        '''
        Initialize a dialog.
        Arguments:
            parent -- a parent window (the application window)
            title -- the dialog title
        '''
        SubWindow.__init__(self, parent)
        self['bg'] = parent['bg']

        self.withdraw()
        # remain invisible for now
        # If the master is not viewable, don't
        # make the child transient, or else it
        # would be opened withdrawn
        if parent.winfo_viewable():
            self.transient(parent)

        if title:
            self.title(title)

        self.parent = parent
        self.resizable(0, 0)

        self.result = None

        body = widgets.Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5, expand='yes', fill='both')

        self.buttonbox()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.center()
        self.deiconify()  # become visibile now

        self.initial_focus.focus_set()

        if show_in_start:
            self.show()
        else:
            self.withdraw()

    def destroy(self):
        self.initial_focus = None
        SubWindow.destroy(self)

    def body(self, master):
        '''
        create dialog body.
        return widget that should have initial focus.
        This method should be overridden, and is called
        by the __init__ method.
        '''
        pass

    def show(self):
        # wait for window to appear on screen before calling grab_set
        self.wait_visibility()
        self.grab_set()
        self.wait_window(self)

    def buttonbox(self):
        '''
        add standard button box.
        override if you do not want the standard buttons
        '''
        box = widgets.Frame(self)

        w = widgets.Button(box, text="OK", command=self.ok, default='active')
        w.pack(side='left', padx=5, pady=5)
        w = widgets.Button(box, text="Cancel", command=self.cancel)
        w.pack(side='left', padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack(side='right')

    def ok(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set()
            return

        self.withdraw()
        self.update_idletasks()

        try:
            self.apply()
        finally:
            self.cancel()

    def cancel(self, event=None):
        # put focus back to the parent window
        if self.parent is not None:
            self.parent.focus_set()
        self.destroy()

    def validate(self):
        '''
        validate the data
        This method is called automatically to validate the data before the
        dialog is destroyed. By default, it always validates OK.
        '''
        return 1  # override

    def apply(self):
        '''
        process the data
        This method is called automatically to process the data, *after*
        the dialog is destroyed. By default, it does nothing.
        '''
        pass  # override

class MessageDialog(DefaultDialog):
    def __init__(self, master, title, message):
        self.__message = message
        DefaultDialog.__init__(self, master, title=title)

    def body(self, master):
        mdl = widgets.MarkDownLabel(master,
            height=1, width=len(self.__message) + 4,
            text=self.__message)
        mdl.centralize_text()
        mdl.pack(expand='yes', fill='both', padx=20, pady=20)
        return mdl

    def buttonbox(self):
        box = widgets.Frame(self)
        w = widgets.Button(box, text="OK", command=self.ok, default='active')
        w.pack(side='left', padx=5, pady=5)
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.ok)
        box.pack()

class MessageBox:
    @staticmethod
    def warning(**kws):
        MessageDialog(
            kws.get('parent'),
            kws.get('title', ''),
            kws.get('message')
        )

    @staticmethod
    def info(**kws):
        MessageDialog(
            kws.get('parent'),
            kws.get('title', ''),
            kws.get('message')
        )

class OkCancel(DefaultDialog):
    def __init__(self, parent, msg, title=None):
        self.msg = msg
        DefaultDialog.__init__(self, parent, title)

    def body(self, parent):
        self.output = False
        l = widgets.MarkDownLabel(
            parent,
            text=self.msg,
            width=len(self.msg) + 4
        )
        l.pack(padx=20, pady=20)
        return l

    def apply(self):
        self.output = True