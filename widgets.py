# coding: utf-8

import window
import math


class BaseWidget(object):
    def grid(self, *args, **kwargs):
        super(BaseWidget, self).grid(*args, **kwargs)
        return self

    def pack(self, *args, **kwargs):
        super(BaseWidget, self).pack(*args, **kwargs)
        return self

    def hide_bg(self):
        self.__copy_bg()
        self.master.bind('<Configure>', self.__copy_bg, '+')

    def __copy_bg(self, event=None):
        self['bg'] = self.master['bg']


class Frame(BaseWidget, window.tk.Frame):
    def __init__(self, *args, **kwargs):
        window.tk.Frame.__init__(self, *args, **kwargs)
        BaseWidget.__init__(self)
        self.hide_bg()

    @property
    def width(self):
        return int(self['width'])

    @width.setter
    def width(self, value):
        self['width'] = value

    @property
    def height(self):
        return int(self['height'])

    @height.setter
    def height(self, value):
        self['height'] = value


class ExtendedCanvas(BaseWidget, window.tk.Canvas):
    def __init__(self, *args, **kwargs):
        self.__items = []
        BaseWidget.__init__(self)
        window.tk.Canvas.__init__(self, *args, **kwargs)

    @property
    def center(self):
        return [self.width / 2, self.height / 2]

    @property
    def width(self):
        self.update_idletasks()
        return max(int(self['width']) - 1, int(self.winfo_width()))

    @width.setter
    def width(self, value):
        self['width'] = value
        self.update()

    @property
    def height(self):
        self.update_idletasks()
        return max(int(self['height']) - 1, int(self.winfo_height()))

    @height.setter
    def height(self, value):
        self['height'] = value
        self.update()

    def get_circle_point(self, cx, cy, radius, angle):
        '''
        Returns the position of a vertex2D of a circle
        which center is in [cx,cy] position and radius 'radius'
        in the angle 'angle'
        '''
        # angle in degree
        angle = math.radians(angle)
        y = math.sin(angle) * radius
        x = math.cos(angle) * radius
        x += cx
        y = cy - y
        return [x, y]

    def create_rounded_rectangle(self, pos, radius, **kwargs):
        '''
        pos: [x1, y1, x2, y2]
        radius: [nw, sw, se, ne]
        '''
        pts = []
        # NW
        if radius[0]:
            cx = pos[0] + radius[0]
            cy = pos[1] + radius[0]
            for i in range(90, 180):
                pts.extend(self.get_circle_point(
                    cx, cy,
                    radius[0], i))
        else:
            pts.extend([pos[0], pos[1]])
        # SW
        if radius[1]:
            cx = pos[0] + radius[1]
            cy = pos[3] - radius[1]
            for i in range(180, 270):
                pts.extend(self.get_circle_point(
                    cx, cy,
                    radius[1], i))
        else:
            pts.extend([pos[0], pos[3]])

        # SE
        if radius[2]:
            cx = pos[2] - radius[2]
            cy = pos[3] - radius[2]
            for i in range(270, 360):
                pts.extend(self.get_circle_point(
                    cx, cy,
                    radius[2], i))
        else:
            pts.extend([pos[2],
                        pos[3]])
        # NE
        if radius[3]:
            cx = pos[2] - radius[3]
            cy = pos[1] + radius[3]
            for i in range(0, 90):
                pts.extend(self.get_circle_point(
                    cx, cy,
                    radius[3], i))
        else:
            pts.extend([pos[2],
                        pos[1]])
        return self.create_polygon(*pts, **kwargs)


class Label(BaseWidget, window.tk.Label):
    def __init__(self, *args, **kwargs):
        window.tk.Label.__init__(self, *args, **kwargs)
        BaseWidget.__init__(self)
        self.hide_bg()

    @property
    def text(self):
        return self['text']

    @text.setter
    def text(self, value):
        self['text'] = value


class HorizontalLine(ExtendedCanvas):
    def __init__(self, master, **kws):
        ExtendedCanvas.__init__(
            self,
            master,
            height=1,
            relief='flat',
            bd=0,
            highlightthickness=0,
            **kws
        )


if __name__ == '__main__':
    import window
    top = window.Window('rounded rectangle')
    top.enable_escape()
    ca = ExtendedCanvas(top, width=100, height=30).pack()
    ca.create_rounded_rectangle(
        [2, 2, 90, 30], [8] * 4, outline='#999',
        fill=''
    )
    top.mainloop()

# ## LISTBOX
# class ExtendedListboxItem(object):
#     '''
#     before_click: function called before the click selection
#     '''
#     def __init__(self, canvas, title, subtitle, icon,
#             height, yoffset, before_click):
#         '''
#         use_arrows: if arrow up and down will change the
#         selected item
#         '''
#         self.canvas = canvas
#         self.__before_click = before_click
#         self.__selected = False
#         self.__rec_bg = draw.RectangleDraw(canvas, 1, 1+yoffset,
#             canvas.width, 40, fill=self.canvas['bg'], outline='')

