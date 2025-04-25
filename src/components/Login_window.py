from tkinter import Toplevel,Frame,Label,Entry
from helper import CustomButton
import json

class Login(Toplevel):
    def __init__(self,master,setting,**kwarg):
        super().__init__(master,**kwarg)
        self.setting = setting
        self.config(background=self.setting["App"]["primary-background-color"])
        self.geometry("400x400")
        self.resizable(0,0)
        login_window = Frame(
            self,
            background=self.setting["App"]["secondary-background-color"]
        )
        login_window.pack(padx=50, pady=50)
        login_window.pack_propagate(0)
        login_window.config(width=300, height=300) 

        id_label = Label(
            login_window,
            text="Enter ID:",
            background=self.setting["Label"]["background-color"],
            foreground=self.setting["Label"]["foreground-color"],
            font=self.setting["Label"]["font"],
            borderwidth=self.setting["Label"]["border-width"],
            anchor='w',
            justify='left'
        )
        id_label.pack(fill='x',padx=10, pady=(10,0))

        id_entry = Entry(
            login_window,
            background=self.setting["Entry"]["background-color"],
            foreground=self.setting["Entry"]["foreground-color"],
            font=self.setting["Entry"]["font"],
            borderwidth=self.setting["Entry"]["border-width"],
            insertbackground=self.setting["Entry"]["foreground-color"]
        )
        id_entry.pack(fill='x',padx=(10,10),pady=(0,10))

        name_label = Label(
            login_window,
            text="Enter Name:",
            background=self.setting["Label"]["background-color"],
            foreground=self.setting["Label"]["foreground-color"],
            font=self.setting["Label"]["font"],
            borderwidth=self.setting["Label"]["border-width"],
            anchor='w',
            justify='left'
        )
        name_label.pack(fill='x',padx=10, pady=(10,0))

        name_entry = Entry(
            login_window,
            background=self.setting["Entry"]["background-color"],
            foreground=self.setting["Entry"]["foreground-color"],
            font=self.setting["Entry"]["font"],
            borderwidth=self.setting["Entry"]["border-width"],
            insertbackground=self.setting["Entry"]["foreground-color"]
        )
        name_entry.pack(fill='x',padx=(10,10),pady=(0,10))

        age_label = Label(
            login_window,
            text="Enter Age:",
            background=self.setting["Label"]["background-color"],
            foreground=self.setting["Label"]["foreground-color"],
            font=self.setting["Label"]["font"],
            borderwidth=self.setting["Label"]["border-width"],
            anchor='w',
            justify='left'
        )
        age_label.pack(fill='x',padx=10, pady=(10,0))

        age_entry = Entry(
            login_window,
            background=self.setting["Entry"]["background-color"],
            foreground=self.setting["Entry"]["foreground-color"],
            font=self.setting["Entry"]["font"],
            borderwidth=self.setting["Entry"]["border-width"],
            insertbackground=self.setting["Entry"]["foreground-color"]
        )
        age_entry.pack(fill='x',padx=(10,10),pady=(0,10))

        
        password_label = Label(
            login_window,
            text="Enter Pasword:",
            background=self.setting["Label"]["background-color"],
            foreground=self.setting["Label"]["foreground-color"],
            font=self.setting["Label"]["font"],
            borderwidth=self.setting["Label"]["border-width"],
            anchor='w',
            justify='left'
        )
        password_label.pack(fill='x',padx=10, pady=(10,0))

        password_entry = Entry(
            login_window,
            background=self.setting["Entry"]["background-color"],
            foreground=self.setting["Entry"]["foreground-color"],
            font=self.setting["Entry"]["font"],
            borderwidth=self.setting["Entry"]["border-width"],
            insertbackground=self.setting["Entry"]["foreground-color"]
        )
        password_entry.pack(fill='x',padx=(10,10),pady=(0,10))

        login_button_frame = Frame(login_window,background=self.setting["App"]["secondary-background-color"])
        login_button_frame.pack(fill='x')
        login_button = CustomButton(
            login_button_frame,
            text="Login",
            background=self.setting["Button"]["background-color"],
            foreground=self.setting["Button"]["foreground-color"],
            font=self.setting["Button"]["font"],
            relief=self.setting["Button"]["relief"],
            cursor="hand2",
            pady=5,
            padx=5,
            command=lambda:self.creating_new_account(id_entry.get(),name_entry.get(),age_entry.get(),password_entry.get())
        )
        login_button.pack(side='left',padx=(10,0))


        login_if_already = CustomButton(
            login_button_frame,
            text="I have an account",
            background=self.setting["Button"]["background-color"],
            foreground=self.setting["Button"]["foreground-color"],
            font=self.setting["Button"]["font"],
            relief=self.setting["Button"]["relief"],
            cursor="hand2",
            pady=5,
            padx=5,
            command=self.change_to_switch_account)
        
        login_if_already.pack(side='right',padx=(0,10))
    def creating_new_account(self,id,name,age,password):
        data = {
            "id": id,
            "name": name,
            "selected": 1,
            "age": age,
            "password":password,
            "path": f"src/{id}-papers",
            "number-of-papers": 0,
            "papers-dictionary": []
        }
        for account in self.master.accounts:
            if account["selected"] == 1:
                account["selected"] = 0
        self.master.accounts.append(data)
        with open("src/accounts.json","w") as f:
            json.dump(self.master.accounts,f,indent=4)
        for element in self.master.element_list:
            element.pack_forget()
        self.master.account = self.master.check_ids()
        userid =  "Login" if self.master.account is None else self.master.account.get("id", "Unknown")
        self.master.profile_label.config(text=userid)
        self.master.check_paper_exist()
        self.destroy()
    def change_to_switch_account(self):
        from .switch_account_window import SwitchAccount
        SwitchAccount(self.master,self.setting)
        self.destroy()