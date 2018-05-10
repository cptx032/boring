# coding: utf-8

import collections
import copy

from boring import packer
from boring import widgets
from boring import tabthemes


class SimpleTabButton(packer.StatePacker):
    ACTIVE_STATE = 'active'
    NORMAL_STATE = 'normal'
    DISABLED = 'disabled'

    def __init__(self, *args, **kwargs):
        # as opções são: text, icon
        _text = kwargs.pop('text', u'')
        _icon = kwargs.pop('icon', None)

        kwargs.setdefault('cursor', 'hand1')
        kwargs.setdefault('highlightthickness', 0)
        kwargs.setdefault('bd', 0)
        kwargs.setdefault('width', 100)
        kwargs.setdefault('height', 40)
        kwargs.setdefault('state', 'normal')
        kwargs.setdefault('elems', copy.deepcopy(tabthemes.LIGHT_THEME))

        packer.StatePacker.__init__(self, *args, **kwargs)
        self.set_text(_text)
        self.set_icon(_icon)

    def set_text(self, text):
        self.items.get('text').get('draw').text = text

    def get_text(self):
        return self.items.get('text').get('draw').text

    def set_icon(self, icon):
        self.items.get('icon').get('draw').image = icon

    def get_icon(self):
        return self.items.get('icon').get('draw').image


class Tab(widgets.Frame):
    VERTICAL = 'vertical'
    HORIZONTAL = 'horizontal'

    def __init__(self, master, **kwargs):
        self.__orientation = kwargs.pop('orientation', Tab.HORIZONTAL)
        # the class of tab button
        self.tab_button_class = kwargs.pop('tab_button_class', SimpleTabButton)
        widgets.Frame.__init__(self, master)

        # the frame where is placed all tab buttons
        self.__tabs_frame = widgets.Frame(self)
        # the frame where is placed the content of each tab
        self.__content_frame = widgets.Frame(self)

        # <name>: <widget>
        self.tabs = collections.OrderedDict()

        self.set_orientation(self.get_orientation())

    def add_tab(self, name, content_func, **kwargs):
        u"""Add a new tab.

        Params:
            name: the ID of tab. Can be anything but is preferable that
                it be a string
            content_func: a function that returns only one widget to be
                showed when user active a tab
            view_tab: a boolean indicating if that tab that is being added
                should be active or not. This option will be ignored if tab
                container hasnt any tab (is this case that tab will be
                activated).
        """
        _view_tab = kwargs.pop('view_tab', False)
        tabbutton = self.tab_button_class(self.__tabs_frame, **kwargs)
        tabbutton.bind(
            '<ButtonRelease-1>',
            lambda evt: self.__view_tab_handler(evt, name),
            '+')
        content_frame = widgets.Frame(self.__content_frame)
        content = content_func(content_frame)
        self.tabs[name] = dict(
            name=name,
            tabbutton=tabbutton,
            content_frame=content_frame,
            content=content)

        kw = dict(sticky='nw')
        if self.get_orientation() == Tab.HORIZONTAL:
            kw['row'] = 0
            kw['column'] = len(self.tabs.keys())
        elif self.get_orientation() == Tab.VERTICAL:
            kw['row'] = len(self.tabs.keys())
            kw['column'] = 0
        tabbutton.grid(**kw)

        # if is the first tag being added
        if len(self.tabs) == 1 or _view_tab:
            self.view_tab(name)

    def __view_tab_handler(self, event, name):
        u"""Called when the tabbutton is clicked."""
        self.view_tab(name)

    def view_tab(self, name):
        u"""Switch to a tab.

        Params:
            name: the ID of tab
        """
        for i in self.tabs:
            if self.tabs[i]['tabbutton'].actual_state == 'active':
                self.tabs[i]['tabbutton'].switch_state('normal')
                self.tabs[i]['tabbutton'].update_items('normal')
                self.tabs[i]['content_frame'].pack_forget()
        self.tabs[name]['content_frame'].pack(
            expand='yes',
            fill='both',
            anchor='nw')
        self.tabs[name]['tabbutton'].switch_state('active')

    def get_orientation(self):
        u"""Return 'horizontal' or 'vertical'."""
        return self.__orientation

    def set_orientation(self, orientation):
        assert orientation in (Tab.VERTICAL, Tab.HORIZONTAL)
        self.__orientation = orientation
        self.update_orientation()

    def update_orientation(self):
        self.__tabs_frame.pack_forget()
        self.__content_frame.pack_forget()
        if self.__orientation == Tab.VERTICAL:
            self.__tabs_frame.pack(side='left')
            self.__content_frame.pack(expand='yes', fill='both')
        elif self.__orientation == Tab.HORIZONTAL:
            self.__tabs_frame.pack(side='top')
            self.__content_frame.pack(expand='yes', fill='both')


if __name__ == '__main__':
    import window

    def _gen_content(title):
        def _get_content(master):
            fr = widgets.Frame(master).grid(sticky='nw')
            widgets.Label(
                fr,
                text=title,
                font=('TkDefaultFont', 15),
                fg='#444').grid(sticky='nw', pady=15, padx=15)
            widgets.HorizontalLine(
                fr,
                width=500).grid(sticky='we')

            return fr

        return _get_content

    top = window.Window()
    # top.resizable(0, 0)
    top.enable_escape()
    top['bg'] = '#fafafa'
    tab = Tab(top, orientation=Tab.VERTICAL).grid()
    tab.add_tab(
        'code',
        _gen_content(u'Code'),
        text=u'Code',
        width=150)
    tab.add_tab(
        'issues',
        _gen_content(u'Issues'),
        text=u'Issues',
        width=150)
    tab.add_tab(
        'PR',
        _gen_content(u'Pull requests'),
        text=u'Pull Requests',
        width=150)
    tab.add_tab(
        'wiki',
        _gen_content(u'Wiki'),
        text=u'Wiki',
        width=150)
    _icon = None
    # this will fail if you havent PIL
    try:
        _icon = window.get_photo_class()(file='examples/settings.png')
    except:
        pass
    tab.add_tab(
        'settings',
        _gen_content(u'Settings'),
        text=u'Settings',
        icon=_icon,
        width=150)
    tab.add_tab(
        'overview',
        _gen_content(u'Overview'),
        text=u'Overview',
        width=150)
    tab.add_tab(
        'ssh',
        _gen_content(u'SSH Keys'),
        text=u'SSH Keys',
        width=150)
    tab.add_tab(
        'milestones',
        _gen_content(u'Milestones'),
        text=u'Milestones',
        width=150)
    tab.add_tab(
        'snippets',
        _gen_content(u'Snippets'),
        text=u'Snippets',
        width=150)
    tab.view_tab('issues')
    top.mainloop()

# fixme: o tabbutton padrão deve permitir aceitar ícones e texto
