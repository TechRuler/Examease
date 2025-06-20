from tkinter import Toplevel, Entry, StringVar
from helper import CustomButton,get_json
from widget import ScrollableFrame
import os,json
class ThemeWindow(Toplevel):
    def __init__(self,master,setting,**kwarg):
        super().__init__(master,**kwarg)
        self.master = master 
        self.setting = setting 
        self.text_variable:str = StringVar()
        self.resizable(0,0)
        self.entry = Entry(self,
                           font=("Consolas",14),
                           textvariable=self.text_variable,
                           background=self.setting["Entry"]["background-color"],
                           foreground=self.setting["Entry"]["foreground-color"],
                           insertbackground=self.setting["Entry"]["foreground-color"],
                           width=30)
        self.entry.pack(fill='x')
        self.text_variable.set(os.path.basename(self.master.account["selected-theme"]).split('.')[0])
        self.config(bg=self.setting["App"]["secondary-background-color"])
        self.scroll_frame = ScrollableFrame(self)
        self.scroll_frame.canvas.config(bg=self.setting["App"]["secondary-background-color"])
        self.scroll_frame.scrollable_frame.config(bg=self.setting["App"]["secondary-background-color"])
        self.scroll_frame.pack(expand=True,fill='both')
        self.path:str = ''
        self.themes:list[str] = []
        self.master.dropdown.hide()
        self.list_themes_name("./theme")
        # print(self.themes)
        self.add_themes()
    def list_themes_name(self,path:str):
        self.path:str = path
        for name in os.listdir(self.path):
            self.themes.append(name)
    def add_themes(self):
        for name in self.themes:
            if name == os.path.basename(self.master.account["selected-theme"]):
                button = CustomButton(self.scroll_frame.scrollable_frame,
                                  text=f"{name.split('.')[0]} (current)",
                                  background=self.setting["Button"]["background-color"],
                                  foreground=self.setting["Button"]["foreground-color"],
                                  font=self.setting["Button"]["font"],
                                  relief=self.setting["Button"]["relief"],
                                  cursor="hand2",
                                  width=30,
                                  pady=5,
                                  padx=5,
                                  anchor="w",
                                  borderwidth=0
                )
                button.pack(fill='x')
                button.add_command(command=lambda j=name:self.change_setting(j))
                button.hover(self.setting["Button"]["button-hover"],self.setting["Button"]["background-color"],button)
            else:
                button = CustomButton(self.scroll_frame.scrollable_frame,
                                    text=name.split('.')[0],
                                    background=self.setting["Button"]["background-color"],
                                    foreground=self.setting["Button"]["foreground-color"],
                                    font=self.setting["Button"]["font"],
                                    relief=self.setting["Button"]["relief"],
                                    cursor="hand2",
                                    width=30,
                                    pady=5,
                                    padx=5,
                                    anchor="w",
                                    borderwidth=0
                )
                button.hover(self.setting["Button"]["button-hover"],self.setting["Button"]["background-color"],button)
                button.pack(fill='x')
                button.add_command(command=lambda j=name:self.change_setting(j))
    def change_setting(self,name:str):
        self.master.setting = get_json(os.path.join(self.path,name))
        for data in self.master.accounts:
            data["selected-theme"] = f"{self.path}/{name}"
        with open("data/accounts.json",'w') as file:
            data = json.dump(self.master.accounts,file,indent=4)
        self.master.change_color()
        self.destroy()

        
