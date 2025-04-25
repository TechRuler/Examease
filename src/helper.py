from tkinter import Frame,Label
import json 
import os
class DropdownMenu(Frame):
    def __init__(self,master, *args,**kwargs):
        super().__init__(master,*args,**kwargs)
        pass

    def add_option(self,text,command=None):
        option = Label(self, text=text)
        option.pack(fill="x")
        option.bind("<Button-1>", lambda e: command() if command else None)
        
       
        return option
    def hover(self,color1,color2,option):
        # option = event.widget
        option.bind("<Enter>", lambda e: option.config(background=color1))
        option.bind("<Leave>", lambda e: option.config(background=color2))
    def show(self,x,y):
        self.place(x=x,y=y)
    def hide(self):
        self.place_forget() 
class CustomButton(Label):
    def __init__(self,master, command=None,**kwarg):
        super().__init__(master,**kwarg)
        self.command = command
        self.text = kwarg.get("text")
        self.config(text=self.text)

        self.bind("<Button-1>",lambda event=None:self.command())
    def add_command(self,command):
        self.command = command
        
    
def get_json(path):
    try:
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
        with open(path) as f:
            return json.load(f)
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in file: {path}")
def update_json_value(file_path, key, new_value):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(file_path, 'r+') as f:
            data = json.load(f)
            
            for account in data:
                if account.get("selected") == 1:
                    account[key] = new_value
                    break
            f.seek(0)  # Move the cursor to the beginning of the file
            json.dump(data, f, indent=4)
            f.truncate()  # Remove any leftover data from the previous content
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in file: {file_path}")