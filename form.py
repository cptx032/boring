import widgets
import ios

DEFAULT_FORM_WIDGETS = {
    'button': widgets.Button,
    'check': ios.IOSCheckbox,
    'float': widgets.Entry,
    'int': widgets.Entry,
    'password': widgets.Entry,
    'string': widgets.Entry,
    'color': widgets.ColorChooser,
    'text': widgets.Text
}

class FormFrame(widgets.Frame):
    def __init__(self, master, formstring,
                input_width=40,
                initial_values=None,
                title='',
                inputswidgets=DEFAULT_FORM_WIDGETS,
                font=('TkDefaultFont', 10)):
        self.__inputswidgets = inputswidgets
        self.__title = title
        self.__formstring = formstring
        self.__font = font
        self.initial_values = initial_values
        self.__frames = []
        self.__inputs = []
        self.__horizontal_line = None
        self.__markdown_title = None
        self.input_width = input_width
        widgets.Frame.__init__(self, master)
        self.build_form()

    def kill_frames(self):
        '''
        grid forget all frames
        '''
        if self.__horizontal_line:
            self.__horizontal_line.grid_forget()
        if self.__markdown_title:
            self.__markdown_title.grid_forget()
        for frame in self.__frames:
            frame.grid_forget()

    @property
    def values(self):
        '''
        return the current value in form
        '''
        result = []
        for i in self.__inputs:
            if type(i) == widgets.Entry:
                result.append(i.value)
            elif type(i) == self.__inputswidgets['text']:
                result.append(i.text)
            elif type(i) == self.__inputswidgets['check']:
                result.append(i.checked)
            elif type(i) == self.__inputswidgets['color']:
                result.append(i.color)
        return result

    def build_form(self):
        self.kill_frames()
        if self.__title:
            self.__markdown_title = widgets.MarkDownLabel(
                self,
                text='### %s' % (self.__title),
                height=2,
                width=30
            )
            self.__markdown_title.grid(
                sticky='w', pady=10
            )
            self.__horizontal_line = widgets.HorizontalLine(self, width=100)
            self.__horizontal_line.grid(sticky='we', pady=10)
        field_counter = 0
        for line in self.__formstring.split('\n'):
            if not line:
                continue
            fields = line.split('|')
            # each line has a frame
            frame = widgets.Frame(self)
            column = 0
            for field in fields:
                textlabel, inputtype = field.split('@')
                # each field has a frame, a line can have many
                # fields per line
                fieldframe = widgets.Frame(frame)
                fieldframe.grid(row=0, column=column, padx=0)

                label = widgets.Label(
                    fieldframe, text=textlabel,
                    font=self.__font
                )
                label.grid(
                    pady=1, padx=1, row=0,
                    column=0, sticky='w'
                )

                _input = None

                if inputtype == 'string':
                    _input = self.__inputswidgets['string'](
                        fieldframe,
                        width=self.input_width / len(fields),
                        font=self.__font
                    )
                    if self.initial_values:
                        _input.text = self.initial_values[field_counter]
                elif inputtype == 'int':
                    _input = self.__inputswidgets['int'](
                        fieldframe,
                        # many fields in line makes the sum of the widths be
                        # greater than an only fields because border
                        width=(self.input_width / len(fields)) if len(fields) == 1 else (self.input_width / len(fields) - 2),
                        numbersonly=True,
                        integersonly=True,
                        font=self.__font
                    )
                    if self.initial_values:
                        _input.text = self.initial_values[field_counter]
                elif inputtype == 'float':
                    _input = self.__inputswidgets['float'](
                        fieldframe,
                        width=self.input_width / len(fields),
                        numbersonly=True,
                        integersonly=False,
                        font=self.__font
                    )
                    if self.initial_values:
                        _input.text = self.initial_values[field_counter]
                elif inputtype == 'password':
                    # has not initial values for password entry
                    # if someone is given, is ignored
                    _input = self.__inputswidgets['password'](
                        fieldframe,
                        width=self.input_width / len(fields),
                        show='*',
                        font=self.__font
                    )
                elif inputtype == 'check':
                    _input = self.__inputswidgets['check'](fieldframe)
                    if self.initial_values:
                        _input.checked = self.initial_values[field_counter]
                elif inputtype == 'color':
                    _input = self.__inputswidgets['color'](
                        fieldframe,
                        '#dadada' if not self.initial_values else self.initial_values[field_counter],
                        height=30, width=350
                    )
                elif inputtype == 'text':
                    _input = self.__inputswidgets['text'](
                        fieldframe,
                        width=self.input_width / len(fields),
                        font=self.__font
                    )
                else:
                    raise Exception('InvalidFormStringError')
                _input.grid(pady=1, padx=0, row=1, column=0, sticky='w')

                self.__inputs.append(_input)

                column += 1
                field_counter += 1
            frame.grid(pady=5, padx=5, sticky='w')
            self.__frames.append(frame)
        self.__inputs[0].focus_force()

    @property
    def formstring(self):
        return self.__formstring

    @property
    def inputs(self):
        return self.__inputs

    @formstring.setter
    def formstring(self, value):
        self.__formstring = value
        self.build_form()