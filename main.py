from pickle import dump, load
from PIL import Image, ImageTk
from random import randint
from tkinter import Button, Entry, Frame, Label, messagebox, Text, Tk, Toplevel
from tkinter.filedialog import askopenfilename, asksaveasfilename
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

        self.frames = list()
        self.board = list()
        self.num_players = 4
        self.resolution = '1460x940'

        self.autoload()
    

    def autosave(self):
        with open('./saves/autosave.dat', 'wb') as savefile:
            dump(self.data, savefile)
    

    def autoload(self):
        try:
            with open('./saves/autosave.dat', 'rb') as loadfile:
                self.data = load(loadfile)
        except FileNotFoundError:
            self.data = [[0, '-', 0, 0, '']]*4

    
    def save_board(self):
        file = asksaveasfilename(confirmoverwrite=True, defaultextension='dat', filetypes=[('DAT Files', '*.dat')], initialdir='./saves')

        if file != '':
            with open(file, 'wb') as savefile:
                dump(self.data, savefile)


    def load_board(self):
        file = askopenfilename(filetypes=[('DAT Files', '*.dat')], initialdir='./saves')

        if file != '':
            for frame in self.frames:
                frame.destroy()
            
            self.frames.clear()
            self.board.clear()
            self.data.clear()

            with open(file, 'rb') as loadfile:
                self.data = load(loadfile)
        
            for row in self.data:
                self.load_character(*row)
    

    def insert_data(self, button):
        for row in self.board:
            if button in row:
                r_index = self.board.index(row)
                b_index = self.board[r_index].index(button)
                self.data[r_index][b_index] = button['text']
                break


    def set_value(self, button, prompt, int_only=False):

        def ok(event=None):
            if int_only:
                try:
                    button.config(text=int(text_entry.get()))
                    self.insert_data(button)
                    self.autosave()
                    win.destroy()
                except ValueError:
                    messagebox.showerror('Integer required', 'Value must be an integer.')
            else:
                button.config(text=text_entry.get())
                self.insert_data(button)
                self.autosave()
                win.destroy()

        win = Toplevel(button)
        win.title(str())
        win.geometry('200x100+500+500')
        win.resizable(0, 0)
        win.wm_attributes('-topmost', True)
        win.wm_transient(self.root)

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
    

    def move_up(self, temp_frame):
        for frame in self.frames:
            if frame == temp_frame:
                index = self.frames.index(frame)
                if index != 0:
                    temp_frame.pack(before=self.frames[index-1])
                    self.frames.remove(frame)
                    self.frames.insert(index-1, frame)
                    b_row = self.board.pop(index)
                    d_row = self.data.pop(index)
                    self.board.insert(index-1, b_row)
                    self.data.insert(index-1, d_row)
                    break

        self.autosave()
    

    def move_down(self, temp_frame):
        for frame in self.frames:
            if frame == temp_frame:
                index = self.frames.index(frame)
                if index < len(self.frames)-1:
                    temp_frame.pack(after=self.frames[index+1])
                    self.frames.remove(frame)
                    self.frames.insert(index+1, frame)
                    b_row = self.board.pop(index)
                    d_row = self.data.pop(index)
                    self.board.insert(index+1, b_row)
                    self.data.insert(index+1, d_row)
                    break

        self.autosave()
    
    
    def generate_character_row(self, init=0, name='-', hp=0, ac=0, notes=''):

        def save_notes(textbox):
            for row in self.board:
                if textbox in row:
                    index = self.board.index(row)
                    self.data[index][-1] = notes_textbox.get('1.0', 'end').rstrip('\n')
                    self.autosave()
                    break

        temp_frame = Frame(self.scoreboard_frame, bg=self.bg_color)
        arrow_frame = Frame(temp_frame, bg=self.bg_color)

        up_arrow = Button(arrow_frame, command=lambda tf=temp_frame: self.move_up(tf), bg=self.bg_color, fg=self.fg_color, text='▲')
        down_arrow = Button(arrow_frame, command=lambda tf=temp_frame: self.move_down(tf), bg=self.bg_color, fg=self.fg_color, text='▼')
        init_button = Button(temp_frame, bg=self.bg_color, fg=self.fg_color, height=self.height, width=self.width, font=self.button_font, text=init)
        name_button = Button(temp_frame, bg=self.bg_color, fg=self.fg_color, height=self.height, width=self.width*2, font=self.button_font, text=name)
        hp_button = Button(temp_frame, bg=self.bg_color, fg=self.fg_color, height=self.height, width=self.width, font=self.button_font, text=hp)
        ac_button = Button(temp_frame, bg=self.bg_color, fg=self.fg_color, height=self.height, width=self.width, font=self.button_font, text=ac)
        x_button = Button(temp_frame, command=lambda tf=temp_frame: self.remove_character(tf), bg=self.bg_color, fg=self.fg_color, bd=2, relief='ridge', font=self.button_font, text='X', padx=10, pady=5)
        
        notes_textbox = Text(temp_frame, bd=4, relief='ridge', bg=self.bg_color, fg=self.fg_color, insertbackground=self.fg_color, padx=5, pady=5, height=self.height, width=self.width*6, font=self.button_font)

        init_button.configure(command=lambda b=init_button: self.set_value(b, 'Enter an initiative value', True))
        name_button.configure(command=lambda b=name_button: self.set_value(b, 'Enter a character name:'))
        hp_button.configure(command=lambda b=hp_button: self.set_value(b, 'Enter an HP value:', True))
        ac_button.configure(command=lambda b=ac_button: self.set_value(b, 'Enter an AC value:', True))

        notes_textbox.insert('1.0', notes)
        notes_textbox.bind('<KeyRelease>', lambda _, t=notes_textbox: save_notes(t))
        
        temp_frame.pack(side='top')
        arrow_frame.pack(side='left')
        up_arrow.pack(side='top', padx=5)
        down_arrow.pack(side='top', padx=5)
        init_button.pack(side='left')
        name_button.pack(side='left')
        hp_button.pack(side='left')
        ac_button.pack(side='left')
        notes_textbox.pack(side='left')
        x_button.pack(side='left', anchor='c', padx=5)

        self.scrollframe.update()

        return [temp_frame, init_button, name_button, hp_button, ac_button, notes_textbox]


    def add_character(self, init=0, name='-', hp=0, ac=0, notes=''):
        widgets = self.generate_character_row(init, name, hp, ac, notes)
        self.frames.append(widgets[0])
        self.board.extend([[widgets[1], widgets[2], widgets[3], widgets[4], widgets[5]]])
        self.data.extend([[init, name, hp, ac, notes]])
        self.autosave()
    

    def load_character(self, init, name, hp, ac, notes):
        widgets = self.generate_character_row(init, name, hp, ac, notes)
        self.frames.append(widgets[0])
        self.board.extend([[widgets[1], widgets[2], widgets[3], widgets[4], widgets[5]]])


    def remove_character(self, temp_frame):
        for frame in self.frames:
            if frame == temp_frame:
                index = self.frames.index(frame)
                temp_frame.destroy()
                self.frames.remove(frame)
                self.board.pop(index)
                self.data.pop(index)
                self.scrollframe.update()
                break

        self.autosave()


    def reset(self):
        for row in self.board: row[0]['text'] = 0
        for row in self.data: row[0] = 0
        self.autosave()
    

    def roll_dice(sides, label):
        label['text'] = randint(1, sides)
    

    def main(self):
        self.root = Tk()
        self.root.title('DM Tools')
        self.root.geometry(self.resolution)
        self.root.iconphoto(True, ImageTk.PhotoImage(file='./images/d20.png'))
        self.root.configure(bg=self.bg_color)

        self.bg_frame = Frame(self.root, bg=self.bg_color)
        self.dice_frame = Frame(self.bg_frame, bg=self.bg_color)
        self.header_frame = Frame(self.bg_frame, bg=self.bg_color, padx=15)

        self.bg_frame.pack(expand=True, fill='both')
        self.dice_frame.pack(side='left', padx=10)
        self.header_frame.pack(side='top')

        self.scrollframe = ScrollFrame(self.bg_frame)
        self.scoreboard_frame = Frame(self.scrollframe, bg=self.bg_color, pady=10)
        self.button_frame = Frame(self.root, bg=self.bg_color)

        self.d20_image = ImageTk.PhotoImage(Image.open('./images/d20.png').resize((100, 100)), master=self.dice_frame)
        self.d12_image = ImageTk.PhotoImage(Image.open('./images/d12.png').resize((100, 100)), master=self.dice_frame)
        self.d8_image = ImageTk.PhotoImage(Image.open('./images/d8.png').resize((100, 100)), master=self.dice_frame)
        self.d6_image = ImageTk.PhotoImage(Image.open('./images/d6.png').resize((100, 100)), master=self.dice_frame)
        self.d4_image = ImageTk.PhotoImage(Image.open('./images/d4.png').resize((100, 100)), master=self.dice_frame)

        self.d20_button = Button(self.dice_frame, command=lambda: self.roll_dice(20, self.d20_label), bg=self.bg_color, image=self.d20_image)
        self.d12_button = Button(self.dice_frame, command=lambda: self.roll_dice(12, self.d12_label), bg=self.bg_color, image=self.d12_image)
        self.d8_button = Button(self.dice_frame, command=lambda: self.roll_dice(8, self.d8_label), bg=self.bg_color, image=self.d8_image)
        self.d6_button = Button(self.dice_frame, command=lambda: self.roll_dice(6, self.d6_label), bg=self.bg_color, image=self.d6_image)
        self.d4_button = Button(self.dice_frame, command=lambda: self.roll_dice(4, self.d4_label), bg=self.bg_color, image=self.d4_image)
        
        self.save_button = Button(self.button_frame, command=lambda: self.save_board(), bg=self.bg_color, fg=self.fg_color, bd=5, relief='ridge', font=self.large_button_font, text='Save', pady=5)
        self.load_button = Button(self.button_frame, command=lambda: self.load_board(), bg=self.bg_color, fg=self.fg_color, bd=5, relief='ridge', font=self.large_button_font, text='Load', pady=5)
        self.add_button = Button(self.button_frame, command=lambda: self.add_character(name='-'), bg=self.bg_color, fg=self.fg_color, bd=5, relief='ridge', font=self.large_button_font, text='Add Character', pady=5)
        self.reset_button = Button(self.button_frame, command=lambda: self.reset(), bg=self.bg_color, fg=self.fg_color, bd=5, relief='ridge', font=self.large_button_font, text='Reset Initiative', pady=5)

        self.d20_label = Label(self.dice_frame, bg=self.bg_color, fg=self.fg_color, bd=2, relief='ridge', font=self.button_font, text='-', width=8)
        self.d12_label = Label(self.dice_frame, bg=self.bg_color, fg=self.fg_color, bd=2, relief='ridge', font=self.button_font, text='-', width=8)
        self.d8_label = Label(self.dice_frame, bg=self.bg_color, fg=self.fg_color, bd=2, relief='ridge', font=self.button_font, text='-', width=8)
        self.d6_label = Label(self.dice_frame, bg=self.bg_color, fg=self.fg_color, bd=2, relief='ridge', font=self.button_font, text='-', width=8)
        self.d4_label = Label(self.dice_frame, bg=self.bg_color, fg=self.fg_color, bd=2, relief='ridge', font=self.button_font, text='-', width=8)

        self.init_label = Label(self.header_frame, bg=self.bg_color, fg=self.fg_color, height=self.height//2, width=self.width, font=self.header_font, text='Initiative')
        self.name_label = Label(self.header_frame, bd=4, bg=self.bg_color, fg=self.fg_color, height=self.height//2, width=self.width*2, font=self.header_font, text='Name')
        self.hp_label = Label(self.header_frame, bd=4, bg=self.bg_color, fg=self.fg_color, height=self.height//2, width=self.width, font=self.header_font, text='HP')
        self.ac_label = Label(self.header_frame, bd=4, bg=self.bg_color, fg=self.fg_color, height=self.height//2, width=self.width, font=self.header_font, text='AC')
        self.notes_label = Label(self.header_frame, bd=4, bg=self.bg_color, fg=self.fg_color, height=self.height//2, width=49, font=self.header_font, text='Notes / Conditions')

        self.scoreboard_frame.pack(anchor='c', expand=True, fill='both')
        self.button_frame.pack(side='top', fill='x', pady=10)

        self.d20_button.pack(pady=10)
        self.d20_label.pack()
        self.d12_button.pack(pady=10)
        self.d12_label.pack()
        self.d8_button.pack(pady=10)
        self.d8_label.pack()
        self.d6_button.pack(pady=10)
        self.d6_label.pack()
        self.d4_button.pack(pady=10)
        self.d4_label.pack()

        self.init_label.pack(side='left', anchor='s')
        self.name_label.pack(side='left', anchor='s')
        self.hp_label.pack(side='left', anchor='s')
        self.ac_label.pack(side='left', anchor='s')
        self.notes_label.pack(side='left', anchor='s')
        
        self.save_button.pack(side='left', anchor='c', expand=True, fill='x')
        self.load_button.pack(side='left', anchor='c', expand=True, fill='x')
        self.add_button.pack(side='left', anchor='c', expand=True, fill='x')
        self.reset_button.pack(side='left', anchor='c', expand=True, fill='x')

        for row in self.data:
            self.load_character(*row)

        self.root.mainloop()
    

if __name__ == '__main__':
    tracker = Tracker()
    tracker.main()
