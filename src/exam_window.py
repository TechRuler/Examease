from tkinter import Tk, Toplevel, Label, messagebox,Frame
from helper import CustomButton
from tkinter import ttk
import os
import json
from datetime import datetime, timedelta
from helper import update_json_value
from physics import Physics
from chemistry import Chemistry
from maths import Maths 
class ExamWindow(Toplevel):
    def __init__(self, master,setting, account, datas,exam_id,exam_start_time, start_button,element_label):
        super().__init__(master)  # Fixed the super() call
        self.title("Exam Window")
        self.geometry("1000x700")
        self.setting = setting
        self.master = master 
        self.account = account
        self.datas = datas
        self.exam_id = exam_id
        self.exam_start_time = exam_start_time
        self.start_button = start_button
        self.element_label = element_label
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.physics = datas.get("Physics", {})
        self.chemistry = datas.get("Chemistry", {})
        self.maths = datas.get("Maths", {})
        self.total_exam_time = 180*60
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TNotebook', background=self.setting["App"]["secondary-background-color"], borderwidth=0)
        style.configure('TNotebook.Tab', background=self.setting["dropdown"]["background-color"], foreground=self.setting["App"]["foreground-color"], font=self.setting["Button"]["font"], padding=(10, 5))
        style.map('TNotebook.Tab', background=[('selected', self.setting["App"]["primary-background-color"],)], foreground=[('selected', self.setting["App"]["foreground-color"])])

        self.upper_frame = Frame(self, height=60, background=self.setting["App"]["secondary-background-color"])
        self.upper_frame.pack(fill='x')
        self.upper_frame.pack_propagate(0)

        self.title_label = Label(
            self.upper_frame,
            text="ExamWindow",
            background=self.setting["App"]["secondary-background-color"],
            foreground=self.setting["App"]["foreground-color"],
            font=("Consolas", 16),
            relief="flat",
            bd=0
        )
        self.title_label.pack(side='left', padx=(10, 5), pady=(5, 5))

        self.time = Label(
            self.upper_frame,
            text="Time: 00:00",
            background=self.setting["App"]["secondary-background-color"],
            foreground=self.setting["App"]["foreground-color"],
            font=self.setting["Button"]["font"],
            relief="flat",
            bd=0
        )
        self.time.pack(side='right', padx=(5, 10), pady=(5, 5))


        self.lower_frame = Frame(self, background="red")
        self.lower_frame.pack(fill='both', expand=True)

        self.lower_frame.pack_propagate(0)

        self.notebook = ttk.Notebook(self.lower_frame)
        self.notebook.pack(fill='both', expand=True)

        self.physics_frame = Frame(self.notebook, background=self.setting["App"]["primary-background-color"])
        self.notebook.add(self.physics_frame, text="Physics")
        self.physics_frame.pack_propagate(0)

        self.chemistry_frame = Frame(self.notebook, background=self.setting["App"]["primary-background-color"])
        self.notebook.add(self.chemistry_frame, text="Chemistry")
        self.chemistry_frame.pack_propagate(0)

        self.maths_frame = Frame(self.notebook, background=self.setting["App"]["primary-background-color"])
        self.notebook.add(self.maths_frame, text="maths")
        self.maths_frame.pack_propagate(0)

        self.physics_window = Physics(self.physics_frame, self.setting, self.physics)
        self.physics_window.pack(fill='both', expand=True)
        self.physics_window.set_submit_function(self.submit_function)

        self.chemistry_window = Chemistry(self.chemistry_frame, self.setting, self.chemistry)
        self.chemistry_window.pack(fill='both', expand=True)
        self.chemistry_window.set_submit_function(self.submit_function)

        self.maths_window = Maths(self.maths_frame, self.setting, self.maths)
        self.maths_window.pack(fill='both', expand=True)
        self.maths_window.set_submit_function(self.submit_function)

        self.load_exam_progress()
    # 1 ends here
    # 2 start 
    def load_saved_data(self):
        for paper in self.account["papers-dictionary"]:
            if paper[3] == self.exam_id:
                test_name = paper[0].split(".")[0]
                file_name = test_name + "_solved" + ".json"
                folder_path = self.account["path"]
                path = os.path.join(folder_path, file_name)
                if os.path.exists(path):
                    with open(path, 'r') as file:
                        solved_paper = json.load(file)
                    return solved_paper,paper[1].split(" ")[1]
                else:
                    return None,None
    def load_exam_progress(self):
        solved_paper,time = self.load_saved_data()
        if solved_paper != None:
            self.physics_window.physics_questions_and_selected_options = solved_paper["Physics"]
            
            self.chemistry_window.chemistry_questions_and_selected_options = solved_paper["Chemistry"]
            
            self.maths_window.maths_questions_and_selected_options = solved_paper["Maths"] 
            
    
            for question in self.physics_window.physics_questions_and_selected_options.keys():
                for button, data in self.physics_window.buttons_and_physics_question.items():
                    if data["question"] == question:
                        self.physics_window.update_physics_question(question,data["options"])
            
            for question in self.chemistry_window.chemistry_questions_and_selected_options.keys():
                for button, data in self.chemistry_window.buttons_and_chemistry_question.items():
                    if data["question"] == question:
                        self.chemistry_window.update_chemistry_question(question,data["options"])
    
            for question in self.maths_window.maths_questions_and_selected_options.keys():
                for button, data in self.maths_window.buttons_and_maths_question.items():
                    if data["question"] == question:
                        self.maths_window.update_maths_question(question,data["options"])
            current_time = datetime.now()
            exam_started_time = datetime.strptime(time, "%Y-%m-%d-%H:%M:%S")
            
            # Add 3 hours to exam start time
            exam_end_time = exam_started_time + timedelta(hours=int(self.total_exam_time/3600))
            
            # Calculate remaining time
            remaining_time = exam_end_time - current_time
            
            # Only run countdown if time is left
            if remaining_time.total_seconds() > 0:
                self.countdown(seconds=int(remaining_time.total_seconds()))
            else:
                self.time.config(text="Time's up!")
        else:
            self.countdown(seconds=(self.total_exam_time))
            
    # 2 ends here
                
                
    # 3 start
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.submit()
            for i, paper in enumerate(self.account["papers-dictionary"]):
                if paper[3] == self.exam_id and paper[1] == "New Exam":
                    paper = list(paper)  # Convert tuple to list
                    paper[1] = f"pending {self.exam_start_time}"
                    paper[4] = int(paper[4]) + 1
                    if paper[2].split("--"):
                        paper[2] = paper[2].split("--")[0]
                    self.account["papers-dictionary"][i] = paper  # Save back updated list
                    
                    self.element_label.config(text=f"{paper[2]}--(Resume the exam in 3 hours from the time exam started)")
                    self.start_button.config(text="Resume")
                    
                    break
                elif paper[3] == self.exam_id and paper[1] != "New Exam":
                    paper[4] = int(paper[4]) + 1
                    test_name = paper[0].split(".")[0]
                    file_name = test_name + "_solved" + ".json"
                    paper[1] = f"auto_submit {file_name}"
                    self.account["papers-dictionary"][i] = paper
                    if paper[4] < 2:
                        self.element_label.config(text=f"{paper[2]}--(Resume in exam in 3 hours from the time exam started)")
                        self.start_button.config(text="Resume")
                    else:
                        self.element_label.config(text=f"{paper[2]}--(Oops! Paper is auto submitted)")
                        self.start_button.pack_forget()
                        self.view_button = CustomButton(
                        self.element_label.master,
                        text="View",
                        background=self.setting["Button"]["background-color"],
                        foreground=self.setting["Button"]["foreground-color"],
                        font=self.setting["Button"]["font"],
                        relief=self.setting["Button"]["relief"],
                        cursor="hand2",
                        padx=5,
                        pady=5,
                        command=lambda:self.master.view_marks(self.exam_id)
                    )
                        self.view_button.pack(side='right', padx=(5, 10), pady=(5, 5))

            update_json_value("src/accounts.json", "papers-dictionary", self.account["papers-dictionary"])
            
 
            self.destroy()
    def submit(self):
        solved_paper = {}
        physics_solved = {}
        chemistry_solved = {}
        maths_solved = {} 
        for question, data in self.physics_window.physics_questions_and_selected_options.items(): 
            physics_solved[question] = data

        for question, data in self.chemistry_window.chemistry_questions_and_selected_options.items(): 
            chemistry_solved[question] = data

        for question, data in self.maths_window.maths_questions_and_selected_options.items():  
            maths_solved[question] = data 

        solved_paper["Physics"] = physics_solved
        solved_paper["Chemistry"] = chemistry_solved
        solved_paper["Maths"] = maths_solved
        folder_path = self.account["path"]
        for paper in self.account["papers-dictionary"]:
            if paper[3] == self.exam_id:
                test_name = paper[0].split(".")[0]
                file_name = test_name + "_solved" + ".json"

        path = os.path.join(folder_path, file_name)
        with open(path, 'w') as file:
            json.dump(solved_paper, file, indent=4)
    
    def submit_function(self):
        self.submit()
        for i, paper in enumerate(self.account["papers-dictionary"]):
            if paper[3] == self.exam_id:
                paper = list(paper)  # Convert tuple to list
                test_name = paper[0].split(".")[0]
                file_name = test_name + "_solved" + ".json"
                paper[1] = f"solved {file_name}"
                self.account["papers-dictionary"][i] = paper
                self.element_label.config(text=f"{paper[2]}--(Solved)")
                self.start_button.pack_forget()
                self.view_button = CustomButton(
                        self.element_label.master,
                        text="View",
                        background=self.setting["Button"]["background-color"],
                        foreground=self.setting["Button"]["foreground-color"],
                        font=self.setting["Button"]["font"],
                        relief=self.setting["Button"]["relief"],
                        cursor="hand2",
                        padx=5,
                        pady=5,
                        command=lambda:self.master.view_marks(self.exam_id)
                    )
                self.view_button.pack(side='right', padx=(5, 10), pady=(5, 5))
                break
        update_json_value("src/accounts.json", "papers-dictionary", self.account["papers-dictionary"])
        
        self.destroy()


        
    # 3 ends here
    #1 extra
    def countdown(self, seconds):
        if seconds >= 0:
            hours, rem = divmod(seconds, 3600)
            mins, secs = divmod(rem, 60)
            time_str = f"{int(hours):02d}:{int(mins):02d}:{int(secs):02d}"
            self.time.config(text=time_str)
            self.after(1000, self.countdown, seconds - 1)
        else:
            self.time.config(text="Time's up!")
            self.submit()
            for i, paper in enumerate(self.account["papers-dictionary"]):
                if paper[3] == self.exam_id:
                    paper = list(paper)  # Convert tuple to list
                    test_name = paper[0].split(".")[0]
                    file_name = test_name + "_solved" + ".json"
                    paper[1] = f"auto_submit {file_name}"
                    paper[4] = 2 
                    self.account["papers-dictionary"][i] = paper  # Save back updated list
                    
                    self.element_label.config(text=f"{paper[2]}--(Oops! Paper is auto submitted)")
                    self.start_button.pack_forget()
                    self.view_button = CustomButton(
                        self.element_label.master,
                        text="View",
                        background=self.setting["Button"]["background-color"],
                        foreground=self.setting["Button"]["foreground-color"],
                        font=self.setting["Button"]["font"],
                        relief=self.setting["Button"]["relief"],
                        cursor="hand2",
                        padx=5,
                        pady=5,
                        command=lambda:self.master.view_marks(self.exam_id)
                    )
                    self.view_button.pack(side='right', padx=(5, 10), pady=(5, 5))
                    break
            print(self.element_label.master)
            update_json_value("src/accounts.json", "papers-dictionary", self.account["papers-dictionary"])
            self.destroy()
    

