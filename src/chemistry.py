from tkinter import Frame, Label
from helper import CustomButton
class Chemistry(Frame):
    def __init__(self, master,setting,chemistry):
        super().__init__(master)
        self.master = master
        self.setting = setting
        self.chemistry = chemistry
        self.buttons_and_chemistry_question = {}
        self.chemistry_questions_and_selected_options = {}
        self.selected_chemistry_box = None
        self.chemistry_window()
    def set_submit_function(self,function):
        self.submit_function = function
    def chemistry_window(self):
        
        self.chemistry_question_and_options_frame()
        self.count_and_button_chemistry = self.chemistry_question_box_list_frame()
        for key in self.count_and_button_chemistry.keys():
            self.buttons_and_chemistry_question[self.count_and_button_chemistry[key]] = self.chemistry[key-1]
        
            self.selected_chemistry_box = self.count_and_button_chemistry[1]
        self.update_chemistry_question(
            self.buttons_and_chemistry_question[self.count_and_button_chemistry[1]].get("question"),
            self.buttons_and_chemistry_question[self.count_and_button_chemistry[1]].get("options")

        )
    def change_chemistry_question(self,event):
        widget = event.widget 
        self.selected_chemistry_box.config(background=self.setting["App"]["secondary-background-color"])
        for question, data in self.chemistry_questions_and_selected_options.items():
            if self.selected_chemistry_box and self.selected_chemistry_box.cget("text") == data[0]:
                print("Selected chemistry Box:", self.selected_chemistry_box.cget("text"))
                self.selected_chemistry_box.config(background="spring green")
        self.selected_chemistry_box = widget
        self.update_chemistry_question(
            self.buttons_and_chemistry_question[widget].get("question"),
            self.buttons_and_chemistry_question[widget].get("options")
        )
        self.selected_chemistry_box.config(background="steelblue")

    def chemistry_question_and_options_frame(self):

        self.exam_window = Frame(self.master, background=self.setting["App"]["secondary-background-color"])
        self.exam_window.pack(side='left', padx=(10, 10), pady=(5, 5), fill='both', expand=True)
        self.exam_window.pack_propagate(0)

        self.question_label_chemistry = Label(
            self.exam_window,
            text="Q1) What is the phenomenon of splitting of light into its constituent colors called?",
            background=self.setting["App"]["secondary-background-color"],
            foreground=self.setting["App"]["foreground-color"],
            font=("Consolas", 16),
            relief="flat",
            bd=0,
            wraplength=600,
            anchor="w",
            justify="left",
            
        )
        self.question_label_chemistry.pack(pady=(10, 10),fill='x', padx=(10, 10))
        options = ["Dispersion", "Reflection", "Refraction", "Diffraction"]
        self.option_frame_chemistry = []
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
            self.option_frame_chemistry.append(option_button)
            option_button.pack(pady=(10, 10), padx=(10, 10), fill='x')
            option_button.config(width=50, height=2)
            option_button.add_command(command=lambda btn=option_button: self.click_on_options_chemistry(btn))

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
            command=lambda: self.chemistry_next_button_function()
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
            command=lambda: self.chemistry_previous_button_function()
        )
        self.previous_button.pack(side='right', padx=(10, 10), pady=(5, 5))
        # self.previous_button.config(width=10, height=2)
    def chemistry_next_button_function(self):
        self.selected_chemistry_box.config(background=self.setting["App"]["secondary-background-color"])
        for question, data in self.chemistry_questions_and_selected_options.items():
            if self.selected_chemistry_box and self.selected_chemistry_box.cget("text") == data[0]:
                print("Selected chemistry Box:", self.selected_chemistry_box.cget("text"))
                self.selected_chemistry_box.config(background="spring green")
        number = self.selected_chemistry_box.cget("text")
        number = int(number) + 1 
        if number > 30:
            number = 1
        for button in self.buttons_and_chemistry_question.keys():
            if button.cget('text') == number:
                self.selected_chemistry_box = button
                self.update_chemistry_question(
                        self.buttons_and_chemistry_question[button].get("question"),
                        self.buttons_and_chemistry_question[button].get("options"))
                break
    def chemistry_previous_button_function(self):
        self.selected_chemistry_box.config(background=self.setting["App"]["secondary-background-color"])
        for question, data in self.chemistry_questions_and_selected_options.items():
            if self.selected_chemistry_box and self.selected_chemistry_box.cget("text") == data[0]:
                print("Selected chemistry Box:", self.selected_chemistry_box.cget("text"))
                self.selected_chemistry_box.config(background="spring green")
        number = self.selected_chemistry_box.cget("text")
        number = int(number) - 1 
        if number < 1:
            number = 30
        for button in self.buttons_and_chemistry_question.keys():
            if button.cget('text') == number:
                self.selected_chemistry_box = button
                self.update_chemistry_question(
                        self.buttons_and_chemistry_question[button].get("question"),
                        self.buttons_and_chemistry_question[button].get("options"))
                break
        
    def click_on_options_chemistry(self,widget):
        for opt in self.option_frame_chemistry:
                opt.config(background=self.setting["App"]["secondary-background-color"])

        for button, questions in self.buttons_and_chemistry_question.items():
            if widget.cget("text") in questions["options"] and self.selected_chemistry_box == button:
                if questions["question"] in self.chemistry_questions_and_selected_options and widget.cget("text") == self.chemistry_questions_and_selected_options[questions["question"]][1]:
                    self.count_and_button_chemistry[self.chemistry_questions_and_selected_options[questions["question"]][0]].config(background=self.setting["App"]["secondary-background-color"])
                    del self.chemistry_questions_and_selected_options[questions["question"]]
                    button.config(background="steelblue")
                else:
                    self.chemistry_questions_and_selected_options[questions["question"]] = [button.cget("text"),widget.cget("text")]
                    # self.chemistry_questions_and_selected_options["current_box"] = self.selected_chemistry_box
                    print("Selected chemistry Box:", widget.cget("text"))
                    widget.config(background="spring green")
                break
                
                
            
       


    def chemistry_question_box_list_frame(self):
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
                button.bind("<Button-1>", self.change_chemistry_question)
        return count_and_button

    
    def update_chemistry_question(self, question_text, options):
        
        self.question_label_chemistry.config(text=f"Q{self.selected_chemistry_box.cget("text")}){question_text}")
        for i, option in enumerate(options):
            self.option_frame_chemistry[i].config(text=option,background=self.setting["App"]["secondary-background-color"])
        for question, data in self.chemistry_questions_and_selected_options.items():
            for opt in self.option_frame_chemistry:
                if opt.cget("text") == data[1] and question == question_text:
                    opt.config(background="spring green")
                    self.count_and_button_chemistry[data[0]].config(background="spring green")
                    break
        self.selected_chemistry_box.config(background="steelblue")