import customtkinter as ctk
import tkinter as tk
from configuration import MAIN_CONFIG, theme_light
from graphics_scripts import BaseWindow
from process import guess, generate_word, in_database
from words import words
import string


class App(BaseWindow):
    def __init__(self, config):
        global word, current_guess
        super().__init__(config)

        self.create_components()
        self.set_layout()

        word = generate_word(words)
        current_guess = 0
        
        

        self.mainloop()

    def create_components(self):
        font_title = ctk.CTkFont(family='Lemon/Milk light', size=40)
        font_button = ctk.CTkFont(family='Lemon/Milk light', size=20)
        font_credits = ctk.CTkFont(family=None, size=12)
        self.title_label = ctk.CTkLabel(self, text="Termo.py", text_color=theme_light['dark'], font=font_title, bg_color=theme_light['light'])
        self.guesses_matrix = GuessesMatrix(self)
        self.palpite = ctk.CTkButton(self,
                                     text="Dar palpite", 
                                     command=self.on_button_clicked,
                                     corner_radius=5, 
                                     text_color=theme_light['light'], 
                                     fg_color= theme_light['accent2'],
                                     font=font_button,
                                     hover_color= theme_light['accent1'],
                                     )
        self.credits = ctk.CTkLabel(self, text="by Igor M. in 2023  ", text_color=theme_light['accent2'], font=font_credits, bg_color=theme_light['light'])


    def set_layout(self):
        self.title_label.pack(pady=10)
        self.guesses_matrix.pack()
        self.palpite.pack(ipadx=5,ipady=5, padx=10, pady=20)
        self.credits.place(relx=1, rely=1, anchor='se')
        
    
    def on_button_clicked(self):
        global current_guess, word
        guesses = list(self.guesses_matrix.string_vars[current_guess][col].get() for col in range(5))
        if '' in guesses:
            tk.messagebox.showerror(title="Erro", message="Preencha os campos!")
            return
        str_guesses = str.join('',guesses)
        if not in_database(str_guesses, words):
            tk.messagebox.showerror(title="Erro", message="A palavra não existe!")
            return
        print(word)
        print(guesses)
        print(str_guesses)

        result = guess(str_guesses, word)
        self.guesses_matrix.set_border_colors(result)
        victory = self.check_victory(result)
        if not victory and current_guess < len(self.guesses_matrix.string_vars)-1:
            self.guesses_matrix.change_row(current_guess+1)
        elif victory:
            tk.messagebox.showinfo(title="Vitória", message=f"Você ganhou! A palavra era {word}")
            self.guesses_matrix.lock_row(current_guess)
            self.set_replay_button()
        else:
            tk.messagebox.showinfo(title="Derrota", message=f"Você perdeu! A palavra era {word}")
            self.guesses_matrix.lock_row(current_guess)
            self.set_replay_button()


    def check_victory(self, result):
        return not ('position' in result or 'wrong' in result)

    def set_replay_button(self):
        def reset():
            global word, current_guess
            word = generate_word(words)
            current_guess = 0
            self.guesses_matrix.reset()
            self.palpite.configure(text="Dar palpite", command=self.on_button_clicked)
        self.palpite.configure(text="Reiniciar", command=reset)




    

class GuessesMatrix(ctk.CTkFrame):
    def __init__(self, *arg, **argv):
        super().__init__(*arg, **argv)

        self.create_components()
        self.set_layout()        
    
    def create_components(self):
        self.string_vars = []
        self.fields = []
        
        def character_limit(entry_text, row, col):
            if len(entry_text.get()) > 0:
                char=entry_text.get()[-1].upper()
                if not char in string.ascii_uppercase:
                    entry_text.set('')
                    return
                
                entry_text.set(char)
                if col+1<5:
                    if len(self.string_vars[row][col+1].get()) == 0:
                        self.fields[row][col+1].focus_set()
                    else:
                        handle_unfocus(row, col)
                else:
                    handle_unfocus(row, col)
            # else:
            #     if col > 0 and len(self.string_vars[row][col-1].get()) > 0:
            #         self.fields[row][col-1].focus_set()
    
                    
        def handle_focus(row, col):
            self.fields[row][col].configure(border_color = theme_light['accent1'])
            self.string_vars[row][col].set('')
            for i_col in range(5):
                if i_col != col:
                    self.fields[row][i_col].configure(border_color = theme_light['accent2'])

        def handle_unfocus(row, col):
            self.focus_set()
            self.fields[row][col].configure(border_color = theme_light['accent2'])


        for row in range(6):
            self.string_vars.append([])
            self.fields.append([])
            for col in range(5):
                self.string_vars[row].append(ctk.StringVar())
                font = ctk.CTkFont(family='Lemon/Milk', size=50, weight='bold')
                self.fields[row].append(ctk.CTkEntry(self, 
                                                     width=70, 
                                                     height=70, 
                                                     corner_radius=5, 
                                                     text_color=theme_light['light'], 
                                                     fg_color= theme_light['secondary'] if row>0 else theme_light['accent2'],
                                                     font=font,
                                                     justify='center',
                                                     textvariable=self.string_vars[row][col],
                                                     insertontime=0,
                                                     state='disabled' if row>0 else 'normal',
                                                     border_width=5,
                                                     border_color =  theme_light['secondary'] if row>0 else theme_light['accent2'],


                                                     ))
                
                self.string_vars[row][col].trace("w", lambda *args, row=row, col=col: character_limit(self.string_vars[row][col], row, col))
                self.fields[row][col].bind("<FocusIn>", lambda *args, row=row, col=col:handle_focus(row, col))
    def set_layout(self):
        self.rowconfigure((0, 1, 2, 3, 4, 5), weight=1, uniform = 'a')
        self.columnconfigure((0, 1, 2, 3, 4), weight=1, uniform = 'a')
        for row in range(6):
            for col in range(5):
                self.fields[row][col].grid(row=row, column=col, padx=5, pady=5, sticky='nsew')

        # ctk.CTkFrame()
        self.configure(fg_color = theme_light['accent3'])

    def set_border_colors(self, result):
        for i in range(len(word)):
            if result[i] == 'right':
                self.fields[current_guess][i].configure(border_color =  theme_light['success'])
            elif result[i] == 'position':
                self.fields[current_guess][i].configure(border_color =  theme_light['warning'])
            else:
                self.fields[current_guess][i].configure(border_color =  theme_light['danger'])

    def change_row(self, row):
        global current_guess
        for col in range(len(self.string_vars[0])):
            self.fields[current_guess][col].configure(fg_color= theme_light['secondary'], state='disabled')
        for col in range(len(self.string_vars[0])):
            self.fields[row][col].configure(fg_color= theme_light['accent2'], 
                                            state='normal', 
                                            border_color = theme_light['accent2'])

        current_guess = row
    
    def lock_row(self, row):
        for col in range(len(self.string_vars[0])):
            self.fields[row][col].configure(state='disabled')

    def reset(self):
        for row in range(6):
            for col in range(5):
                if row == 0:
                    self.fields[row][col].configure(fg_color= theme_light['accent2'], 
                                                    state='normal', 
                                                    border_color = theme_light['accent2'])
                else:
                    self.fields[row][col].configure(fg_color= theme_light['secondary'],
                                                    state='disabled',
                                                    border_color = theme_light['secondary'])

                self.string_vars[row][col].set('')




if __name__ == '__main__':
    App(MAIN_CONFIG)