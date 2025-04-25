from tkinter import*
from .auto_scrollbar import AutoScrollbar
class ScrollableFrame(Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.canvas = Canvas(self,bd=0, highlightthickness=0)
        self.scrollbar = AutoScrollbar (self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas_window =self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind(
            "<Configure>",
            lambda event: self.canvas.itemconfig(self.canvas_window,width=event.width)
        )
        self.scrollbar.grid(row=0,column=1,sticky="ns")
        self.canvas.grid(row=0,column=0,sticky="nsew")
        
        self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=1)

        # Bind mousewheel events
        self.scrollable_frame.bind("<Enter>", self._bind_mousewheel)
        self.scrollable_frame.bind("<Leave>", self._unbind_mousewheel)

        self.master.bind("<Enter>", self._bind_mousewheel)
        self.master.bind("<Leave>", self._unbind_mousewheel)
    
    def _bind_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        current_y = self.canvas.yview()
        if event.delta > 0:  # Mouse wheel up
            if current_y[0] > 0:
                self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        elif event.delta < 0:  # Mouse wheel down
            if current_y[1] < 1:
                self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
if __name__ == '__main__':
    # Usage
    root = Tk()
    root.geometry("400x400")

    scroll_frame = ScrollableFrame(root)
    scroll_frame.pack(fill="both", expand=True)

    for i in range(50):
        Label(scroll_frame.scrollable_frame,bg='red', text=f"Label {i}",anchor='').pack(fill='x',expand=True)

    root.mainloop()
