# coding: utf-8
import collections
from boring import draw

SHADOWED_WHITE = collections.OrderedDict()
SHADOWED_WHITE['shadow'] = {
    'def': {
        'class': draw.RoundedRectangleDraw,
        'x': 0,
        'y': 0,
        'width': 1.0,
        'height': 1.0
    },
    'states': {
        'active': {
            'normal': {
                'fill': '#0078e7',
                'radius': [5, 5, 5, 5],
            },
            'over': {
                'fill': '#0068d7',
                'radius': [5, 5, 5, 5],
            },
            'click': {
                'fill': '#0058c7',
                'radius': [5, 5, 5, 5],
            },
        },
        'normal': {
            'normal': {
                'fill': '#cccccc',
                'width': 0,
                'radius': [5, 5, 5, 5],
            },
            'over': {
                'fill': '#d5d5d5',
                'width': 0,
                'radius': [5, 5, 5, 5],
            },
            'click': {
                'fill': '#dadada',
                'width': 0,
                'radius': [5, 5, 5, 5],
            },
        },
        'disabled': {
            'normal': {
                'fill': '#000000',
                'radius': [5, 5, 5, 5],
            },
            'over': {
                'fill': '#000000',
                'radius': [5, 5, 5, 5],
            },
            'click': {
                'fill': '#000000',
                'radius': [5, 5, 5, 5],
            },
        },
    }
}

SHADOWED_WHITE['text'] = {
    'def': {
        'class': draw.TextDraw,
        'x': 0.5,
        'y': 0.5,
        'anchor': 'center',
        'font': ('TkDefaultFont', 12),
    },
    'states': {
        'active': {
            'normal': {
                'fill': '#ffffff',
            },
            'over': {
                'fill': '#ffffff',
            },
            'click': {
                'fill': '#ffffff',
            },
        },
        'normal': {
            'normal': {
                'fill': '#333333'
            },
            'over': {
                'fill': '#333333',
            },
            'click': {
                'fill': '#333333',
            },
        },
        'disabled': {
            'normal': {
                'fill': '#333333',
            },
            'over': {
                'fill': '#333333',
            },
            'click': {
                'fill': '#333333',
            },
        },
    }
}