#         self.__title = draw.TextDraw(canvas, 50, 7 + yoffset, text=title,
#             anchor='nw', font=('TkDefaultFont', 10))
#         self.__subtitle = draw.TextDraw(canvas, 50, 22 + yoffset,
#             text=subtitle, anchor='nw', font=('TkDefaultFont',8), fill='#555')
#         self.__icon = draw.ImageDraw(self.canvas, 5, 6+yoffset, icon, anchor='nw') if icon else None

#         self.bind('<Enter>', self.__mouse_over, '+')
#         self.bind('<Leave>', self.__mouse_leave, '+')
#         self.bind('<1>', self.__on_click, '+')

#     def __on_click(self, evt):
#         if self.__before_click:
#             self.__before_click(self)
#         self.selected = True

#     @property
#     def before_click(self):
#         return self.__before_click

#     def bind(self, *args, **kws):
#         self.__rec_bg.bind(*args, **kws)
#         self.__title.bind(*args, **kws)
#         self.__subtitle.bind(*args, **kws)
#         if self.__icon:
#             self.__icon.bind(*args, **kws)

#     def __mouse_over(self, evt):
#         self.__rec_bg.style['fill'] = '#cdcdcd'
#         self.__rec_bg.update()

#     def __mouse_leave(self, evt):
#         if self.__selected:
#             self.__rec_bg.style['fill'] = '#bbb'
#         else:
#             self.__rec_bg.style['fill'] = self.canvas['bg']
#         self.__rec_bg.update()

#     @property
#     def selected(self):
#         return self.__selected

#     @selected.setter
#     def selected(self, value):
#         self.__selected = bool(value)
#         self.__mouse_leave(None)

#     def delete(self):
#         self.__rec_bg.delete()
#         self.__title.delete()
#         self.__subtitle.delete()
#         if self.__icon:
#             self.__icon.delete()

#     @property
#     def title(self):
#         return self.__title.text

#     @title.setter
#     def title(self, value):
#         self.__title.text = value

#     @property
#     def subtitle(self):
#         return self.__subtitle.text

#     @subtitle.setter
#     def subtitle(self, value):
#         self.__subtitle.text = value

#     @property
#     def icon(self):
#         return self.__icon.image

#     # is not possible set icon because
#     # any bind already made cant be applyed
#     # to image
#     # @icon.setter
#     # def icon(self, value):
#     #     self.__icon.image = value


# class DuplicatedExtendedListboxItemException(Exception):
#     pass


# class ExtendedListbox(ExtendedCanvas):
#     def __init__(self, *args, **kws):
#         self.__items = []
#         # if unique titles is true, when you add a item
#         # with a title equal than another the ExtendedListbox
#         # raises an DuplicatedExtendedListboxItemError
#         self.unique_titles = kws.pop('unique_titles', False)
#         self.item_height = kws.pop('item_height', 40)
#         ExtendedCanvas.__init__(self, *args, **kws)

#         if kws.pop('use_arrows', True):
#             self.bind('<Up>', lambda evt: self.up_selection(), '+')
#             self.bind('<Down>', lambda evt: self.down_selection(), '+')

#     def up_selection(self):
#         if len(self.__items) > 1 and self.get_selected_index() > 0:
#             self.select_by_index(self.get_selected_index() - 1)

#     def down_selection(self):
#         if len(self.__items) > 0 and self.get_selected_index() < (len(self.__items)-1):
#             self.select_by_index(self.get_selected_index() + 1)

#     def add_item(self, title, subtitle=None, icon=None, before_click=None):
#         if self.unique_titles and self.get_item_by_title(title):
#             raise DuplicatedExtendedListboxItemException()
#         item = ExtendedListboxItem(self, title, subtitle, icon,
#             self.item_height, self.item_height * len(self.__items),
#             before_click=self.__item_click_handler(before_click))
#         self.__items.append(item)
#         self.__update_scroll_region()
#         return item

#     def __update_scroll_region(self):
#         self['scrollregion'] = (0, 0, self.width, self.item_height * len(self.__items))

#     def __item_click_handler(self, function):
#         '''
#         returns a function that returns a function
#         '''
#         def __final_function(*args):
#             self.desselect_all()
#             if function:
#                 function(*args)
#         return __final_function

#     def get_all(self):
#         return self.__items

#     def get_item_by_title(self, title):
#         for i in self.__items:
#             if i.title == title:
#                 return i
#         return None

#     def remove_by_title(self, title):
#         for i in self.__items:
#             if i.title == title:
#                 i.delete()
#                 self.__items.remove(i)
#         self.redraw()

#     def remove_by_index(self, index):
#         self.__items.pop(index).delete()
#         self.redraw()

#     def get_selected(self):
#         '''
#         returns the item selected
#         '''
#         for i in self.__items:
#             if i.selected:
#                 return i
#         return None

