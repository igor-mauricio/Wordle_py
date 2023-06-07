theme_light = {
    "white":      ('#FFFFFF', '#FFFFFF'),
    "light":      ('#d2d0cd', '#040c13'),
    "dark":       ('#0f0b09', '#040c13'),
    "primary":    ('#3a4427', '#3d3568'),
    "secondary":  ('#626746', '#62689b'),
    "info":       ('#5e9276', '#96a4cc'),
    "accent1":    ('#484b1c', '#d9c89b'),
    "accent2":    ('#827548', '#25182e'),
    "accent3":    ('#b2aa96', '#4d4465'),
    "success":    ('#37a125', '#3c9a67'),
    "warning":    ('#f9c127', '#ddca3f'),
    "danger":     ('#ee1552', '#e53123'),
}



TITLE = 'Termo.py'
APPEARANCE_MODE = 'light'

MAIN_CONFIG = {
    'title':TITLE,
    'width':{
        'min':500,
        'start':500,
        'max':None
    },
    'height':{
        'min':630,
        'start':630,
        'max':None
    },
    'resizable':{
        'width':True,
        'height':True
    },
    'fullscreen':False,
    'icon':'images/automaniac_logo.ico',
    'theme':None,
    'color':{
        'topbar':theme_light['light'],
        'topbar_text':theme_light['dark']
    }
}