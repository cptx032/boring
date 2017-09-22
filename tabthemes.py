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
        'active': {
            'normal': {
                'fill': '#ffffff',
                'width': 0
            },
            'over': {
                'fill': '#ffffff',
                'width': 0
            },
            'click': {
                'fill': '#ffffff',
                'width': 0
            }
        }
    }
}

LIGHT_THEME['bottom_shadow'] = {
    'def': {
        'class': draw.RectangleDraw,
        'x': 0,
        'y': 0.95,
        'width': 1.0,
        'height': 0.05
    },
    'states': {
        'active': {
            'normal': {
                'fill': '#AAA',
                'width': 0
            },
            'over': {
                'fill': '#CCC',
                'width': 0
            },
            'click': {
                'fill': '#555',
                'width': 0
            }
        }
    }
}

LIGHT_THEME['text'] = {
    'def': {
        'class': draw.TextDraw,
        'x': 0.5,
        'y': 0.5
    },
    'states': {
        'active': {
            'normal': {
                'fill': '#000',
                'width': 0
            },
            'over': {
                'fill': '#000',
                'width': 0
            },
            'click': {
                'fill': '#000',
                'width': 0
            }
        }
    }
}
