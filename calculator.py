import tkinter as tk
from tkinter import messagebox
import math

class Calculator:
    def __init__(self, master):
        self.master = master
        master.title("Calculator")
        master.geometry("650x500")
        master.resizable(False, False)

        # Define font
        self.font = ("Roboto", 12)

        self.result_var = tk.StringVar()
        self.result_var.set("0")

        self.entry = tk.Entry(master, textvariable=self.result_var, font=self.font, bd=0, insertwidth=4, width=15, justify='right')
        self.entry.grid(row=0, column=0, columnspan=5, pady=(20, 10), padx=4, sticky="nsew")

        buttons = [
            ('Clear', 1, 0), ('Mode', 1, 1), ('Del', 1, 2), ('/', 1, 4),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('*', 2, 4),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('-', 3, 4),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('+', 4, 4),
            ('0', 5, 0), ('.', 5, 1), ('C', 5, 2), ('=', 5, 4)
        ]

        for (text, row, col) in buttons:
            if text in ['Clear', 'Mode', 'Del']:
                button = tk.Button(master, text=text, height=2, width=10, bg="#d9d9d9", fg="black", bd=0, font=self.font, command=lambda t=text: self.custom_command(t))
            elif text == '=':
                button = tk.Button(master, text=text, height=2, width=10, bg="#d9d9d9", fg="black", bd=0, font=self.font, command=self.calculate)
            elif text == 'C':
                button = tk.Button(master, text=text, height=2, width=10, bg="#d9d9d9", fg="black", bd=0, font=self.font, command=self.clear)
            elif text == 'x^y':
                button = tk.Button(master, text=text, height=2, width=10, bg="#d9d9d9", fg="black", bd=0, font=self.font, command=lambda t='^': self.append(t))
            elif text == '√x':
                button = tk.Button(master, text=text, height=2, width=10, bg="#d9d9d9", fg="black", bd=0, font=self.font, command=lambda t='√': self.append(t))
            elif text == 'M+':
                button = tk.Button(master, text=text, height=2, width=10, bg="#d9d9d9", fg="black", bd=0, font=self.font, command=self.memory_add)
            else:
                button = tk.Button(master, text=text, height=2, width=10, bg="#d9d9d9", fg="black", bd=0, font=self.font, command=lambda t=text: self.append(t))
            button.grid(row=row, column=col, padx=4, pady=4, sticky="nsew")

        self.memory = 0

        # Configure grid weights to distribute extra space
        for i in range(6):
            master.grid_rowconfigure(i, weight=1)
        for i in range(5):
            master.grid_columnconfigure(i, weight=1)

    def append(self, value):
        current_text = self.result_var.get()
        if current_text == "0" and value != '.':
            self.result_var.set(value)
        else:
            self.result_var.set(current_text + value)

    def calculate(self):
        try:
            expression = self.result_var.get()
            expression = expression.replace('^', '**')
            expression = expression.replace('√', 'math.sqrt')

            result = eval(expression)
            self.result_var.set(str(result))
        except Exception as e:
            messagebox.showerror("Error", "Invalid Input")

    def clear(self):
        self.result_var.set("0")

    def memory_add(self):
        try:
            self.memory += float(self.result_var.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid Memory Addition")
        else:
            messagebox.showinfo("Memory", "Value Added to Memory")

    def custom_command(self, cmd):
        if cmd == 'Clear':
            self.clear()
        elif cmd == 'Mode':
            self.display_mode()

    def display_mode(self):
        mode_frame = tk.Frame(self.master)
        mode_frame.grid(row=0, column=6, rowspan=6, padx=10, pady=10, sticky="nsew")

        shape_var = tk.StringVar()
        shape_var.set("circle")

        shapes = ["circle", "triangle", "rectangle", "square"]

        for idx, shape in enumerate(shapes):
            row = idx
            col = 0
            tk.Radiobutton(mode_frame, text=shape.capitalize(), variable=shape_var, value=shape, font=self.font, relief="flat", command=lambda: self.display_inputs(shape_var.get())).grid(row=row, column=col, sticky="w")

    def display_inputs(self, selected_shape):
        self.selected_shape = selected_shape  
        input_frame = tk.Frame(self.master)
        input_frame.grid(row=0, column=7, rowspan=6, padx=10, pady=10, sticky="nsew")

        self.entries = []

        inputs = {
            "circle": [("Radius", "")],
            "triangle": [("Base", ""), ("Height", "")],
            "rectangle": [("Length", ""), ("Width", "")],
            "square": [("Side", "")]
        }

        for idx, (label, default) in enumerate(inputs[selected_shape]):
            tk.Label(input_frame, text=label, font=self.font).grid(row=idx*2, column=0, sticky="w")
            entry = tk.Entry(input_frame, font=self.font, bd=1, insertwidth=4, width=10)
            entry.insert(0, default)
            entry.grid(row=idx*2+1, column=0, padx=5, pady=2, sticky="w")
            self.entries.append(entry)

        submit_button = tk.Button(input_frame, text="Submit", height=1, width=10, bg="#d9d9d9", fg="black", bd=0, font=self.font, command=self.calculate_area)
        submit_button.grid(row=len(inputs)*2, column=0, padx=5, pady=5, sticky="w")

    def calculate_area(self):
        try:
            selected_shape = self.selected_shape  
            inputs = [float(entry.get()) for entry in self.entries]
            if selected_shape == "circle":
                area = math.pi * (inputs[0] ** 2)
            elif selected_shape == "triangle":
                area = 0.5 * inputs[0] * inputs[1]
            elif selected_shape == "rectangle":
                area = inputs[0] * inputs[1]
            elif selected_shape == "square":
                area = inputs[0] ** 2
            else:
                messagebox.showerror("Error", "Invalid Shape")
                return
            self.result_var.set(str(area))
        except ValueError:
            messagebox.showerror("Error", "Invalid Input")

root = tk.Tk()
calculator = Calculator(root)
root.mainloop()

