# coding: utf-8

CHECK_MARK = unichr(10003)

CHECKBOX_DEFAULT_THEME = {
    'checked': {
        'bg': {
            'fill': '#5cb85c'
        },
        'fg': {
            'text': CHECK_MARK,
            'fill': '#ffffff',
            'font': ('TkDefaultFont', 12, 'bold')
        }
    },
    'unchecked': {
        'bg': {
            'fill': '#5cb85c'
        },
        'text': {
            'fill': 'white',
            'font': ('TkDefaultFont', 12, 'bold')
        }
    },
    'disabled': {
        'bg': {
            'normal': {},
            'over': {},
            'click': {}
        },
        'fg': {
            'normal': {},
            'over': {},
            'click': {}
        }
    }
}
