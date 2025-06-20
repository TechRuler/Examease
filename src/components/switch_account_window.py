from tkinter import Toplevel,Frame, Label
from helper import CustomButton
import json
class SwitchAccount(Toplevel):
    def __init__(self,master,setting,**kwarg):
        super().__init__(master,**kwarg)
        self.setting = setting
        self.config(background=self.setting["App"]["primary-background-color"])
        account_cantainer = Frame(self,background=self.setting["App"]["primary-background-color"])
        account_cantainer.pack(padx=(50,50),pady=(50,50))
        account_label = Label(
            account_cantainer,
            text="Accounts",
            background=self.setting["Button"]["background-color"],
            foreground=self.setting["Button"]["foreground-color"],
            font=self.setting["Button"]["font"],
            padx=5,
            pady=5,
            anchor='w',
            justify='left'
        )
        account_label.pack(fill='x')
        for account in self.master.accounts:
            if account["selected"] == 1:
                button = CustomButton(
                    account_cantainer,
                    text=f"{account["id"]} (current)",
                    background=self.setting["Button"]["background-color"],
                    foreground=self.setting["Button"]["foreground-color"],
                    font=self.setting["Button"]["font"],
                    relief=self.setting["Button"]["relief"],
                    cursor="hand2",
                    padx=5,
                    pady=5,
                    width=30,
                    command=lambda j=account["id"]:self.switch_account_function(j)
                )
            else:
                button = CustomButton(
                    account_cantainer,
                    text=account["id"],
                    background=self.setting["Button"]["background-color"],
                    foreground=self.setting["Button"]["foreground-color"],
                    font=self.setting["Button"]["font"],
                    relief=self.setting["Button"]["relief"],
                    cursor="hand2",
                    padx=5,
                    pady=5,
                    width=30,
                    command=lambda j=account["id"]:self.switch_account_function(j)
                )
            button.pack()
            button.pack_propagate(0)
        create_new_account = CustomButton(
                    self,
                    text="click here to create new account",
                    background=self.setting["App"]["primary-background-color"],
                    foreground=self.setting["Button"]["foreground-color"],
                    font=self.setting["Button"]["font"],
                    relief=self.setting["Button"]["relief"],
                    cursor="hand2",
                    borderwidth=0,
                    padx=5,
                    pady=5,
                    width=30,
                    command=self.change_to_login_window
        )
        create_new_account.pack(fill='x')
        self.master.dropdown.hide()
    def switch_account_function(self,id):
        for account in self.master.accounts:
            if account["id"] == id:
                account["selected"] = 1 
            else: 
                account["selected"] = 0
        with open("data/accounts.json","w") as f:
            json.dump(self.master.accounts,f,indent=4)
        for element in self.master.element_list:
            element.pack_forget()
        self.master.account = self.master.check_ids()
        print(self.master.account["selected-theme"])
        userid =  "Login" if self.master.account is None else self.master.account.get("id", "Unknown")
        self.master.profile_label.config(text=userid)
        self.master.check_paper_exist()
        self.master.change_color()
        self.destroy()
    def change_to_login_window(self):
        from .Login_window import Login
        Login(self.master,self.setting)
        self.destroy()