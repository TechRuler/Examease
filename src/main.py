from tkinter import Tk, Frame, Label, Toplevel,Entry,Text,Scrollbar
from tkinter import messagebox
import json
import os
import random
from datetime import datetime
from helper import get_json, update_json_value,DropdownMenu,CustomButton
from exam_window import ExamWindow



        
class App(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("800x700")
        self.title("Examease")
        self.importing_all_json()
        self.element_list = []

        # Safely access settings with defaults
        app_settings = self.setting.get("App", {})
        self.config(background=app_settings["primary-background-color"])

        self.upper_frame = Frame(self, height=60, background=app_settings["secondary-background-color"])
        self.upper_frame.pack(fill='x')
        self.upper_frame.pack_propagate(0)

        app_title_settings = self.setting.get("App-title", {})
        self.app_name = Label(
            self.upper_frame,
            text="<:-)Examease(-:>",
            background=app_title_settings["background-color"],
            foreground=app_title_settings["foreground-color"],
            font=app_title_settings["font"],
            relief=app_title_settings["relief"],
            borderwidth=app_title_settings["border-width"]
        )
        self.app_name.pack(side='left', padx=(10, 5), pady=(5, 5))

        self.account = self.check_ids()
        
        self.user_id = "Login" if self.account is None else self.account.get("id", "Unknown")

        button_settings = self.setting.get("Button", {})
        self.profile_label = CustomButton(
            self.upper_frame,
            text=self.user_id,
            background=button_settings["background-color"],
            foreground=button_settings["foreground-color"],
            font=button_settings["font"],
            relief=button_settings["relief"],
            cursor="hand2",
            width=15,
            pady=5,
            padx=5,
            command=self.login_window
        )
        self.profile_label.pack(side='right', padx=(5, 10), pady=(5, 5))
        self.profile_label.pack_propagate(0)

        self.create_exam_button = CustomButton(
            self.upper_frame,
            text="Create Exam",
            background=button_settings["background-color"],
            foreground=button_settings["foreground-color"],
            font=button_settings["font"],
            relief=button_settings["relief"],
            cursor="hand2",
            pady=5,
            padx=5,
            command=self.create_exam
        )
        self.create_exam_button.pack(side='right', padx=(10, 5), pady=(5, 5))

        empty_label_settings = self.setting.get("Empty-Label", {})
        self.empty_Label = Label(
                self,
                text="No Exam conducted!",
                background=empty_label_settings["background-color"],
                foreground=empty_label_settings["foreground-color"],
                font=empty_label_settings["font"],
                relief=empty_label_settings["relief"],
                borderwidth=empty_label_settings["border-width"]
            )
        self.check_paper_exist()
        self.login_dropdown()
        
        
    def importing_all_json(self):
        try:
            self.setting = get_json("theme/App_theme.json")
        except (FileNotFoundError, ValueError) as e:
            print(f"Error loading settings: {e}")
            self.setting = {}

        try:
            self.accounts = get_json("src/accounts.json")
        except (FileNotFoundError, ValueError) as e:
            print(f"Error loading accounts: {e}")
            self.accounts = []

    def check_ids(self):
        if self.accounts:
            for account in self.accounts:
                if account.get("selected") == 1:
                    return account
                    
    def check_paper_exist(self):
        if not self.account:
            
            self.empty_Label.pack(padx=(40, 40), pady=(200, 40))
        else:
            
            if self.account.get("number-of-papers", 0) != 0:
                
                
                for paper in self.account["papers-dictionary"]:
                    
                    path = os.path.join(self.account.get("path"), paper[0])
                    if not os.path.exists(path):
                        self.empty_Label.pack(padx=(40, 40), pady=(200, 40))
                        
                        return
                    with open(path,'r') as f:
                        physics,chemistry,maths = json.load(f)
                    
                    datas = {
                        "Physics": physics,
                        "Chemistry": chemistry,
                        "Maths": maths
                    }
                    # self.add_exam_element(paper[2],datas,paper[3])
                    if paper[1] == "New Exam":
                        self.add_exam_element(f"{paper[2]}--(New Exam)", "Start",datas,paper[3])
                    elif paper[1].split(" ")[0] == "solved":
                        self.add_view_element(f"{paper[2]}--(Solved)", "View",paper[3])
                    elif paper[1].split(" ")[0] == "pending" and int(paper[4]) < 2:
                        self.add_exam_element(f"{paper[2]}--(Resume the exam in 3 hours from the time exam started)", "Resume",datas,paper[3])
                    elif paper[1].split(" ")[0] == "auto_submit" and int(paper[4]) >= 2:
                        self.add_view_element(f"{paper[2]}--(Oops! Paper is auto submitted)", "View",paper[3])
                    
                    self.empty_Label.pack_forget()
            else:
                self.empty_Label.pack(padx=(40, 40), pady=(200, 40))


    def login_window(self):
        if self.account:
            if self.dropdown.winfo_ismapped():
                self.dropdown.hide()
            else:
                self.dropdown.show(x=(self.profile_label.winfo_x()), y=(self.profile_label.winfo_y() + self.profile_label.winfo_height()+5))
                self.dropdown.lift()
            return
        else: 
            self.Login()
        # Logic to open login window goes here
        print("Opening login window...")
    def login_dropdown(self):
        self.dropdown = DropdownMenu(self)
        self.profile_option = self.dropdown.add_option("Profile",)
        self.switch_option = self.dropdown.add_option("Switch Account",)
        self.logout_option = self.dropdown.add_option("Logout",)
        self.exit_option = self.dropdown.add_option("Exit App",)

        self.profile_option.config(
            background=self.setting["dropdown"]["background-color"],
            foreground=self.setting["dropdown"]["foreground-color"],
            font=self.setting["dropdown"]["font"],
            borderwidth=0,
            anchor="w",
            padx=10
        )
        self.profile_option.bind("<Button-1>",lambda event=None:self.profile_function())
        self.switch_option.config(
            background=self.setting["dropdown"]["background-color"],
            foreground=self.setting["dropdown"]["foreground-color"],
            font=self.setting["dropdown"]["font"],
            borderwidth=0,
            anchor="w",
            padx=10,
        )
        self.switch_option.bind("<Button-1>",lambda event=None:self.switch_account_window())
        self.logout_option.config(
            background=self.setting["dropdown"]["background-color"],
            foreground=self.setting["dropdown"]["foreground-color"],
            font=self.setting["dropdown"]["font"],
            borderwidth=0,
            anchor="w",
            padx=10
        )
        self.logout_option.bind("<Button-1>",lambda event=None:self.logout_function())
        self.exit_option.config(
            background=self.setting["dropdown"]["background-color"],
            foreground=self.setting["dropdown"]["foreground-color"],
            font=self.setting["dropdown"]["font"],
            borderwidth=0,
            anchor="w",
            padx=10
        )
        self.exit_option.bind("<Button-1>", lambda e: self.quit())
        self.dropdown.hover(self.setting["dropdown"]["hover-color"], self.setting["dropdown"]["background-color"],self.profile_option)
        self.dropdown.hover(self.setting["dropdown"]["hover-color"], self.setting["dropdown"]["background-color"],self.switch_option)
        self.dropdown.hover(self.setting["dropdown"]["hover-color"], self.setting["dropdown"]["background-color"],self.logout_option)
        self.dropdown.hover(self.setting["dropdown"]["hover-color"], self.setting["dropdown"]["background-color"],self.exit_option)
    def profile_function(self):
        profile = Toplevel(self)
        profile.resizable(0,0)
        profile.maxsize(400,400)
        profile.config(background=self.setting["App"]["primary-background-color"])
        profile_container = Frame(profile,background=self.setting["App"]["primary-background-color"])
        profile_container.pack(padx=(50,50),pady=(50,50))

        id_label = Label(
            profile_container,
            text=f"User ID :- {self.account["id"]}",
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
            text=f"Name :- {self.account["name"]}",
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
            text=f"Age :- {self.account["age"]}",
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
            text=f"Password :- {self.account["password"]}",
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
            text=f"folder path :- {self.account["path"]}",
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
            text=f"Number of papers :- {self.account["number-of-papers"]}",
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
        password_label.pack()
        password_label.pack_propagate(0)
        path_label.pack()
        path_label.pack_propagate(0)
        number_of_papers_label.pack()
        number_of_papers_label.pack_propagate(0)

        self.dropdown.hide()
    def logout_function(self):
        self.account["selected"] = 0 
        with open("src/accounts.json","w") as f:
            json.dump(self.accounts,f,indent=4)
        for element in self.element_list:
            element.pack_forget()
        self.account = self.check_ids()
        userid =  "Login" if self.account is None else self.account.get("id", "Unknown")
        self.profile_label.config(text=userid)
        self.check_paper_exist()
        self.dropdown.hide()
    def create_exam(self):
        if not self.account:
            print("Please Login first!")
            messagebox.showerror("Error", "Please Login first!")
            self.Login()
            return
        # Logic to create an exam goes here
        print("Creating exam...")
        physics, chemistry, maths = self.load_questions()
        
        
        self.storing_question_paper(self.account, [physics, chemistry, maths])
        if not physics and not chemistry and not maths:
            messagebox.showinfo("Info", "No questions available for the selected subjects.")
            return
        
        if self.empty_Label.winfo_ismapped():
            self.empty_Label.pack_forget()
        text = f"Paper {self.account.get('number-of-papers', 0)+1}"
        exam_id = self.generate_random_id()
        self.add_exam_element(f"Paper {self.account.get('number-of-papers', 0)+1}", "Start",{"Physics": physics,"Chemistry": chemistry,"Maths": maths},exam_id)


        i = self.account.get("number-of-papers",0)
        self.account["papers-dictionary"].append((self.account.get("id")+ str(i+1) + ".json","New Exam",text,exam_id,0))
        self.account["number-of-papers"] = i+1
        update_json_value("src/accounts.json", "number-of-papers", self.account["number-of-papers"])
        update_json_value("src/accounts.json", "papers-dictionary", self.account["papers-dictionary"])
    def storing_question_paper(self,account,datas):
        i = account.get("number-of-papers",0)
        path = os.path.join(account.get("path"), account.get("id") + str(i+1) + ".json")
        
        try:
            if not os.path.exists(account.get("path")):
                os.makedirs(account.get("path"))
            if not os.path.exists(path):
                # Create the file and initialize it with an empty list
                with open(path, 'w') as f:
                    json.dump([], f, indent=4)
            
            with open(path, 'r+') as f:
                content = json.load(f)
                for data in datas:
                    content.append(data)
                f.seek(0)  # Move the cursor to the beginning of the file
                json.dump(content, f, indent=4)
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON format in file: {path}")
    def Login(self):
        login = Toplevel(self)
        login.geometry("400x400")
        login.resizable(0,0)
        login.config(background=self.setting["App"]["primary-background-color"])

        login_window = Frame(
            login,
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
            command=lambda:self.creating_new_account(id_entry.get(),name_entry.get(),age_entry.get(),password_entry.get(),login)
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
            command=lambda:self.function_with_destroy(self.switch_account_window,login))
        
        login_if_already.pack(side='right',padx=(0,10))
    def function_with_destroy(self,function,window):
        function()
        window.destroy()
    def creating_new_account(self,id,name,age,password,login):
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
        for account in self.accounts:
            if account["selected"] == 1:
                account["selected"] = 0
        self.accounts.append(data)
        with open("src/accounts.json","w") as f:
            json.dump(self.accounts,f,indent=4)
        for element in self.element_list:
            element.pack_forget()
        self.account = self.check_ids()
        userid =  "Login" if self.account is None else self.account.get("id", "Unknown")
        self.profile_label.config(text=userid)
        self.check_paper_exist()
        login.destroy()
    def generate_random_id(self):
        exam_id =  random.randint(1000, 9999)
        if self.account["papers-dictionary"]:
            for paper in self.account["papers-dictionary"]:
                if paper[3] == exam_id:
                    return self.generate_random_id()
            return exam_id
        return exam_id
    def switch_account_window(self):
        switch_window = Toplevel(self)
        # switch_window.geometry("400x400")
        switch_window.maxsize(width=400,height=400)
        switch_window.resizable(0,0)
        switch_window.config(background=self.setting["App"]["primary-background-color"])
        account_cantainer = Frame(switch_window,background=self.setting["App"]["primary-background-color"])
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
        for account in self.accounts:
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
                    command=lambda j=account["id"]:self.switch_account_function(j,switch_window)
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
                    command=lambda j=account["id"]:self.switch_account_function(j,switch_window)
                )
            button.pack()
            button.pack_propagate(0)
        create_new_account = CustomButton(
                    switch_window,
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
                    command=lambda:self.function_with_destroy(self.Login,switch_window)
        )
        create_new_account.pack(fill='x')
        self.dropdown.hide()
    def switch_account_function(self,id,switch_window):
        for account in self.accounts:
            if account["id"] == id:
                account["selected"] = 1 
            else: 
                account["selected"] = 0
        with open("src/accounts.json","w") as f:
            json.dump(self.accounts,f,indent=4)
        for element in self.element_list:
            element.pack_forget()
        self.account = self.check_ids()
        userid =  "Login" if self.account is None else self.account.get("id", "Unknown")
        self.profile_label.config(text=userid)
        self.check_paper_exist()
        switch_window.destroy()
        
    def add_exam_element(self,text,button_text,data,exam_id):
        button_settings = self.setting.get("Button", {})
        exam_element_frame = Frame(self, background=button_settings.get("background-color", "#FFFFFF"),highlightthickness=1)
        exam_element_frame.pack(fill='x', padx=(40, 40), pady=(5, 5))
        exam_element = Label(
            exam_element_frame,
            text=text,
            background=button_settings.get("background-color", "#FFFFFF"),
            foreground=button_settings.get("foreground-color", "#000000"),
            font=button_settings.get("font", ("Arial", 10)),
            relief=button_settings.get("relief", "flat"),
            borderwidth=0,
            cursor="hand2",
        )
        exam_element.pack(side='left', padx=(10, 5), pady=(5, 5))

        
        start_button = CustomButton(
            exam_element_frame,
            text=button_text,
            background=button_settings.get("background-color", "#FFFFFF"),
            foreground=button_settings.get("foreground-color", "#000000"),
            font=button_settings.get("font", ("Arial", 10)),
            relief=button_settings.get("relief", "flat"),
            pady=5,
            padx=5,
            cursor="hand2"
        )
        start_button.add_command(command=lambda btn=start_button: self.start_exam(data,exam_id,btn,exam_element))
        start_button.pack(side='right', padx=(5, 10), pady=(5, 5))

        self.element_list.append(exam_element_frame)
        
        

    def add_view_element(self,text,button_text,exam_id):
        button_settings = self.setting.get("Button", {})
        exam_element_frame = Frame(self, background=button_settings.get("background-color", "#FFFFFF"),highlightthickness=1)
        exam_element_frame.pack(fill='x', padx=(40, 40), pady=(5, 5))
        exam_element = Label(
            exam_element_frame,
            text=text,
            background=button_settings.get("background-color", "#FFFFFF"),
            foreground=button_settings.get("foreground-color", "#000000"),
            font=button_settings.get("font", ("Arial", 10)),
            relief=button_settings.get("relief", "flat"),
            borderwidth=0,
            cursor="hand2",
        )
        exam_element.pack(side='left', padx=(10, 5), pady=(5, 5))

        
        view_button = CustomButton(
            exam_element_frame,
            text=button_text,
            background=button_settings.get("background-color", "#FFFFFF"),
            foreground=button_settings.get("foreground-color", "#000000"),
            font=button_settings.get("font", ("Arial", 10)),
            relief=button_settings.get("relief", "flat"),
            cursor="hand2",
            pady=5,
            padx=5,
            command=lambda:self.view_marks(exam_id)
        )
        self.element_list.append(exam_element_frame)
        view_button.pack(side='right', padx=(5, 10), pady=(5, 5))
    
    def start_exam(self, questions_dictionary,exam_id,start_button,element_label):
        exam_start_time = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
        physics = questions_dictionary.get("Physics", [])
        chemistry = questions_dictionary.get("Chemistry", [])
        maths = questions_dictionary.get("Maths", [])

        if not physics and not chemistry and not maths:
            messagebox.showinfo("Info", "No questions available for the selected subjects.")
            return

        exam_window = ExamWindow(self,self.setting,self.account,questions_dictionary,exam_id,exam_start_time,start_button,element_label)

    def view_marks(self,exam_id):
        button_settings = self.setting.get("Button", {})
        marks_window = Toplevel(self)
        marks_window.resizable(0,0)
        marks_window.config(background=self.setting["App"]["primary-background-color"])
        marks_container = Frame(marks_window,background=self.setting["App"]["primary-background-color"])
        marks_container.pack(padx=(50,50),pady=(50,50))
        physics_marks,chemistry_marks,maths_marks,total_marks = self.calculate_marks(exam_id)
        phyiscs_label = Label(
            marks_container,
            text=f"Physics Marks :- {physics_marks}",
            background=button_settings.get("background-color", "#FFFFFF"),
            foreground=button_settings.get("foreground-color", "#000000"),
            font=button_settings.get("font", ("Arial", 10)),
            relief=button_settings.get("relief", "flat"),
            borderwidth=0,
            padx=5,
            pady=5,
            width=25,
            anchor='w',
            justify='left'

        )
        phyiscs_label.pack(padx=(50,50))
        phyiscs_label.pack_propagate(0)
        chemistry_label = Label(
            marks_container,
            text=f"Chemistry Marks :- {chemistry_marks}",
            background=button_settings.get("background-color", "#FFFFFF"),
            foreground=button_settings.get("foreground-color", "#000000"),
            font=button_settings.get("font", ("Arial", 10)),
            relief=button_settings.get("relief", "flat"),
            borderwidth=0,
            padx=5,
            pady=5,
            width=25,
            anchor='w',
            justify='left'

        )
        chemistry_label.pack(padx=(50,50))
        chemistry_label.pack_propagate(0)
        maths_label = Label(
            marks_container,
            text=f"Maths Marks :- {maths_marks}",
            background=button_settings.get("background-color", "#FFFFFF"),
            foreground=button_settings.get("foreground-color", "#000000"),
            font=button_settings.get("font", ("Arial", 10)),
            relief=button_settings.get("relief", "flat"),
            borderwidth=0,
            padx=5,
            pady=5,
            width=25,
            anchor='w',
            justify='left'

        )
        maths_label.pack(padx=(50,50))
        maths_label.pack_propagate(0)

        total_label = Label(
            marks_container,
            text=f"Total Marks :- {total_marks}",
            background=button_settings.get("background-color", "#FFFFFF"),
            foreground=button_settings.get("foreground-color", "#000000"),
            font=button_settings.get("font", ("Arial", 10)),
            relief=button_settings.get("relief", "flat"),
            borderwidth=0,
            padx=5,
            pady=5,
            width=25,
            anchor='w',
            justify='left'

        )
        total_label.pack(padx=(50,50))
        total_label.pack_propagate(0)

        show_answer_sheet = CustomButton(
            marks_window,
            text="Click here for answer sheet",
            background=self.setting["App"]["primary-background-color"],
            foreground=self.setting["Button"]["foreground-color"],
            font=self.setting["Button"]["font"],
            relief=self.setting["Button"]["relief"],
            cursor="hand2",
            borderwidth=0,
            padx=5,
            pady=5,
            command=lambda:self.answer_sheet_window(exam_id,marks_window)
        )
        show_answer_sheet.pack()
    def answer_sheet_window(self,exam_id,marks_window):
        answer_sheet_window = Toplevel()
        answer_sheet_window.title(f"Answer Sheet (Exam id:{exam_id})")
        answer_sheet_window_scrollbar = Scrollbar(answer_sheet_window,orient='vertical')
        answer_sheet_text = Text(answer_sheet_window,
                                 background=self.setting["App"]["primary-background-color"],
                                 foreground=self.setting["App"]["foreground-color"],
                                 font=self.setting["App-title"]["font"],
                                 wrap="word",
                                 borderwidth=0,
                                 padx=5,
                                 pady=5,
                                 yscrollcommand=answer_sheet_window_scrollbar.set)
        answer_sheet_window_scrollbar.config(command=answer_sheet_text.yview)
        answer_sheet_text.tag_configure("wrong",foreground="red")
        answer_sheet_text.tag_configure("right",foreground="spring green")
        answer_sheet_text.tag_configure("title",font=("Consolas",20,"bold"),underline=True)
        answer_sheet_text.pack(side='left',expand=True,fill='both')
        answer_sheet_window_scrollbar.pack(side='right',fill='y')
        for paper in self.account["papers-dictionary"]:
            if paper[3] == exam_id:
                question_paper_path = os.path.join(self.account["path"],paper[0])
                answer_sheet_path = os.path.join(self.account["path"],paper[1].split(" ")[1])
                with open(question_paper_path,'r') as f:
                    question_paper = json.load(f)
                with open(answer_sheet_path,'r') as f:
                    answer_sheet = json.load(f)
                physics_paper,chemistry_paper,maths_paper = question_paper
                physics_sheet,chemistry_sheet,maths_sheet = answer_sheet["Physics"],answer_sheet["Chemistry"],answer_sheet["Maths"]
                
                
                answer_sheet_text.insert("end","Physics\n","title")
                # for sheet in physics_sheet:
                for i,paper in enumerate(physics_paper,start=1):
                    answer_sheet_text.insert("end",f"Q{i}) {paper["question"]}\n")
                    if paper["question"] in self.physics_obtain_answers.keys():
                        answer_sheet_text.insert("end",f"Correct Answer :- {paper["correctOption"]}\n","right")
                        answer_sheet_text.insert("end",f"Your Answer :- {self.physics_obtain_answers[paper["question"]][0]}\n\n",self.physics_obtain_answers[paper["question"]][1])
                    else:
                        answer_sheet_text.insert("end",f"Correct Answer :- {paper["correctOption"]}\n","right")
                        answer_sheet_text.insert("end",f"Your Answer :- Not attempt\n\n")
                
                answer_sheet_text.insert("end","Chemistry\n","title")
                # for sheet in chemistry_sheet:
                for j,paper in enumerate(chemistry_paper,start=1):
                    answer_sheet_text.insert("end",f"Q{j}) {paper["question"]}\n")
                    if paper["question"] in self.chemistry_obtain_answers.keys():
                        answer_sheet_text.insert("end",f"Correct Answer :- {paper["correctOption"]}\n","right")
                        answer_sheet_text.insert("end",f"Your Answer :- {self.chemistry_obtain_answers[paper["question"]][0]}\n\n",self.chemistry_obtain_answers[paper["question"]][1])
                    else:
                        answer_sheet_text.insert("end",f"Correct Answer :- {paper["correctOption"]}\n","right")
                        answer_sheet_text.insert("end",f"Your Answer :- Not attempt\n\n")
                
                answer_sheet_text.insert("end","Maths\n","title")
                # for sheet in maths_sheet:
                for k,paper in enumerate(maths_paper,start=1):
                    answer_sheet_text.insert("end",f"Q{k}) {paper["question"]}\n")
                    if paper["question"] in self.maths_obtain_answers.keys():
                        answer_sheet_text.insert("end",f"Correct Answer :- {paper["correctOption"]}\n","right")
                        answer_sheet_text.insert("end",f"Your Answer :- {self.maths_obtain_answers[paper["question"]][0]}\n\n",self.maths_obtain_answers[paper["question"]][1])
                    else:
                        answer_sheet_text.insert("end",f"Correct Answer :- {paper["correctOption"]}\n","right")
                        answer_sheet_text.insert("end",f"Your Answer :- Not attempt\n\n")
                
        self.physics_obtain_answers = {}
        self.chemistry_obtain_answers = {}
        self.maths_obtain_answers = {}
        answer_sheet_text.config(state='disabled')
        marks_window.destroy()
        
    def calculate_marks(self,exam_id):
        marks = 0
        physics_marks = 0 
        chemistry_marks = 0 
        maths_marks = 0
        self.physics_obtain_answers = {}
        self.chemistry_obtain_answers = {}
        self.maths_obtain_answers = {}
        for paper in self.account["papers-dictionary"]:
            if paper[3] == exam_id:
                question_paper_path = os.path.join(self.account["path"],paper[0])
                answer_sheet_path = os.path.join(self.account["path"],paper[1].split(" ")[1])
                with open(question_paper_path,'r') as f:
                    question_paper = json.load(f)
                with open(answer_sheet_path,'r') as f:
                    answer_sheet = json.load(f)
                physics_paper,chemistry_paper,maths_paper = question_paper
                physics_sheet,chemistry_sheet,maths_sheet = answer_sheet["Physics"],answer_sheet["Chemistry"],answer_sheet["Maths"]

                for sheet in physics_sheet:
                    for paper in physics_paper:
                        if sheet == paper["question"]:
                            if physics_sheet[sheet][1] == paper["correctOption"]:
                                physics_marks+=4
                                self.physics_obtain_answers[paper["question"]] = [physics_sheet[sheet][1],"right"]
                            else:
                                physics_marks-=1
                                self.physics_obtain_answers[paper["question"]] = [physics_sheet[sheet][1],"wrong"]
                    
                for sheet in chemistry_sheet:
                    for paper in chemistry_paper:
                        if sheet == paper["question"]:
                            if chemistry_sheet[sheet][1] == paper["correctOption"]:
                                chemistry_marks+=4
                                self.chemistry_obtain_answers[paper["question"]] = [chemistry_sheet[sheet][1],"right"]
                            else:
                                chemistry_marks-=1
                                self.chemistry_obtain_answers[paper["question"]] = [chemistry_sheet[sheet][1],"wrong"]
                    
                for sheet in maths_sheet:
                    for paper in maths_paper:
                        if sheet == paper["question"]:
                            if maths_sheet[sheet][1] == paper["correctOption"]:
                                maths_marks+=4
                                self.maths_obtain_answers[paper["question"]] = [maths_sheet[sheet][1],"right"]
                            else:
                                maths_marks-=1
                                self.maths_obtain_answers[paper["question"]] = [maths_sheet[sheet][1],"wrong"]
                    
                break

        marks = int(physics_marks) + int(chemistry_marks) + int(maths_marks)
        return physics_marks,chemistry_marks,maths_marks,marks
                        


    def load_questions(self):
    
        phyiscs_json = get_json("src/questions/physics.json")
        chemistry_json = get_json("src/questions/chemistry.json")
        maths_json = get_json("src/questions/maths.json")

        phyiscs = random.sample(phyiscs_json, 30) if phyiscs_json else []
        chemistry = random.sample(chemistry_json, 30) if chemistry_json else []
        maths = random.sample(maths_json, 30) if maths_json else []

        return phyiscs, chemistry, maths

if __name__ == '__main__':
    app = App()
    app.mainloop()