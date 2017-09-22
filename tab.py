# coding: utf-8
import collections
import packer
import widgets
import tabthemes


class SimpleTabButton(packer.StatePacker):
    ACTIVE_STATE = 'active'
    NORMAL_STATE = 'normal'
    DISABLED = 'disabled'

    def __init__(self, *args, **kwargs):
        kwargs['elems'] = tabthemes.LIGHT_THEME
        kwargs['state'] = 'active'
        # as opções são: text, icon
        _text = kwargs.pop('text', u'')

        kwargs['bd'] = 0
        kwargs['highlightthickness'] = 0

        if 'width' not in kwargs:
            kwargs['width'] = 100
        if 'height' not in kwargs:
            kwargs['height'] = 40
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
        content_frame = widgets.Frame(self.__content_frame)
        content = content_func(content_frame)
        self.tabs[name] = dict(
            name=name,
            tabbutton=tabbutton,
            content_frame=content_frame,
            content=content)

        kw = dict()
        if self.get_orientation() == Tab.HORIZONTAL:
            kw['row'] = 0
            kw['column'] = len(self.tabs.keys())
        elif self.get_orientation() == Tab.VERTICAL:
            kw['row'] = len(self.tabs.keys())
            kw['column'] = 0
        tabbutton.grid(**kw)

    def view_tab(self, name):
        for i in self.tabs:
            self.tabs[i]['content_frame'].grid_forget()
        self.tabs[name]['content_frame'].grid()

    # deve-se criar uma funcao que recebe um parent e todos os
    # elementos devem ser dispostos dentro desse parent
    # fixme: remover isso
    def merged_content(self, master):
        pass

    def get_orientation(self):
        return self.__orientation

    def set_orientation(self, orientation):
        assert orientation in (Tab.VERTICAL, Tab.HORIZONTAL)
        self.__orientation = orientation
        self.update_orientation()

    def update_orientation(self):
        self.__tabs_frame.grid_forget()
        self.__content_frame.grid_forget()
        self.__tabs_frame.grid(row=0, column=0)
        if self.__orientation == Tab.VERTICAL:
            self.__content_frame.grid(row=0, column=1)
        elif self.__orientation == Tab.HORIZONTAL:
            self.__content_frame.grid(row=1, column=0)


if __name__ == '__main__':
    import window
    import button

    def conteudo(master):
        return button.SimpleButton(master, text='Open').grid()

    def conteudo2(master):
        return button.SimpleButton(
            master, text='MERGEG').grid(pady=15, padx=15)

    top = window.Window()
    top.enable_escape()
    top['bg'] = '#fafafa'
    tab = Tab(top).grid()
    tab.add_tab('code', conteudo, text=u'Code')
    tab.add_tab('issues', conteudo2, text=u'Issues')
    tab.add_tab('PR', conteudo2, text=u'Pull Requests')
    tab.add_tab('wiki', conteudo2, text=u'Wiki')
    tab.add_tab('settings', conteudo2, text=u'Settings')
    tab.view_tab('wiki')
    top.mainloop()

# fixme: o conteudo deve ocupar todo o espaço disponível
# fixme: o tabbutton padrão deve permitir aceitar ícones e texto
