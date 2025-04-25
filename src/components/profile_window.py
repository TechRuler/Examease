from tkinter import Toplevel,Frame,Label
import os 
class ProfileWindow(Toplevel):
    def __init__(self,master,setting,**kwarg):
        super().__init__(master,**kwarg)
        self.setting = setting
        self.resizable(0,0)
        self.maxsize(400,400)
        self.config(background=self.setting["App"]["primary-background-color"])
        profile_container = Frame(self,background=self.setting["App"]["primary-background-color"])
        profile_container.pack(padx=(50,50),pady=(50,50))

        id_label = Label(
            profile_container,
            text=f"User ID :- {self.master.account["id"]}",
            background=self.setting["Label"]["background-color"],
            foreground=self.setting["Label"]["foreground-color"],
            font=self.setting["Label"]["font"],
            borderwidth=self.setting["Label"]["border-width"],
            anchor='w',
            justify='left',
            width=30,
            padx=10,
            wraplength=300
        )
        name_label = Label(
            profile_container,
            text=f"Name :- {self.master.account["name"]}",
            background=self.setting["Label"]["background-color"],
            foreground=self.setting["Label"]["foreground-color"],
            font=self.setting["Label"]["font"],
            borderwidth=self.setting["Label"]["border-width"],
            anchor='w',
            justify='left',
            width=30,
            padx=10,
            wraplength=300
        )
        age_label = Label(
            profile_container,
            text=f"Age :- {self.master.account["age"]}",
            background=self.setting["Label"]["background-color"],
            foreground=self.setting["Label"]["foreground-color"],
            font=self.setting["Label"]["font"],
            borderwidth=self.setting["Label"]["border-width"],
            anchor='w',
            justify='left',
            width=30,
            padx=10,
            wraplength=300
        )
        theme_label = Label(
            profile_container,
            text=f"Current Theme :- {os.path.basename(self.master.account["selected-theme"]).split('.')[0]}",
            background=self.setting["Label"]["background-color"],
            foreground=self.setting["Label"]["foreground-color"],
            font=self.setting["Label"]["font"],
            borderwidth=self.setting["Label"]["border-width"],
            anchor='w',
            justify='left',
            width=30,
            padx=10,
            wraplength=300
        )
        password_label = Label(
            profile_container,
            text=f"Password :- {self.master.account["password"]}",
            background=self.setting["Label"]["background-color"],
            foreground=self.setting["Label"]["foreground-color"],
            font=self.setting["Label"]["font"],
            borderwidth=self.setting["Label"]["border-width"],
            anchor='w',
            justify='left',
            width=30,
            padx=10,
            wraplength=300
        )
        path_label = Label(
            profile_container,
            text=f"folder path :- {self.master.account["path"]}",
            background=self.setting["Label"]["background-color"],
            foreground=self.setting["Label"]["foreground-color"],
            font=self.setting["Label"]["font"],
            borderwidth=self.setting["Label"]["border-width"],
            anchor='w',
            justify='left',
            width=30,
            padx=10,
            wraplength=300
        )
        number_of_papers_label = Label(
            profile_container,
            text=f"Number of papers :- {self.master.account["number-of-papers"]}",
            background=self.setting["Label"]["background-color"],
            foreground=self.setting["Label"]["foreground-color"],
            font=self.setting["Label"]["font"],
            borderwidth=self.setting["Label"]["border-width"],
            anchor='w',
            justify='left',
            width=30,
            padx=10,
            wraplength=300
        )
        id_label.pack()
        id_label.pack_propagate(0)
        name_label.pack()
        name_label.pack_propagate(0)
        age_label.pack()
        age_label.pack_propagate(0)
        theme_label.pack()
        theme_label.pack_propagate(0)
        password_label.pack()
        password_label.pack_propagate(0)
        path_label.pack()
        path_label.pack_propagate(0)
        number_of_papers_label.pack()
        number_of_papers_label.pack_propagate(0)

        self.master.dropdown.hide()