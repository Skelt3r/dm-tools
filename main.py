from PIL import Image, ImageTk
from random import randint
from tkinter import Button, Entry, Frame, Label, messagebox, Text, Tk, Toplevel
from utils import ScrollFrame


class Tracker:
    def __init__(self):
        self.height = 4
        self.width = 8

        self.bg_color = 'black'
        self.fg_color = 'white'
        
        self.button_font = ('Arial', 16, 'bold')
        self.large_button_font = ('Arial', 28, 'bold')
        self.header_font = ('Arial', 16, 'bold', 'underline')

        self.board = list()
        self.num_players = 4
        self.resolution = '1460x940'


    def main(self):

        def roll_dice(sides, label):
            label['text'] = randint(1, sides)


        def set_value(button, prompt, int_only=False):

            def ok(event=None):
                if int_only:
                    try:
                        button.config(text=int(text_entry.get()))
                        win.destroy()
                    except ValueError:
                        messagebox.showerror('Integer required', 'Value must be an integer.')
                else:
                    button.config(text=text_entry.get())
                    win.destroy()

            win = Toplevel(button)
            win.title(str())
            win.geometry('200x100+500+500')
            win.resizable(0, 0)
            win.wm_attributes('-topmost', True)
            win.wm_transient(root)

            Label(win, text=prompt).pack(anchor='c', padx=5, pady=5, side='top')

            text_entry = Entry(win)
            button_frame = Frame(win)

            text_entry.pack(anchor='c', padx=5, pady=5, side='top')
            button_frame.pack(anchor='c', side='top')

            Button(button_frame, text='OK', command=ok).pack(anchor='c', padx=5, pady=5, side='left')
            Button(button_frame, text='Cancel', command=lambda: win.destroy()).pack(anchor='c', padx=5, pady=5, side='left')

            text_entry.focus()
            text_entry.bind('<Return>', ok)
            text_entry.bind('<Escape>', lambda _: win.destroy())


        def add_player(num):

            def move_up(temp_frame):
                for row in self.board:
                    if row[0] == temp_frame:
                        index = self.board.index(row)
                        if index != 0:
                            temp_frame.pack(before=self.board[index-1][0])
                            self.board.remove(row)
                            self.board.insert(index-1, row)
                            break
            

            def move_down(temp_frame):
                for row in self.board:
                    if row[0] == temp_frame:
                        index = self.board.index(row)
                        if index < len(self.board)-1:
                            temp_frame.pack(after=self.board[index+1][0])
                            self.board.remove(row)
                            self.board.insert(index+1, row)
                            break


            temp_frame = Frame(scoreboard_frame, bg=self.bg_color)
            arrow_frame = Frame(temp_frame, bg=self.bg_color)

            up_arrow = Button(arrow_frame, command=lambda tf=temp_frame: move_up(tf), bg=self.bg_color, fg=self.fg_color, text='▲')
            down_arrow = Button(arrow_frame, command=lambda tf=temp_frame: move_down(tf), bg=self.bg_color, fg=self.fg_color, text='▼')
            init_button = Button(temp_frame, bg=self.bg_color, fg=self.fg_color, height=self.height, width=self.width, font=self.button_font, text=0)
            name_button = Button(temp_frame, bg=self.bg_color, fg=self.fg_color, height=self.height, width=self.width*2, font=self.button_font, text=f'Character {num}')
            hp_button = Button(temp_frame, bg=self.bg_color, fg=self.fg_color, height=self.height, width=self.width, font=self.button_font, text=0)
            ac_button = Button(temp_frame, bg=self.bg_color, fg=self.fg_color, height=self.height, width=self.width, font=self.button_font, text=0)
            x_button = Button(temp_frame, command=lambda tf=temp_frame: remove_player(tf), bg=self.bg_color, fg=self.fg_color, bd=2, relief='ridge', font=self.button_font, text='X', padx=10, pady=5)
            
            notes_entry = Text(temp_frame, bd=4, relief='ridge', bg=self.bg_color, fg=self.fg_color, insertbackground=self.fg_color, padx=5, pady=5, height=self.height, width=self.width*6, font=self.button_font)

            init_button.config(command=lambda b=init_button: set_value(b, 'Enter an initiative value', True))
            name_button.config(command=lambda b=name_button: set_value(b, 'Enter a character name:'))
            hp_button.config(command=lambda b=hp_button: set_value(b, 'Enter an HP value:', True))
            ac_button.config(command=lambda b=ac_button: set_value(b, 'Enter an AC value:', True))
            
            temp_frame.pack(side='top')
            arrow_frame.pack(side='left')
            up_arrow.pack(side='top', padx=5)
            down_arrow.pack(side='top', padx=5)
            init_button.pack(side='left')
            name_button.pack(side='left')
            hp_button.pack(side='left')
            ac_button.pack(side='left')
            notes_entry.pack(side='left')
            x_button.pack(side='left', anchor='c', padx=5)

            scrollframe.update()

            self.board.extend([[temp_frame, init_button, name_button, hp_button, ac_button, notes_entry, x_button]])
            self.num_players = num+1
        

        def remove_player(temp_frame):
            for row in self.board:
                if row[0] == temp_frame:
                    temp_frame.destroy()
                    self.board.remove(row)
                    scrollframe.update()
                    break


        def reset():
            for row in self.board:
                row[1]['text'] = 0
            

        root = Tk()
        root.title('DM Tools')
        root.geometry(self.resolution)
        root.iconphoto(True, ImageTk.PhotoImage(file='./images/d20.png'))
        root.configure(bg=self.bg_color)

        bg_frame = Frame(root, bg=self.bg_color)
        dice_frame = Frame(bg_frame, bg=self.bg_color)
        header_frame = Frame(bg_frame, bg=self.bg_color, padx=15)

        bg_frame.pack(expand=True, fill='both')
        dice_frame.pack(side='left', padx=10)
        header_frame.pack(side='top')

        scrollframe = ScrollFrame(bg_frame)
        scoreboard_frame = Frame(scrollframe, bg=self.bg_color, pady=10)
        button_frame = Frame(root, bg=self.bg_color)

        d20_image = ImageTk.PhotoImage(Image.open('./images/d20.png').resize((100, 100)), master=dice_frame)
        d12_image = ImageTk.PhotoImage(Image.open('./images/d12.png').resize((100, 100)), master=dice_frame)
        d8_image = ImageTk.PhotoImage(Image.open('./images/d8.png').resize((100, 100)), master=dice_frame)
        d6_image = ImageTk.PhotoImage(Image.open('./images/d6.png').resize((100, 100)), master=dice_frame)
        d4_image = ImageTk.PhotoImage(Image.open('./images/d4.png').resize((100, 100)), master=dice_frame)

        d20_button = Button(dice_frame, command=lambda: roll_dice(20, d20_label), bg=self.bg_color, image=d20_image)
        d12_button = Button(dice_frame, command=lambda: roll_dice(12, d12_label), bg=self.bg_color, image=d12_image)
        d8_button = Button(dice_frame, command=lambda: roll_dice(8, d8_label), bg=self.bg_color, image=d8_image)
        d6_button = Button(dice_frame, command=lambda: roll_dice(6, d6_label), bg=self.bg_color, image=d6_image)
        d4_button = Button(dice_frame, command=lambda: roll_dice(4, d4_label), bg=self.bg_color, image=d4_image)
        
        add_button = Button(button_frame, command=lambda: add_player(self.num_players), bg=self.bg_color, fg=self.fg_color, bd=5, relief='ridge', font=self.large_button_font, text='Add Character', pady=5)
        reset_button = Button(button_frame, command=lambda: reset(), bg=self.bg_color, fg=self.fg_color, bd=5, relief='ridge', font=self.large_button_font, text='Reset Initiative', pady=5)

        d20_label = Label(dice_frame, bg=self.bg_color, fg=self.fg_color, bd=2, relief='ridge', font=self.button_font, text='-', width=8)
        d12_label = Label(dice_frame, bg=self.bg_color, fg=self.fg_color, bd=2, relief='ridge', font=self.button_font, text='-', width=8)
        d8_label = Label(dice_frame, bg=self.bg_color, fg=self.fg_color, bd=2, relief='ridge', font=self.button_font, text='-', width=8)
        d6_label = Label(dice_frame, bg=self.bg_color, fg=self.fg_color, bd=2, relief='ridge', font=self.button_font, text='-', width=8)
        d4_label = Label(dice_frame, bg=self.bg_color, fg=self.fg_color, bd=2, relief='ridge', font=self.button_font, text='-', width=8)

        init_label = Label(header_frame, bg=self.bg_color, fg=self.fg_color, height=self.height//2, width=self.width, font=self.header_font, text=f'Initiative')
        name_label = Label(header_frame, bd=4, bg=self.bg_color, fg=self.fg_color, height=self.height//2, width=self.width*2, font=self.header_font, text=f'Name')
        hp_label = Label(header_frame, bd=4, bg=self.bg_color, fg=self.fg_color, height=self.height//2, width=self.width, font=self.header_font, text=f'HP')
        ac_label = Label(header_frame, bd=4, bg=self.bg_color, fg=self.fg_color, height=self.height//2, width=self.width, font=self.header_font, text=f'AC')
        notes_label = Label(header_frame, bd=4, bg=self.bg_color, fg=self.fg_color, height=self.height//2, width=49, font=self.header_font, text=f'Notes / Conditions')

        scoreboard_frame.pack(anchor='c', expand=True, fill='both')
        button_frame.pack(side='top', fill='x', pady=10)

        d20_button.pack(pady=10)
        d20_label.pack()
        d12_button.pack(pady=10)
        d12_label.pack()
        d8_button.pack(pady=10)
        d8_label.pack()
        d6_button.pack(pady=10)
        d6_label.pack()
        d4_button.pack(pady=10)
        d4_label.pack()

        init_label.pack(side='left', anchor='s')
        name_label.pack(side='left', anchor='s')
        hp_label.pack(side='left', anchor='s')
        ac_label.pack(side='left', anchor='s')
        notes_label.pack(side='left', anchor='s')
        
        add_button.pack(side='left', anchor='c', expand=True, fill='x')
        reset_button.pack(side='left', anchor='c', expand=True, fill='x')

        for p in range(self.num_players): add_player(p+1)

        root.mainloop()
    

if __name__ == '__main__':
    tracker = Tracker()
    tracker.main()
