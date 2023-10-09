import customtkinter as ctk
import tkinter as tk
from configuration import *
try:
    from ctypes import windll, byref, sizeof, c_int
except ImportError:
    print('Error importing ctypes')


def colors_decorator(func):
    def wrapper(window, bar_colors, text_colors):
        bar_color = color_by_mode(bar_colors)
        text_color = color_by_mode(text_colors)
        func(window, bar_color, text_color)
    return wrapper

@colors_decorator
def change_title_bar_color(window, bar_color, text_color):
    def str_to_hex(hex_str):
        rgb_hex = hex_str[1:]
        bgr_hex = rgb_hex[4:] + rgb_hex[2:4] + rgb_hex[:2]

        return int(bgr_hex, base=16)
        
    try:
        window.update()
        HWND = windll.user32.GetParent(window.winfo_id())
        DWNA_ATTRIBUTE_BAR_COLOR = 35
        DWNA_ATTRIBUTE_TEXT_COLOR = 36
        hex_bar_color = str_to_hex(bar_color)
        hex_text_color = str_to_hex(text_color)
        
        windll.dwmapi.DwmSetWindowAttribute(
            HWND, 
            DWNA_ATTRIBUTE_BAR_COLOR, 
            byref(c_int(hex_bar_color)), 
            sizeof(c_int)
        )
        
        windll.dwmapi.DwmSetWindowAttribute(
            HWND, 
            DWNA_ATTRIBUTE_TEXT_COLOR, 
            byref(c_int(hex_text_color)), 
            sizeof(c_int)
        )
    except Exception as e:
        print(e)


# def get_color(theme, label):
#     style = ttk.Style(theme=theme)
#     return style.colors.get(label)


def centered_window_geometry(window, window_config):
    return f"{window_config['width']['start']}x{window_config['height']['start']}+{window.winfo_screenwidth()/2 -window_config['width']['start']/2:.0f}+{window.winfo_screenheight()/2-window_config['height']['start']/2:.0f}"


class BaseWindow(ctk.CTk):
    def __init__(self, config):
        super().__init__()
        if config['title']:
            self.title(config['title'])
        if config['height']['start'] and config['width']['start']:    
            self.geometry(centered_window_geometry(self, config))
        if config['height']['min'] and config['width']['min']:
            self.minsize(config['width']['min'], config['height']['min'])
        if config['height']['max'] and config['width']['max']:
            self.maxsize(config['width']['max'],  config['height']['max'])
        try:
            self.iconbitmap(config['icon'])
        except:
            pass
        if APPEARANCE_MODE in ["system", "dark", "light"]:
            ctk.set_appearance_mode(APPEARANCE_MODE)

        self.resizable(width = config['resizable']['width'], height = config['resizable']['height'])
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        change_title_bar_color(self, bar_colors=config['color']['topbar'], text_colors=config['color']['topbar_text'])

        self.config(bg=color_by_mode(config['color']['topbar']))

    def on_closing(self):
        if tk.messagebox.askokcancel("sair", "Você quer mesmo sair?"):
            self.quit()

def color_by_mode(colors):
    if ctk.get_appearance_mode() == "Light":
        return colors[0]
    else:
        return colors[1]
    
        


# change_title_bar_color(window, get_color('flatly', 'primary'), get_color('flatly', 'secondary'))
