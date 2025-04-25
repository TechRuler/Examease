from tkinter import Toplevel,Text,Scrollbar
import os,json
class AnswerSheet(Toplevel):
    def __init__(self,master,setting,exam_id,selected_answer,view_window,**kwarg):
        super().__init__(master,**kwarg)
        self.setting = setting
        self.master = master
        self.seleted_answer = selected_answer
        self.physics_obtain_answers = selected_answer[0]
        self.chemistry_obtain_answers = selected_answer[1]
        self.maths_obtain_answers = selected_answer[2]
        self.title(f"Answer Sheet (Exam id:{exam_id})")
        answer_sheet_window_scrollbar = Scrollbar(self,orient='vertical')
        answer_sheet_text = Text(self,
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
        view_window.destroy()
    
        