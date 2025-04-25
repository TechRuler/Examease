from tkinter import Toplevel,Frame,Label
from helper import CustomButton
import os
import json
class ViewMarks(Toplevel):
    def __init__(self,master,setting,exam_id,**kwarg):
        super().__init__(master,**kwarg)
        self.setting = setting
        self.master = master
        self.exam_id = exam_id
        button_settings = self.setting.get("Button", {})
        self.resizable(0,0)
        self.config(background=self.setting["App"]["primary-background-color"])
        marks_container = Frame(self,background=self.setting["App"]["primary-background-color"])
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
            self,
            text="Click here for answer sheet",
            background=self.setting["App"]["primary-background-color"],
            foreground=self.setting["Button"]["foreground-color"],
            font=self.setting["Button"]["font"],
            relief=self.setting["Button"]["relief"],
            cursor="hand2",
            borderwidth=0,
            padx=5,
            pady=5,
            command=self.show_answer_sheet
        )
        show_answer_sheet.pack()
    def show_answer_sheet(self):
        from .answer_sheet_window import AnswerSheet
        AnswerSheet(self.master,self.setting,self.exam_id,[self.physics_obtain_answers,self.chemistry_obtain_answers,self.master],self)
    def calculate_marks(self,exam_id):
        marks = 0
        physics_marks = 0 
        chemistry_marks = 0 
        maths_marks = 0
        self.physics_obtain_answers = {}
        self.chemistry_obtain_answers = {}
        self.maths_obtain_answers = {}
        for paper in self.master.account["papers-dictionary"]:
            if paper[3] == exam_id:
                question_paper_path = os.path.join(self.master.account["path"],paper[0])
                answer_sheet_path = os.path.join(self.master.account["path"],paper[1].split(" ")[1])
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
                        
