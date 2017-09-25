# coding: utf-8
import collections
import copy
import packer
import widgets
import tabthemes


class SimpleTabButton(packer.StatePacker):
    ACTIVE_STATE = 'active'
    NORMAL_STATE = 'normal'
    DISABLED = 'disabled'

    def __init__(self, *args, **kwargs):
        # as opções são: text, icon
        _text = kwargs.pop('text', u'')

        kwargs.setdefault('cursor', 'hand1')
        kwargs.setdefault('highlightthickness', 0)
        kwargs.setdefault('bd', 0)
        kwargs.setdefault('width', 100)
        kwargs.setdefault('height', 40)
        kwargs.setdefault('state', 'normal')
        kwargs.setdefault('elems', copy.deepcopy(tabthemes.LIGHT_THEME))

        packer.StatePacker.__init__(self, *args, **kwargs)
        self.set_text(_text)

    def set_text(self, text):
        self.items.get('text').get('draw').text = text

    def get_text(self):
        return self.items.get('text').get('draw').text


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
        # fixme: ao adicionar uma aba, se não houver nenhuma
        # ela deve ser ativada
        # se já existirem outras abas é preciso definir se vai
        # ser ativada ou não a partir da kwarg "view:True/False"
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

    def __view_tab_handler(self, event, name):
        u"""Called when the tabbutton is clicked."""
        self.view_tab(name)

    def view_tab(self, name):
        for i in self.tabs:
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
    import button

    def conteudo(master):
        return button.SimpleButton(master, text='Open').grid()

    def conteudo2(master):
        return button.SimpleButton(
            master, text='MERGEG').grid(pady=15, padx=15)

    def wiki_content(master):
        fr = widgets.Frame(master).grid(sticky='nw')
        widgets.Label(
            fr,
            text=u'Wiki',
            font=('TkDefaultFont', 15),
            fg='#444').grid(sticky='nw', pady=15, padx=15)
        widgets.HorizontalLine(
            fr,
            width=400).grid()

        return fr

    top = window.Window()
    top.enable_escape()
    top['bg'] = '#fafafa'
    tab = Tab(top, orientation=Tab.VERTICAL).grid()
    tab.add_tab('code', conteudo, text=u'Code', width=150)
    tab.add_tab('issues', conteudo2, text=u'Issues', width=150)
    tab.add_tab('PR', conteudo2, text=u'Pull Requests', width=150)
    tab.add_tab('wiki', wiki_content, text=u'Wiki', width=150)
    tab.add_tab('settings', conteudo2, text=u'Settings', width=150)
    tab.view_tab('wiki')
    top.mainloop()

# fixme: o conteudo deve ocupar todo o espaço disponível
# fixme: o tabbutton padrão deve permitir aceitar ícones e texto