#     def get_selected_index(self):
#         '''
#         returns the index of item inside
#         the list of items
#         '''
#         for i in range(len(self.__items)):
#             if self.__items[i].selected:
#                 return i

#     def select_item(self, item):
#         item.selected = True
#         # finding the index
#         for i in range(len(self.__items)):
#             if self.__items[i] == item:
#                 self.yview('moveto', float(i) / len(self.__items))
#                 break

#     def select_last(self):
#         if len(self.__items) > 0:
#             self.select_item(self.__items[-1])

#     def select_first(self):
#         if len(self.__items) > 0:
#             self.select_item(self.__items[0])

#     def select_by_index(self, index):
#         if index >= 0 and index <= (len(self.__items) - 1):
#             self.desselect_all()
#             self.select_item(self.__items[index])

#     def desselect_all(self, *args):
#         for i in self.__items:
#             i.selected = False

#     def delete_all(self):
#         for i in self.__items:
#             i.delete()
#         self.__items = []
#         self.redraw()

#     def redraw(self):
#         _old_list = self.__items
#         self.__items = []
#         for i in _old_list:
#             i.delete()
#             item = ExtendedListboxItem(self, i.title, i.subtitle, i.icon,
#                 self.item_height, self.item_height * len(self.__items),
#                 self.desselect_all)
#             self.__items.append(item)
#         self.__update_scroll_region()

# class ScrollableExtendedListbox(Frame):
#     def __init__(self, master, *args, **kws):
#         '''
#         side: the side of scroll
#         '''
#         Frame.__init__(self, master)
#         side = kws.pop('side', 'right')
#         self.__extended_listbox = ExtendedListbox(self, *args, **kws)
#         self.__scroll = FlatVerticalScroller(self)
#         self.__scroll.pack(fill='y', side=side)
#         self.__extended_listbox.pack(
#             expand='yes',
#             fill='both'
#         )
#         self.__scroll.set_command(
#             self.__extended_listbox.yview
#         )

#         self.__extended_listbox.config(
#             yscrollcommand=self.__scroll.set
#         )


#     # ALIAS
#     def select_by_index(self, *args, **kws):
#         return self.__extended_listbox.select_by_index(*args, **kws)

#     # ALIAS
#     def get_selected_index(self, *args, **kws):
#         return self.__extended_listbox.get_selected_index(*args, **kws)

#     # ALIAS
#     def up_selection(self, *args, **kws):
#         return self.__extended_listbox.up_selection(*args, **kws)

#     # ALIAS
#     def down_selection(self, *args, **kws):
#         return self.__extended_listbox.down_selection(*args, **kws)

#     # ALIAS
#     def add_item(self, *args, **kws):
#         return self.__extended_listbox.add_item(*args, **kws)

#     # ALIAS
#     def get_all(self, *args, **kws):
#         return self.__extended_listbox.get_all(*args, **kws)

#     # ALIAS
#     def redraw(self, *args, **kws):
#         return self.__extended_listbox.redraw(*args, **kws)

#     # ALIAS
#     def desselect_all(self, *args, **kws):
#         return self.__extended_listbox.desselect_all(*args, **kws)

#     # ALIAS
#     def remove_by_index(self, *args, **kws):
#         return self.__extended_listbox.remove_by_index(*args, **kws)

#     # ALIAS
#     def get_selected(self, *args, **kws):
#         return self.__extended_listbox.get_selected(*args, **kws)

#     # ALIAS
#     def select_last(self, *args, **kws):
#         return self.__extended_listbox.select_last(*args, **kws)

#     def select_first(self, *args, **kws):
#         return self.__extended_listbox.select_first(*args, **kws)

#     # ALIAS
#     def get_item_by_title(self, *args, **kws):
#         return self.__extended_listbox.get_item_by_title(*args, **kws)

#     # ALIAS
#     def remove_by_title(self, *args, **kws):
#         return self.__extended_listbox.remove_by_title(*args, **kws)

#     # ALIAS
#     def delete_all(self, *args, **kws):
#         return self.__extended_listbox.delete_all(*args, **kws)


# class ColorChooser(ExtendedCanvas):
#     '''
#     To get/set the color use 'color' property
#     '''
#     def __init__(self, parent, color, **kws):
#         radius = kws.pop('radius', [5]*4)
#         kws.update(
#             bg=parent['bg'],
#             bd=0,
#             highlightthickness=0,
#             height=kws.get('height', 30)
#         )
#         self.on_choose = kws.pop('on_choose', None)
#         ExtendedCanvas.__init__(self, parent, **kws)
#         self.__color = draw.RoundedRectangleDraw(self, [0,0,self.width,self.height],
#             radius=radius, fill=color, outline=color)
#         self.bind('<1>', self.choose, '+')

#     @property
#     def radius(self):
#         return self.__color.radius

#     @radius.setter
#     def radius(self, value):
#         self.__color.radius = value

