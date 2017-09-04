# coding: utf-8
import collections
import draw

CHECK_MARK = u'\u2713'

SQUARE_GREEN_THEME = collections.OrderedDict()
SQUARE_GREEN_THEME['bg'] = {
    'def': {
        'class': draw.RoundedRectangleDraw,
        'x': 0,
        'y': 0,
        'width': 1.0,
        'height': 1.0
    },
    'states': {
        'checked': {
            'normal': {
                'fill': '#5cb85c',
                'width': 0,
                'radius': [0] * 4,
            },
            'over': {
                'fill': '#4ca84c',
                'width': 0,
                'radius': [0] * 4,
            },
            'click': {
                'fill': '#3c983c',
                'width': 0,
                'radius': [0] * 4,
            }
        },
        'unchecked': {
            'normal': {
                'fill': '#5cb85c',
                'width': 0,
                'radius': [0] * 4,
            },
            'over': {
                'fill': '#4ca84c',
                'width': 0,
                'radius': [0] * 4,
            },
            'click': {
                'fill': '#3c983c',
                'width': 0,
                'radius': [0] * 4,
            }
        },
        'disabled': {
            'normal': {
                'fill': '#dedede',
            },
            'over': {
                'fill': '#dcdcdc'
            },
            'click': {
                'fill': '#dadada'
            }
        }
    }
}

SQUARE_GREEN_THEME['fg'] = {
    'def': {
        'class': draw.TextDraw,
        'x': 0.5,
        'y': 0.5,
        'anchor': 'center'
    },
    'states': {
        'checked': {
            'normal': {
                'text': CHECK_MARK,
                'fill': '#ffffff',
                'font': ('helvetica', 12, 'bold'),
            },
            'over': {
                'text': CHECK_MARK,
            },
            'click': {
                'text': CHECK_MARK,
            }
        },
        'unchecked': {
            'normal': {
                'text': '',
                'fill': '#ffffff',
                'font': ('helvetica', 12, 'bold'),
            },
            'over': {
                'text': '',
            },
            'click': {
                'text': '',
            }
        },
        'disabled': {
            'normal': {
                'fill': '#aaa',
            },
            'over': {
                'fill': '#aaa',
            },
            'click': {
                'fill': '#aaa',
            },
        }
    }
}

SQUARE_WHITE_THEME = collections.OrderedDict()
SQUARE_WHITE_THEME['bg'] = {
    'def': {
        'class': draw.OvalDraw,
        'x': 0.0,
        'y': 0.0,
        'width': 0.95,
        'height': 0.95
    },
    'states': {
        'checked': {
            'normal': {
                'fill': '#ffffff',
                'width': 1,
                'outline': '#d9d9d9',
            },
            'over': {
                'fill': '#ffffff',
                'outline': '#d9d9d9',
                'width': 1,
            },
            'click': {
                'fill': '#ffffff',
                'outline': '#d9d9d9',
                'width': 1,
            }
        },
        'unchecked': {
            'normal': {
                'fill': '#ffffff',
                'width': 1,
                'outline': '#d9d9d9',
            },
            'over': {
                'outline': '#d9d9d9',
                'fill': '#ffffff',
                'width': 1,
            },
            'click': {
                'outline': '#d9d9d9',
                'fill': '#ffffff',
                'width': 1,
            }
        },
        'disabled': {
            'normal': {
                'outline': '#d9d9d9',
                'fill': '#dedede',
            },
            'over': {
                'outline': '#d9d9d9',
                'fill': '#dedede'
            },
            'click': {
                'outline': '#d9d9d9',
                'fill': '#dedede'
            }
        }
    }
}

SQUARE_WHITE_THEME['fg'] = {
    'def': {
        'class': draw.TextDraw,
        'x': 0.5,
        'y': 0.5,
        'anchor': 'center'
    },
    'states': {
        'checked': {
            'normal': {
                'text': CHECK_MARK,
                'fill': '#000000',
                'font': ('helvetica', 12, 'bold'),
            },
            'over': {
                'text': CHECK_MARK,
            },
            'click': {
                'text': CHECK_MARK,
            }
        },
        'unchecked': {
            'normal': {
                'text': '',
                'fill': '#000000',
                'font': ('helvetica', 12, 'bold'),
            },
            'over': {
                'fill': '#000000',
                'text': '',
            },
            'click': {
                'fill': '#000000',
                'text': '',
            }
        },
        'disabled': {
            'normal': {
                'fill': '#555',
            },
            'over': {
                'fill': '#555',
            },
            'click': {
                'fill': '#555',
            },
        }
    }
}

BIG_WHITE_THEME = collections.OrderedDict()
BIG_WHITE_THEME['bg'] = {
    'def': {
        'class': draw.RectangleDraw,
        'x': 0.0,
        'y': 0.0,
        'width': 0.95,
        'height': 0.95
    },
    'states': {
        'checked': {
            'normal': {
                'fill': '#dedede',
                'width': 1,
                'outline': '#d9d9d9',
            },
            'over': {
                'fill': '#dedede',
                'outline': '#d9d9d9',
                'width': 1,
            },
            'click': {
                'fill': '#dedede',
                'outline': '#d9d9d9',
                'width': 1,
            }
        },
        'unchecked': {
            'normal': {
                'fill': '#dedede',
                'width': 1,
                'outline': '#d9d9d9',
            },
            'over': {
                'outline': '#d9d9d9',
                'fill': '#dedede',
                'width': 1,
            },
            'click': {
                'outline': '#d9d9d9',
                'fill': '#dedede',
                'width': 1,
            }
        },
        'disabled': {
            'normal': {
                'outline': '#d9d9d9',
                'fill': '#dedede',
            },
            'over': {
                'outline': '#d9d9d9',
                'fill': '#dedede'
            },
            'click': {
                'outline': '#d9d9d9',
                'fill': '#dedede'
            }
        }
    }
}

BIG_WHITE_THEME['innercirle'] = {
    'def': {
        'class': draw.RectangleDraw,
        'x': 0.1,
        'y': 0.1,
        'width': 0.8,
        'height': 0.8,
    },
    'states': {
        'checked': {
            'normal': {
                'fill': '#aaaaaa',
                'width': 0,
            },
            'over': {
                'fill': '#aaaaaa',
                'width': 0,
            },
            'click': {
                'fill': '#aaaaaa',
                'width': 0,
            }
        },
        'unchecked': {
            'normal': {
                'fill': '#dedede',
                'width': 0,
            },
            'over': {
                'fill': '#dedede',
                'width': 0,
            },
            'click': {
                'fill': '#dedede',
                'width': 0,
            }
        },
        'disabled': {
            'normal': {
                'fill': '#dadada',
            },
            'over': {
                'fill': '#dadada'
            },
            'click': {
                'fill': '#dadada'
            }
        }
    }
}
