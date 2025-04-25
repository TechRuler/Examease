from tkinter import Tk, Frame, Label
from tkinter import ttk
from tkinter import messagebox
import json
import os
import random
from datetime import datetime
from helper import get_json, update_json_value,DropdownMenu,CustomButton
from exam_window import ExamWindow
from components import Login,SwitchAccount,ProfileWindow,ViewMarks,ThemeWindow
from widget import ScrollableFrame


class App(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("800x700")
        self.title("Examease")
        self.importing_all_json()
        self.element_list = []

        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure('TNotebook', background=self.setting["App"]["secondary-background-color"], borderwidth=0)
        self.style.configure('TNotebook.Tab', background=self.setting["dropdown"]["background-color"], foreground=self.setting["App"]["foreground-color"], font=self.setting["Button"]["font"], padding=(10, 5))
        self.style.map('TNotebook.Tab', background=[('selected', self.setting["App"]["primary-background-color"],)], foreground=[('selected', self.setting["App"]["foreground-color"])])


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

        self.exam_element_frames = ScrollableFrame(self,background=app_settings["primary-background-color"])
        self.exam_element_frames.scrollable_frame.config(background=app_settings["primary-background-color"])
        self.exam_element_frames.canvas.config(background=app_settings["primary-background-color"])
        self.exam_element_frames.pack(expand=True,fill='both')

        empty_label_settings = self.setting.get("Empty-Label", {})
        self.empty_Label = Label(
                self.exam_element_frames.scrollable_frame,
                text="No Exam conducted!",
                background=empty_label_settings["background-color"],
                foreground=empty_label_settings["foreground-color"],
                font=empty_label_settings["font"],
                relief=empty_label_settings["relief"],
                borderwidth=empty_label_settings["border-width"]
            )
        

        self.statusbar_frame = Frame(self,bg=app_settings["secondary-background-color"])
        self.paper_status = Label(self.statusbar_frame,
                                     text="No Exam Conducted yet!",
                                     background=app_settings["secondary-background-color"],
                                     foreground=self.setting["Label"]["foreground-color"],
                                     font=self.setting["Label"]["font"],
                                     border=self.setting["Label"]["border-width"])
        self.paper_status.pack(side='left',padx=(10,10))
        self.statusbar_frame.pack(side='bottom',fill='x')

        
        self.check_paper_exist()
        self.login_dropdown()
        self.scrollbar_configure(scrollbar=app_settings["secondary-background-color"],scroll_bg=app_settings["primary-background-color"],active_scrollbar=app_settings["secondary-background-color"])
    def change_color(self):
        self.style.configure('TNotebook', background=self.setting["App"]["secondary-background-color"], borderwidth=0)
        self.style.configure('TNotebook.Tab', background=self.setting["dropdown"]["background-color"], foreground=self.setting["App"]["foreground-color"], font=self.setting["Button"]["font"], padding=(10, 5))
        self.style.map('TNotebook.Tab', background=[('selected', self.setting["App"]["primary-background-color"],)], foreground=[('selected', self.setting["App"]["foreground-color"])])

        app_settings = self.setting.get("App", {})
        self.exam_element_frames.config(background=app_settings["primary-background-color"])
        self.exam_element_frames.scrollable_frame.config(background=app_settings["primary-background-color"])
        self.exam_element_frames.canvas.config(background=app_settings["primary-background-color"])
        self.statusbar_frame.config(bg=app_settings["secondary-background-color"])
        self.paper_status.configure(background=app_settings["secondary-background-color"],
                                     foreground=self.setting["Label"]["foreground-color"],
                                     font=self.setting["Label"]["font"],
                                     border=self.setting["Label"]["border-width"])

        self.config(background=app_settings["primary-background-color"])
        self.upper_frame.config(background=app_settings["secondary-background-color"])

        app_title_settings = self.setting.get("App-title", {})
        self.app_name.config(background=app_title_settings["background-color"],
            foreground=app_title_settings["foreground-color"],
            font=app_title_settings["font"],
            relief=app_title_settings["relief"],
            borderwidth=app_title_settings["border-width"])
        
        button_settings = self.setting.get("Button", {})
        self.create_exam_button.config( background=button_settings["background-color"],
            foreground=button_settings["foreground-color"],
            font=button_settings["font"],
            relief=button_settings["relief"],
            cursor="hand2",
            pady=5,
            padx=5,)
        self.profile_label.config( background=button_settings["background-color"],
            foreground=button_settings["foreground-color"],
            font=button_settings["font"],
            relief=button_settings["relief"],
            cursor="hand2",
            pady=5,
            padx=5,)
        empty_label_settings = self.setting.get("Empty-Label", {})
        self.empty_Label.config(
                background=empty_label_settings["background-color"],
                foreground=empty_label_settings["foreground-color"],
                font=empty_label_settings["font"],
                relief=empty_label_settings["relief"],
                borderwidth=empty_label_settings["border-width"]
            )
        
        self.profile_option.config(
            background=self.setting["dropdown"]["background-color"],
            foreground=self.setting["dropdown"]["foreground-color"],
            font=self.setting["dropdown"]["font"],
            borderwidth=0,
            anchor="w",
            padx=10
        )
        self.switch_option.config(
            background=self.setting["dropdown"]["background-color"],
            foreground=self.setting["dropdown"]["foreground-color"],
            font=self.setting["dropdown"]["font"],
            borderwidth=0,
            anchor="w",
            padx=10,
        )
        self.theme_option.config(
            background=self.setting["dropdown"]["background-color"],
            foreground=self.setting["dropdown"]["foreground-color"],
            font=self.setting["dropdown"]["font"],
            borderwidth=0,
            anchor="w",
            padx=10,
        )
        self.logout_option.config(
            background=self.setting["dropdown"]["background-color"],
            foreground=self.setting["dropdown"]["foreground-color"],
            font=self.setting["dropdown"]["font"],
            borderwidth=0,
            anchor="w",
            padx=10
        )
        self.exit_option.config(
            background=self.setting["dropdown"]["background-color"],
            foreground=self.setting["dropdown"]["foreground-color"],
            font=self.setting["dropdown"]["font"],
            borderwidth=0,
            anchor="w",
            padx=10
        )
        self.dropdown.hover(self.setting["dropdown"]["hover-color"], self.setting["dropdown"]["background-color"],self.profile_option)
        self.dropdown.hover(self.setting["dropdown"]["hover-color"], self.setting["dropdown"]["background-color"],self.switch_option)
        self.dropdown.hover(self.setting["dropdown"]["hover-color"], self.setting["dropdown"]["background-color"],self.theme_option)
        self.dropdown.hover(self.setting["dropdown"]["hover-color"], self.setting["dropdown"]["background-color"],self.logout_option)
        self.dropdown.hover(self.setting["dropdown"]["hover-color"], self.setting["dropdown"]["background-color"],self.exit_option)
        self.scrollbar_configure(scrollbar=app_settings["secondary-background-color"],scroll_bg=app_settings["primary-background-color"],active_scrollbar=app_settings["secondary-background-color"])
        for element in self.element_list:
            element.pack_forget()
        self.check_paper_exist()
    def scrollbar_configure(self,scrollbar="grey",scroll_bg="white",active_scrollbar="white"):
        self.style.layout("Vertical.TScrollbar",
                 [('Vertical.Scrollbar.trough', {'children': [('Vertical.Scrollbar.thumb', {'expand': '1', 'sticky': 'nswe'})], 'sticky': 'ns'})])
        
        self.style.layout("Horizontal.TScrollbar",
                 [('Horizontal.TScrollbar.trough', {'children': [('Vertical.Scrollbar.thumb', {'expand': '1', 'sticky': 'nswe'})], 'sticky': 'ew'})])

        self.style.configure("Vertical.TScrollbar",
                             background=scrollbar,
                             bordercolor=scroll_bg,
                             darkcolor=scroll_bg,
                             lightcolor=scroll_bg,
                             troughcolor=scroll_bg,
                             arrowcolor=scroll_bg,
                             gripcount=0,
                             borderwidth=0)
        self.style.map("Vertical.TScrollbar",background=[('active',active_scrollbar)])

    def importing_all_json(self):
        try:
            self.accounts = get_json("src/accounts.json")
        except (FileNotFoundError, ValueError) as e:
            print(f"Error loading accounts: {e}")
            self.accounts = []

        self.account = self.check_ids()

        try:
            if self.account:
                self.setting = get_json(self.account["selected-theme"])
            else:
                self.setting = get_json("theme/Dark.json")
            # print(self.setting)
        except (FileNotFoundError, ValueError) as e:
            print(f"Error loading settings: {e}")
            self.setting = {}

        

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
                solved = 0
                for paper in self.account["papers-dictionary"]:
                    if paper[1].split(' ')[0] == "solved":
                        solved+=1
                    
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
                    if paper[1] == "New Exam":
                        self.add_exam_element(f"{paper[2]}--(New Exam)", "Start",datas,paper[3])
                    elif paper[1].split(" ")[0] == "solved":
                        self.add_view_element(f"{paper[2]}--(Solved)", "View",paper[3])
                    elif paper[1].split(" ")[0] == "pending" and int(paper[4]) < 2:
                        self.add_exam_element(f"{paper[2]}--(Resume the exam in 3 hours from the time exam started)", "Resume",datas,paper[3])
                    elif paper[1].split(" ")[0] == "auto_submit" and int(paper[4]) >= 2:
                        self.add_view_element(f"{paper[2]}--(Oops! Paper is auto submitted)", "View",paper[3])
                    
                    self.empty_Label.pack_forget()
                self.paper_status.config(text=f"Total papers->{self.account.get("number-of-papers", 0)} :: solved paper->{solved}")
            else:
                self.empty_Label.pack(padx=(40, 40), pady=(200, 40))
                self.paper_status.config(text=f"No Exam Conducted yet!")


    def login_window(self):
        if self.account:
            if self.dropdown.winfo_ismapped():
                self.dropdown.hide()
            else:
                self.dropdown.show(x=(self.profile_label.winfo_x()), y=(self.profile_label.winfo_y() + self.profile_label.winfo_height()+5))
                self.dropdown.lift()
            return
        else: 
            Login(self,self.setting)
        print("Opening login window...")
    def login_dropdown(self):
        self.dropdown = DropdownMenu(self)
        self.profile_option = self.dropdown.add_option("Profile",)
        self.switch_option = self.dropdown.add_option("Switch Account",)
        self.theme_option = self.dropdown.add_option("Themes",)
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
        self.profile_option.bind("<Button-1>",lambda event=None:ProfileWindow(self,self.setting))
        self.switch_option.config(
            background=self.setting["dropdown"]["background-color"],
            foreground=self.setting["dropdown"]["foreground-color"],
            font=self.setting["dropdown"]["font"],
            borderwidth=0,
            anchor="w",
            padx=10,
        )
        self.switch_option.bind("<Button-1>",lambda event=None:SwitchAccount(self,self.setting))
        self.theme_option.config(
            background=self.setting["dropdown"]["background-color"],
            foreground=self.setting["dropdown"]["foreground-color"],
            font=self.setting["dropdown"]["font"],
            borderwidth=0,
            anchor="w",
            padx=10,
        )
        self.theme_option.bind("<Button-1>",lambda event=None:ThemeWindow(self,self.setting))
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
        self.dropdown.hover(self.setting["dropdown"]["hover-color"], self.setting["dropdown"]["background-color"],self.theme_option)
        self.dropdown.hover(self.setting["dropdown"]["hover-color"], self.setting["dropdown"]["background-color"],self.logout_option)
        self.dropdown.hover(self.setting["dropdown"]["hover-color"], self.setting["dropdown"]["background-color"],self.exit_option)

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
            Login(self,self.setting)
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
    
    
    
    def generate_random_id(self):
        exam_id =  random.randint(1000, 9999)
        if self.account["papers-dictionary"]:
            for paper in self.account["papers-dictionary"]:
                if paper[3] == exam_id:
                    return self.generate_random_id()
            return exam_id
        return exam_id
    
    
        
    def add_exam_element(self,text,button_text,data,exam_id):
        button_settings = self.setting.get("Button", {})
        exam_element_frame = Frame(self.exam_element_frames.scrollable_frame, background=button_settings.get("background-color", "#FFFFFF"),highlightthickness=1)
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
        exam_element_frame = Frame(self.exam_element_frames.scrollable_frame, background=button_settings.get("background-color", "#FFFFFF"),highlightthickness=1)
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
            command=lambda:ViewMarks(self,self.setting,exam_id)
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

        ExamWindow(self,self.setting,self.account,questions_dictionary,exam_id,exam_start_time,start_button,element_label)




    def load_questions(self):
    
        phyiscs_json = get_json("questions/physics.json")
        chemistry_json = get_json("questions/chemistry.json")
        maths_json = get_json("questions/maths.json")

        phyiscs = random.sample(phyiscs_json, 30) if phyiscs_json else []
        chemistry = random.sample(chemistry_json, 30) if chemistry_json else []
        maths = random.sample(maths_json, 30) if maths_json else []

        return phyiscs, chemistry, maths
if __name__ == '__main__':
    app = App()
    app.mainloop()