#     def choose(self, evt):
#         rgb = tkColorChooser.askcolor(color=self.color)[1]
#         if rgb:
#             self.color = rgb
#             if self.on_choose:
#                 self.on_choose(evt)

#     @property
#     def color(self):
#         return self.__color.fill

#     @color.setter
#     def color(self, value):
#         self.__color.configure(fill=value, outline=value)

#     def update(self):
#         ExtendedCanvas.update(self)
#         self.__color.width = self.width
#         self.__color.height = self.height

#     @property
#     def value(self):
#         return self.color


# class Button(ExtendedCanvas):
#     def __init__(self, *args, **kwargs):
#         _wi, _he = kwargs.pop('width', 100), kwargs.pop('height', 25)
#         self.radius = kwargs.pop('radius', [2, 2, 2, 2])
#         self.level = 1
#         self.__bg_color = kwargs.pop('bgcolor', '#efefef')
#         self.__bd_color = kwargs.pop('bdcolor', '#aaa')
#         self.__font = kwargs.pop('font', ('TkDefaultFont', 10))
#         _fg_color = kwargs.pop('fgcolor', 'black')

#         self.default = kwargs.pop('default', '')
#         _text = kwargs.pop('text', '')
#         self.command = kwargs.pop('command', None)

#         if self.default == 'active':
#             self.__bd_color = '#00aacc'

#         kwargs.update(width=_wi, height=_he, bg='#efefef')
#         ExtendedCanvas.__init__(self, *args, **kwargs)
#         self.update_idletasks()

#         self.__bg = draw.RoundedRectangleDraw(
#             self, [0, 0, self.width, self.height],
#             radius=self.radius, fill=self.__bg_color,
#             outline=self.__bd_color
#         )

#         self.__text = draw.TextDraw(
#             self,
#             self.width / 2,
#             self.height / 2,
#             _text,
#             fill=_fg_color,
#             font=self.__font
#         )

#         self.__bind_command(self.command)

#         self.config(
#             bg=self.master['bg'],
#             relief='flat', bd=0,
#             highlightthickness=0)

#     def __bind_command(self, cmd):
#         if not cmd:
#             return
#         self.bind('<1>', lambda *args: cmd(), '+')

#     @property
#     def text(self):
#         return self.__text.text

#     @text.setter
#     def text(self, value):
#         self.__text.text = value

#     @property
#     def fgcolor(self):
#         return self.__text.style['fill']

#     @fgcolor.setter
#     def fgcolor(self, value):
#         self.__text.fill = value

#     @property
#     def bgcolor(self):
#         return self.__bg.style['fill']

#     @bgcolor.setter
#     def bgcolor(self, value):
#         self.__bg.fill = value

#     @property
#     def font(self):
#         return self.__text.font

#     @font.setter
#     def font(self, value):
#         self.__text.font = value

#     def update(self):
#         ExtendedCanvas.update(self)
#         self.__bg.width = self.width
#         self.__bg.height = self.height
#         self.__text.xy = [self.width / 2, self.height / 2]


# class Text(window.tk.Text, object):
#     def __init__(self, *args, **kws):
#         kws.update(
#             relief='flat',
#             border=10,
#             insertwidth=1,
#             highlightcolor='#aaa',
#             highlightthickness=1
#         )
#         window.tk.Text.__init__(self, *args, **kws)

#     def centralize_text(self):
#         self.tag_configure('center', justify='center')
#         self.tag_add('center', 1.0, 'end')

#     @property
#     def text(self):
#         return self.get(0.0, 'end')

#     @text.setter
#     def text(self, value):
#         self.delete(0.0, 'end')
#         self.insert(0.0, unicode(value))

#     @property
#     def value(self):
#         return self.text

# class MarkDownLabel(Text):
#     def __init__(self, master, text='', **kws):
#         kws.update(height=kws.get('height', 1))
#         self.normal_font = tkFont.Font(size=9)
#         self.h1_size = 20
#         self.__tag_count = 0
#         Text.__init__(self, master, **kws)
#         self['state'] = 'disabled'
#         self.text = text
#         self['highlightthickness'] = 0
#         self['relief'] = 'flat'
#         self['bg'] = master['bg']

#         self.tag_config('normal', font=('TkDefaultFont', 9))
#         self.tag_config('bold', font=('TkDefaultFont', 9, 'bold'))
#         self.tag_config('italic', font=('TkDefaultFont', 9, 'italic'))
#         self.tag_config('h1', font=('TkDefaultFont', 45))
#         self.tag_config('h2', font=('TkDefaultFont', 30))
#         self.tag_config('h3', font=('TkDefaultFont', 15))
#         # mixes
#         # self.tag_config('bold.italic', font=('TkDefaultFont', 9, 'italic', 'bold'))
#         # self.tag_config('h1.italic', font=('TkDefaultFont', 20, 'italic'))
#         # self.tag_config('h1.bold', font=('TkDefaultFont', 20, 'bold'))
#         # self.tag_config('h1.bold.italic', font=('TkDefaultFont', 20, 'italic', 'bold'))

