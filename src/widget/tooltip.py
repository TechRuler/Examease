from tkinter import Label
class Tooltip:
    def __init__(self,master) -> None:
        self.master = master
        self.bg = None
        self.fg = None
        self.border = None 
        self.font = None 
    def create_tooltip(self,widget,text:str, bg:str='yellow', fg:str="black", border:int=1, font:tuple[str|int]=('Consolas',10)) -> None:
        self.bg = bg 
        self.fg = fg
        self.border = border 
        self.font = font 
        tooltip = Label(self.master,text=text,background=self.bg, fg=self.fg,relief="solid",borderwidth=self.border,font=self.font)

       
        widget.bind(
            "<Enter>",
            lambda e: tooltip.place(
                x=e.x_root - self.master.winfo_rootx(),
                y=e.y_root - self.master.winfo_rooty()
            )
        )
        widget.bind("<Leave>", lambda _: tooltip.place_forget())

if __name__ == "__main__":
    from tkinter import Tk 
    root:Tk = Tk()

    label:Label = Label(root, text='Text')
    label.pack()

    tooltip:Tooltip = Tooltip(root)
    tooltip.create_tooltip(label, 'This is the label here!')
    root.mainloop()