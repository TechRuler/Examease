from tkinter import Frame, Label
from helper import CustomButton
class Subject(Frame):
    def __init__(self, master,setting,Subject):
        super().__init__(master)
        self.master = master
        self.setting = setting
        self.Subject = Subject
        self.answered_color = self.setting["exam-window"]["selected_answer_color"]
        self.selected_box_color = self.setting["exam-window"]["selected_box"]
        self.buttons_and_Subject_question = {}# button(1 to 30) and Subject dict
        self.Subject_questions_and_selected_options = {}# button(1 to 30) and Subject dict[question:[3,answerd]] selected(answered)
        self.selected_Subject_box = None # current button 
        self.Subject_window() # MAIN UI
    def set_submit_function(self,function):
        """
        This function take sumit functin from exam window
        """
        self.submit_function = function

    def Subject_window(self):
        """
        Main UI of exam of Subject 
        """
        self.Subject_question_and_options_frame() # question and options ui
        self.count_and_button_Subject = self.Subject_question_box_list_frame()
        for key in self.count_and_button_Subject.keys():
            self.buttons_and_Subject_question[self.count_and_button_Subject[key]] = self.Subject[key-1]
            self.selected_Subject_box = self.count_and_button_Subject[1]
        self.update_Subject_question(
            self.buttons_and_Subject_question[self.count_and_button_Subject[1]].get("question"),
            self.buttons_and_Subject_question[self.count_and_button_Subject[1]].get("options")

        )
    
    def Subject_question_and_options_frame(self):

        self.exam_window = Frame(self.master, background=self.setting["App"]["secondary-background-color"])
        self.exam_window.pack(side='left', padx=(10, 10), pady=(5, 5), fill='both', expand=True)
        self.exam_window.pack_propagate(0)

        self.question_label_Subject = Label(
            self.exam_window,
            text="Q1)What is the phenomenon of splitting of light into its constituent colors called?",
            background=self.setting["App"]["secondary-background-color"],
            foreground=self.setting["App"]["foreground-color"],
            font=("Consolas", 16),
            relief="flat",
            bd=0,
            wraplength=600,
            anchor="w",
            justify="left",
            
        )
        self.question_label_Subject.pack(pady=(10, 10),fill='x', padx=(10, 10))
        options = ["Dispersion", "Reflection", "Refraction", "Diffraction"]
        self.option_frame_Subject = []
        for i in options:
            option_button = CustomButton(
                self.exam_window,
                text=f"{i}",
                background=self.setting["App"]["secondary-background-color"],
                foreground=self.setting["App"]["foreground-color"],
                font=self.setting["Button"]["font"],
                relief="ridge",
                cursor="hand2",
                anchor="w",
                justify="left",
                padx=5,
                pady=5,
                wraplength=600
            )
            self.option_frame_Subject.append(option_button)
            option_button.pack(pady=(10, 10), padx=(10, 10), fill='x')
            option_button.config(width=50, height=2)
            option_button.add_command(command=lambda btn=option_button: self.click_on_options_Subject(btn))

        self.next_previous_frame = Frame(self.exam_window, background=self.setting["App"]["secondary-background-color"])
        self.next_previous_frame.pack(side='bottom', padx=(10, 10), pady=(5, 5), fill='x')

        self.next_button = CustomButton(
            self.next_previous_frame,
            text="Next/Save",
            background=self.setting["App"]["secondary-background-color"],
            foreground=self.setting["App"]["foreground-color"],
            font=self.setting["Button"]["font"],
            relief="ridge",
            cursor="hand2",
            justify="center",
            padx=5,
            pady=5,
            command=lambda: self.Subject_next_button_function()
        )
        self.next_button.pack(side='right', padx=(10, 10), pady=(5, 5))
        self.submit_button = CustomButton(
            self.next_previous_frame,
            text="Submit",
            background=self.setting["App"]["secondary-background-color"],
            foreground=self.setting["App"]["foreground-color"],
            font=self.setting["Button"]["font"],
            relief="ridge",
            cursor="hand2",
            justify="center",
            padx=5,
            pady=5,
            command=lambda: self.submit_function()
        )
        self.submit_button.pack(side='left', padx=(10, 10), pady=(5, 5))
        self.previous_button = CustomButton(
            self.next_previous_frame,
            text="Previous",
            background=self.setting["App"]["secondary-background-color"],
            foreground=self.setting["App"]["foreground-color"],
            font=self.setting["Button"]["font"],
            relief="ridge",
            cursor="hand2",
            justify="center",
            padx=5,
            pady=5,
            command=lambda: self.Subject_previous_button_function()
        )
        self.previous_button.pack(side='right', padx=(10, 10), pady=(5, 5))


    def Subject_question_box_list_frame(self):
        """
        Generate buttons from 1 to 30 
        """
        count_and_button = {}
        button_frame = Frame(self.master, background=self.setting["App"]["secondary-background-color"], width=400, height=600)
        button_frame.pack(side='right',padx=(10,10), pady=(5,5),fill='y')
        button_frame.pack_propagate(0)
        count = 1
        for i in range(6):
            for j in range(5):
                button = CustomButton(
                    button_frame,text=count,background=self.setting["App"]["secondary-background-color"],
                    foreground=self.setting["App"]["foreground-color"],
                    font=["Consolas",12,"italic"],
                    relief="ridge",
                    cursor="hand2",
                    padx=5,
                    pady=5
                    )
                
                count_and_button[count] = button
                button.grid(row=i,column=j,padx=(10,10),pady=(20,20))
                button.grid_propagate(0)
                button.config(width=3,height=2)
                count+=1
                button.bind("<Button-1>", self.change_Subject_question)
        return count_and_button

    


    def Subject_next_button_function(self):
        self.selected_Subject_box.config(background=self.setting["App"]["secondary-background-color"])
        for question, data in self.Subject_questions_and_selected_options.items():
            if self.selected_Subject_box and self.selected_Subject_box.cget("text") == data[0]:
                print("Selected Subject Box:", self.selected_Subject_box.cget("text"))
                self.selected_Subject_box.config(background=self.answered_color)
        number = self.selected_Subject_box.cget("text")
        number = int(number) + 1 
        if number > 30:
            number = 1
        for button in self.buttons_and_Subject_question.keys():
            if button.cget('text') == number:
                self.selected_Subject_box = button
                self.update_Subject_question(
                        self.buttons_and_Subject_question[button].get("question"),
                        self.buttons_and_Subject_question[button].get("options"))
                break
    def Subject_previous_button_function(self):
        self.selected_Subject_box.config(background=self.setting["App"]["secondary-background-color"])
        for question, data in self.Subject_questions_and_selected_options.items():
            if self.selected_Subject_box and self.selected_Subject_box.cget("text") == data[0]:
                print("Selected Subject Box:", self.selected_Subject_box.cget("text"))
                self.selected_Subject_box.config(background=self.answered_color)
        number = self.selected_Subject_box.cget("text")
        number = int(number) - 1 
        if number < 1:
            number = 30
        for button in self.buttons_and_Subject_question.keys():
            if button.cget('text') == number:
                self.selected_Subject_box = button
                self.update_Subject_question(
                        self.buttons_and_Subject_question[button].get("question"),
                        self.buttons_and_Subject_question[button].get("options"))
                break

    def change_Subject_question(self,event):
        widget = event.widget 
        self.selected_Subject_box.config(background=self.setting["App"]["secondary-background-color"])
        for question, data in self.Subject_questions_and_selected_options.items():
            if self.selected_Subject_box and self.selected_Subject_box.cget("text") == data[0]:
                print("Selected Subject Box:", self.selected_Subject_box.cget("text"))
                self.selected_Subject_box.config(background=self.answered_color)
        self.selected_Subject_box = widget
        self.update_Subject_question(
            self.buttons_and_Subject_question[widget].get("question"),
            self.buttons_and_Subject_question[widget].get("options")
        )
        self.selected_Subject_box.config(background=self.selected_box_color)

        
    def click_on_options_Subject(self,widget):
        for opt in self.option_frame_Subject:
                opt.config(background=self.setting["App"]["secondary-background-color"])

        for button, questions in self.buttons_and_Subject_question.items():
            if widget.cget("text") in questions["options"] and self.selected_Subject_box == button:
                if questions["question"] in self.Subject_questions_and_selected_options and widget.cget("text") == self.Subject_questions_and_selected_options[questions["question"]][1]:
                    self.count_and_button_Subject[self.Subject_questions_and_selected_options[questions["question"]][0]].config(background=self.setting["App"]["secondary-background-color"])
                    del self.Subject_questions_and_selected_options[questions["question"]]
                    button.config(background=self.selected_box_color)
                else:
                    self.Subject_questions_and_selected_options[questions["question"]] = [button.cget("text"),str(widget.cget("text"))]
                    print("Selected Subject Box:", widget.cget("text"))
                    widget.config(background=self.answered_color)
                break

            
    def update_Subject_question(self, question_text, options):
        
        self.question_label_Subject.config(text=f"Q{self.selected_Subject_box.cget("text")}){question_text}")
        for i, option in enumerate(options):
            self.option_frame_Subject[i].config(text=option,background=self.setting["App"]["secondary-background-color"])
        if self.Subject_questions_and_selected_options:
            for question, data in self.Subject_questions_and_selected_options.items():
                for opt in self.option_frame_Subject:
                    if opt.cget("text") == data[1] and question == question_text:
                        opt.config(background=self.answered_color)
                        break
        self.selected_Subject_box.config(background=self.selected_box_color)