#     @property
#     def text(self):
#         return self.get(0.0, 'end')

#     @text.setter
#     def text(self, value):
#         self['state'] = 'normal'
#         self.delete(0.0, 'end')

#         state = 'normal'
#         last_char = None
#         last_last_char = None

#         for i in range(len(value)):
#             c = value[i]
#             if c == '#':
#                 if state == 'normal':
#                     state = 'h1'
#                 elif state == 'h1':
#                     state = 'h2'
#                 elif state == 'h2':
#                     state = 'h3'
#             elif c == '*':
#                 # two following * must write at least one
#                 if state != 'bold' and last_char != '*':
#                     state = 'bold'
#                 elif state == 'bold':
#                     state = 'normal'
#             elif c == '_':
#                 # two following _ must write at least one
#                 if state != 'italic' and last_char != '_':
#                     state = 'italic'
#                 elif state == 'italic':
#                     state = 'normal'
#             elif c == '-':
#                 if last_char == '-' and last_last_char == '-' and value[i-3] == '\n':
#                     c = '–' * int(self['width'])
#                     self.insert_character(c, state)
#                 else:
#                     self.insert_character(c, state)
#             elif c == ' ':
#                 # ignoring white space after h1
#                 if last_char == '#':
#                     pass
#                 else:
#                     self.insert_character(c, state)
#             elif c == '\n':
#                 if state in ('h1', 'bold', 'italic', 'h2', 'h3'):
#                     # reseting the style on a new line
#                     state = 'normal'
#                 self.new_line()
#             else:
#                 if last_char == '-':
#                     self.insert_character('-', state)
#                 self.insert_character(c, state)
#             last_last_char = last_char
#             last_char = c

#         self['state'] = 'disabled'

#     def new_line(self):
#         '''
#         inserts a new line in text
#         '''
#         self.insert('end', '\n')

#     def insert_character(self, character, state):
#         self.insert('end', character, (state,))


# class LabeledSimpleCheckbox(Frame):
#     '''
#     a simplecheckbox with a label
#     '''
#     def __init__(self, master, text='', checkclass=SimpleCheckbox, **checkinitkws):
#         '''
#         checkclass: the check button class to use
#         checkinitkws: the kws that will be passed to Checkbox instance
#         '''
#         self.__checkclass = checkclass
#         Frame.__init__(self, master)
#         self.checkbutton = checkclass(self, **checkinitkws)
#         self.checkbutton.pack(anchor='nw', pady=5, padx=5, side='left')
#         self.label = Label(self, text=text)
#         self.label.pack(expand='yes', anchor='w')
#         self.label.bind('<1>', self.__check, '+')

#     def __check(self, event):
#         '''
#         called when you click in the frame
#         '''
#         self.checkbutton.checked = not self.checkbutton.checked

#     @property
#     def text(self):
#         return self.label.text

#     @text.setter
#     def text(self, value):
#         self.label.text = value

#     @property
#     def checked(self):
#         return self.checkbutton.checked

#     @checked.setter
#     def checked(self, value):
#         self.checkbutton.checked = value

# class Entry(window.tk.Entry, object):
#     def __init__(self, *args, **kws):
#         self.__placeholder = kws.pop('placeholder', '')
#         self.numbersonly = kws.pop('numbersonly', False)

#         self.__maxlength = None
#         self.__min = kws.pop('min', None)
#         self.__max = kws.pop('max', None)

#         # when 'intergersonly' is false the entry allows
#         # float entry
#         self.integersonly = kws.pop('integersonly', True)
#         # TODO: test period in windows
#         self.commands_dictionary = ['BackSpace', 'Delete',
#             'Left', 'Right', 'Up', 'Down', 'Escape', 'Return',
#             'Tab', 'Shift_L', 'Shift_R', 'ISO_Left_Tab']
#         # allows only specified characters
#         self.__allowsonly = None
#         self.allowsonly = kws.pop('allowsonly', None)

#         # the keysyms allowed in numberonly mode
#         self.numbers_dictionary = ['period', '.', '-', 'minus']
#         self.numbers_dictionary.extend( list(string.digits) )
#         self.numbers_dictionary.extend( self.commands_dictionary )
#         # when you clicks up and down key the current value is
#         # increased or decreased
#         self.__step = kws.pop('step', 1)
#         self.step = self.__step
#         self.min = self.__min
#         self.max = self.__max
#         self.__maxlength = kws.pop('maxlength', None)
#         kws.update(relief='flat',
#             border=10,
#             insertwidth=1,
#             highlightcolor='#aaa',
#             highlightthickness=1)
#         window.tk.Entry.__init__(self, *args, **kws)

#         # TODO: fix this, up and down behaviour is not working properly
#         # self.bind('<Up>', self.__upk_handler, '+')
#         # self.bind('<Down>', self.__downk_handler, '+')
#         self.bind('<Any-Key>', self.__any_key_handler, '+')
#         self.bind('<Any-KeyRelease>', lambda e: self.validate(), '+')

