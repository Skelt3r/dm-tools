from tkinter import Canvas, Frame, Scrollbar


class ScrollFrame(Frame):
    def __init__(self, frame, width=28):
        self.scrollbar = Scrollbar(frame, width=width)
        self.canvas = Canvas(frame, bg='black', yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side='right', fill='y', expand=False)
        self.canvas.pack(side='top', fill='both', expand=True)

        self.scrollbar.config(command=self.canvas.yview)
        self.canvas.bind('<Configure>', self.fill_canvas)
        Frame.__init__(self, frame)
        self.windows_item = self.canvas.create_window(0, 0, window=self, anchor='nw')


    def fill_canvas(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.windows_item, width=canvas_width)


    def update(self):
        self.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox(self.windows_item))
