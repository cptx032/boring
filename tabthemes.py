# coding: utf-8
import collections
import draw

LIGHT_THEME = collections.OrderedDict()
LIGHT_THEME['bg'] = {
    'def': {
        'class': draw.RectangleDraw,
        'x': 0,
        'y': 0,
        'width': 1.0,
        'height': 1.0
    },
    'states': {
        'normal': {
            'normal': {
                'fill': '#eee',
                'width': 0
            },
            'over': {
                'fill': '#ddd',
                'width': 0
            },
            'click': {
                'fill': '#ccc',
                'width': 0
            }
        },
        'active': {
            'normal': {
                'fill': '#c5c5c5',
                'width': 0
            },
            'over': {
                'fill': '#dadada',
                'width': 0
            },
            'click': {
                'fill': '#cacaca',
                'width': 0
            },
        }
    }
}

LIGHT_THEME['text'] = {
    'def': {
        'class': draw.TextDraw,
        'x': 0.2,
        'y': 0.5,
    },
    'states': {
        'normal': {
            'normal': {
                'fill': '#333',
                'width': 0,
                'anchor': 'w'
            },
            'over': {
                'fill': '#333',
                'width': 0,
                'justify': 'left'
            },
            'click': {
                'fill': '#333',
                'width': 0,
                'justify': 'left'
            }
        },
        'active': {
            'normal': {
                'fill': '#333',
                'width': 0,
                'anchor': 'w'
            },
            'over': {
                'fill': '#333',
                'width': 0,
                'justify': 'left'
            },
            'click': {
                'fill': '#333',
                'width': 0,
                'justify': 'left'
            }
        }
    }
}