#     @property
#     def allowsonly(self):
#         return self.__allowsonly

#     @allowsonly.setter
#     def allowsonly(self, value):
#         if type(value) not in (list, type(None), tuple):
#             raise ValueError('wrong type {}'.format(type(value)))
#         if value:
#             self.__allowsonly = list(value)
#             self.__allowsonly.extend( self.commands_dictionary )

#     @property
#     def maxlength(self):
#         return self.__maxlength

#     @maxlength.setter
#     def maxlength(self, value):
#         if type(value) == None:
#             self.__maxlength = None
#             return
#         if type(value) != int or value <= 0:
#             raise ValueError('Incorrect maxlength value')
#         self.__maxlength = value

#     @property
#     def min(self):
#         return self.__min

#     @min.setter
#     def min(self, value):
#         if value is None:
#             self.__min = None
#             return
#         self.__min = (int if self.integersonly else float)(value)

#     @property
#     def max(self):
#         return self.__max

#     @max.setter
#     def max(self, value):
#         if value is None:
#             self.__max = None
#             return
#         self.__max = (int if self.integersonly else float)(value)

#     @property
#     def step(self):
#         return self.__step

#     @step.setter
#     def step(self, value):
#         self.__step = (int if self.integersonly else float)(value)

#     def convert_to_number(self):
#         '''
#         returns the actual text to a number
#         '''
#         return (int if self.integersonly else float)(self.text)

#     def __upk_handler(self, event):
#         '''
#         called when the user press the Up arrow key
#         '''
#         if self.numbersonly:
#             try:
#                 value = self.convert_to_number()
#                 if (self.max is not None) and (value + self.step) > self.max:
#                     self.text = self.max
#                 else:
#                     self.text = value + self.step
#             except:
#                 pass

#     def __downk_handler(self, event):
#         '''
#         called when the user press the Down arrow key
#         '''
#         if self.numbersonly:
#             try:
#                 value = float(self.text)
#                 if (self.min is not None) and (value - self.step) < self.min:
#                     self.text = self.min
#                 else:
#                     self.text = value - self.step
#             except:
#                 pass

#     def valid(self):
#         '''
#         returns true if entry content is valid
#         '''
#         if type(self.allowsonly) == list:
#             for c in self.text:
#                 if c not in self.allowsonly:
#                     return False

#         if self.numbersonly:
#             for c in self.text:
#                 if c not in self.numbers_dictionary:
#                     return False

#         if type(self.maxlength) == int:
#             if len(self.text) > self.maxlength:
#                 return False

#         return True

#     def validate(self):
#         '''
#         called every hit in keyboard
#         make the border red if is not valid
#         '''
#         self['highlightcolor'] = '#aaa' if self.valid() else 'red'

#     def __any_key_handler(self, event):
#         '''
#         called at each hit in the keyboard
#         '''
#         if type(self.allowsonly) == list:
#             if event.keysym not in self.allowsonly:
#                 return 'break'

#         if self.numbersonly:
#             if event.keysym not in self.numbers_dictionary:
#                 # in tkinter, return 'breaks' cancel the propagation
#                 # of event, not putting the letter in entry widget
#                 return 'break'
#             else:
#                 if event.keysym == 'period':
#                     # allows write only one period
#                     if  '.' in self.text:
#                         return 'break'
#                     elif self.text == '':
#                         # if is the first time that the period is hitted
#                         # and the the entry is empty, put a left zero
#                         self.text += '0'
#                 if event.keysym == 'minus':
#                     if self.text[0] == '-':
#                         self.text = self.text[1:]
#                     else:
#                         self.text = '-' + self.text
#                     return 'break'

#         if type(self.maxlength) == int and event.keysym not in self.commands_dictionary:
#             # the character that you are writing now is not in entry still
#             if len(self.text) == self.maxlength:
#                 return 'break'
#         self.validate()

#     @property
#     def text(self):
#         return self.get()

#     @property
#     def value(self):
#         if self.numbersonly:
#             return None if not self.text else (int if self.integersonly else float)(self.text)
#         return self.text

#     @text.setter
#     def text(self, value):
#         self.delete(0, 'end')
#         self.insert(0, unicode(value))
#         self.validate()


# class PlaceHoldedEntry(ExtendedCanvas):
#     def __init__(self, master, placeholder='', **kws):
#         self.__placeholder = placeholder
#         width, height = kws.get('width', 100), kws.get('height', 30)
#         self.__placeholder_width = 150
#         ExtendedCanvas.__init__(self, master,
#             width=width, height=height,
#             bg=BG_COLOR, bd=0, highlightthickness=0
#         )
#         self.__bg = draw.RoundedRectangleDraw(
#             self, [1,1,width-2,height-1],
#             fill='#fff', outline='#aaa',
#             radius=[5,5,5,5]
#         )
#         self.__placeholder_bg = draw.RoundedRectangleDraw(
#             self, [1,1,self.__placeholder_width,height-1],
#             fill='', outline='#00aacc',
#             radius=[5,5,0,0]
#         )
#         self.__placeholder_text = draw.TextDraw(
#             self, self.__placeholder_width/2, height/2,
#             self.__placeholder, anchor='center', fill='#00aacc'
#         )

#         self.__frame = Frame(self, width=width-self.__placeholder_width-4-5, height=height-4)
#         # self.__frame.pack()
#         self.__frame.pack_propagate(0)

#         self.__entry = Entry(self.__frame)
#         self.__entry.pack(expand='yes', fill='both')

#         self.__widget = draw.WidgetDraw(
#             self, self.__placeholder_width+1, 2, self.__frame, anchor='nw'
#         )

#         self.__entry.configure(
#             bd=0, highlightthickness=0
#         )


# class Listbox(window.tk.Listbox):
#     def __init__(self, *args, **kwargs):
#         window.tk.Listbox.__init__(self, *args, **kwargs)
#         self['bg'] = '#d1d8e0'
#         self['relief'] = 'flat'
#         self['highlightthickness'] = 0
#         self['selectbackground'] = '#c7ccd1'
#         self['activestyle'] = 'none'


# class OptionMenu(window.tk.OptionMenu):
#     pass


# class PopUpMenu(window.SubWindow):
#     def __init__(self, master, items, width=500):
#         window.SubWindow.__init__(self, master)
#         self.overrideredirect(True)
#         self.canvas = ExtendedListbox(self)
#         self['width'] = width  # TODO fixme

#         self.bind('<Escape>', lambda evt: self.destroy(), '+')
#         self.focus_force()
#         # ver alternativa pra isso:
#         # self.bind('<FocusOut>', lambda evt: self.destroy(), '+')

#         self.geometry('%dx%d' % (width, len(items) * 40))
#         self.update_idletasks()
#         self.canvas.width = width
#         self.canvas.pack(expand='yes', fill='both')

#         for i in items:
#             self.add_command(
#                 i.get('name', ''),
#                 subtitle=i.get('description', None),
#                 icon=i.get('icon', None),
#                 command=i.get('command', None))

#         self.center()

#     def add_command(self, title, subtitle=None, icon=None, command=None):
#         '''
#         binds a new command to ExtendedListboxItem, when
#         command is called and after that the popup closes
#         '''
#         item = self.canvas.add_item(title, subtitle, icon)
#         def __final_command(evt):
#             self.withdraw()
#             command(evt)
#             self.destroy()
#         item.bind('<1>', __final_command, '+')

#     def hide(self):
#         self.withdraw()

#     def show(self):
#         self.deiconify()

# class RemovableButton(Button):
#     def __init__(self, *args, **kws):
#         self.__removal_function = kws.pop('removal_function', None)
#         Button.__init__(self, *args, **kws)
#         self.__remove_button = draw.TextDraw(
#             self, self.width - 5, self.height/2, 'x',
#             anchor='e'
#         )
#         self.__remove_button.bind('<1>', self.__removal_button_click, '+')

#     def __removal_button_click(self, event=None):
#         if self.__removal_function:
#             self.__removal_function()

#     def update(self):
#         Button.update(self)
#         self.__remove_button.xy = [self.width-5, self.height/2]
#         self.__remove_button.font = self.font

# class DuplicatedRemovalButtonException(Exception):
#     pass

# class RemovalButtonsStack(Frame):
#     def __init__(self, *args, **kws):
#         '''
#         uniqueonly: boolean, if true you wont be add duplicated
#         buttons
#         '''
#         self.__buttons = []
#         self.__uniqueonly = kws.pop('uniqueonly', True)
#         Frame.__init__(self, *args, **kws)

#     def __gen_removal_function(self, button_text):
#         def __final(*args):
#             for i in self.__buttons:
#                 if i.text == button_text:
#                     i.destroy()
#                     self.__buttons.remove(i)
#                     break
#         return __final

#     def buttons_exists(self, button_label):
#         for i in self.__buttons:
#             if i.text == button_label:
#                 return True
#         return False

#     def add(self, button_text):
#         if self.__uniqueonly and self.buttons_exists(button_text):
#             raise DuplicatedRemovalButtonException()
#         btn = RemovableButton(
#             self,
#             text=button_text,
#             removal_function=self.__gen_removal_function(button_text),
#             width=self.width
#         )
#         self.__buttons.append(btn)
#         btn.pack()

#     def add_many(self, *buttons):
#         '''
#         buttons must be a list of strings
#         '''
#         for i in buttons:
#             self.add(i)

#     @property
#     def value(self):
#         buttons = []
#         for i in self.__buttons:
#             buttons.append(i.text)
#         return buttons

# DEFAULT_CIRCLE_LOADER_STYLE = {
#     'bg': {
#         'width': 3, # levar em consideração o tamanho desse width para q o border n seja comido
#         'outline': '#ddd'
#     },
#     'text': {
#         'font': ('TkDefaultFont', 20)
#     },
#     'loader': {
#         'style': 'arc',
#         'width': 3,
#         'outline': '#00aacc',
#         'extent': 359.9,
#         'start': 0
#     }
# }
# class CircleLoader(ExtendedCanvas):
#     def __init__(self, master, *args, **kws):
#         kws.update(
#             width=kws.get('width', 100),
#             height=kws.get('height', 100),
#             bg=kws.get('bg', master['bg']),
#             bd=kws.get('bd', 0),
#             highlightthickness=kws.get('highlightthickness', 0)
#         )
#         text = kws.pop('text', '')
#         style = kws.pop('style', DEFAULT_CIRCLE_LOADER_STYLE)
#         style['bg'].update(
#             style='arc',
#             extent=359.9
#         )
#         ExtendedCanvas.__init__(self, *args, **kws)
#         self.__text = draw.TextDraw(self, self.width/2, self.height/2, text=text, **style['text'])
#         self.__bgloader = draw.ArcDraw(self, [1,1,self.width-1,self.height-1], **style['bg'])
#         self.__loader = draw.ArcDraw(self, [1,1,self.width-1,self.height-1], **style['loader'])
#         self.__tween = animation.Tween(self.after, self.__loader, loop=True, ifactor=0.05, ticker=100)


#     @property
#     def text(self):
#         return self.__text.text

#     @text.setter
#     def text(self, value):
#         self.__text.text = value

#     @property
#     def font(self):
#         return self.__text.font

#     @font.setter
#     def font(self, value):
#         self.__text.font = value

#     @property
#     def outlinewidth(self):
#         return self.__loader.arcwidth

#     def indeterminated(self):
#         # self.__tween.animate('startangle', 360, _from=0)
#         animation.Tween(self.after, self, loop=True, ifactor=0.05, ticker=50).animate('outlinewidth', 10, _from=1)

#     @outlinewidth.setter
#     def outlinewidth(self, value):
#         self.__loader.xy = [value/2]*2
#         self.__loader.width = self.width-value
#         self.__loader.height = self.height-value
#         self.__loader.arcwidth = value
#         self.__bgloader.arcwidth = value
#         self.__bgloader.xy = [value/2]*2
#         self.__bgloader.width = self.width-value
#         self.__bgloader.height = self.height-value


# class FlatVerticalScroller(ExtendedCanvas):
#     def __init__(self, master, width=5):
#         self.__command = None
#         self.__diff = None
#         ExtendedCanvas.__init__(self, master, width=width)
#         self.__scroll = draw.RoundedRectangleDraw(
#             self, 0,0,0,0, fill='#888', radius=[0]*4
#         )
#         self.__scroll.bind('<B1-Motion>', self.__drag_handler, '+')
#         self.__scroll.bind('<ButtonRelease-1>', self.__release_handler, '+')

#     def __release_handler(self, event):
#         self.__diff = None

#     def __drag_handler(self, event):
#         if self.__command:
#             if self.__diff == None:
#                 self.__diff = float(event.y) - self.__scroll.y
#             self.__command('moveto', (float(event.y)-self.__diff) / self.height)

#     def set_command(self, command):
#         self.__command = command

#     def set(self, top, down):
#         self.__scroll.coords = [
#             0, self.height*float(top),
#             self.width, self.height*float(down)
#         ]
#         self.__scroll.update()

# if __name__ == '__main__':
#     top = window.Window()
#     Label(top, text='CircleLoader').pack(side='left')
#     cl = CircleLoader(top); cl.outlinewidth = 10; cl.indeterminated()
#     cl.pack(side='left')
#     Label(top, text='RemovalButtonsStack').pack()
#     r = RemovalButtonsStack(top, width=200, height=50)
#     r.add_many('black', 'red', 'orange', 'blue', 'gray')
#     r.pack()

#     Label(top, text='SimpleCheckbox').pack()
#     SimpleCheckbox(top, checked=True).pack()
#     Label(top, text='ColorChooser').pack()
#     ColorChooser(top, color='black').pack()

#     Label(top, text='Button').pack()
#     Button(top, text='ok').pack()

#     Label(top, text='MarkDownLabel').pack()
#     MarkDownLabel(top, text='# H1\n## H2\n ### H3\n*bold* _italic_', height=10).pack()

#     Label(top, text='Entry (integers only)').pack()
#     e = Entry(top, integersonly=True, numbersonly=True)
#     e.text = 'text'
#     e.pack()

#     Label(top, text='PlaceHoldedEntry').pack()
#     PlaceHoldedEntry(top, placeholder='Name', width=300, text='ok').pack(side='left')

#     Label(top, text='HorizontalLine').pack()
#     HorizontalLine(top, width=300).pack(pady=5)

#     l = Listbox(top, height=3)
#     l.insert('end', 'item 1'); l.insert('end', 'item 2')
#     l.pack()
#     top.mainloop()