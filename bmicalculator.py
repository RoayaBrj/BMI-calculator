import tkinter as tk
from tkinter import messagebox
import csv
import os

HISTORY_FILE = 'bmi_history.csv'

def calculate_bmi(weight, height, system='metric'):
    """
    Calculate BMI based on the chosen unit system.
    :param weight: weight in kg (metric) or lb (imperial)
    :param height: height in meters (metric) or inches (imperial)
    :param system: 'metric' or 'imperial'
    :return: BMI as float
    """
    if system == 'imperial':
        return (weight / (height ** 2)) * 703
    else:
        return weight / (height ** 2)


def classify_bmi(bmi):
    """Return a health classification string based on BMI."""
    if bmi < 18.5:
        return 'Underweight'
    elif bmi < 25:
        return 'Normal weight'
    elif bmi < 30:
        return 'Overweight'
    else:
        return 'Obese'


class BMICalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BMI Calculator")
        self.resizable(False, False)
        self.unit = tk.StringVar(value='metric')
        self._create_widgets()
        self._ensure_history_file()

    def _create_widgets(self):
      
        frame_units = tk.LabelFrame(self, text="Units")
        frame_units.pack(padx=10, pady=5, fill='x')
        tk.Radiobutton(frame_units, text="Metric (kg, cm)", variable=self.unit, value='metric').pack(side='left', padx=5)
        tk.Radiobutton(frame_units, text="Imperial (lb, in)", variable=self.unit, value='imperial').pack(side='left', padx=5)

      
        frame_inputs = tk.Frame(self)
        frame_inputs.pack(padx=10, pady=5)
        tk.Label(frame_inputs, text="Weight:").grid(row=0, column=0, sticky='e')
        self.entry_weight = tk.Entry(frame_inputs)
        self.entry_weight.grid(row=0, column=1)
        tk.Label(frame_inputs, text="Height:").grid(row=1, column=0, sticky='e')
        self.entry_height = tk.Entry(frame_inputs)
        self.entry_height.grid(row=1, column=1)

        frame_buttons = tk.Frame(self)
        frame_buttons.pack(padx=10, pady=5)
        tk.Button(frame_buttons, text="Calculate BMI", command=self.calculate).pack(side='left', padx=5)
        tk.Button(frame_buttons, text="View History", command=self.show_history).pack(side='left', padx=5)

        self.label_result = tk.Label(self, text="", font=('Arial', 12, 'bold'))
        self.label_result.pack(padx=10, pady=5)

    def _ensure_history_file(self):
      
        if not os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Unit','Weight','Height','BMI','Classification'])

    def calculate(self):
      
        try:
            weight = float(self.entry_weight.get())
            height = float(self.entry_height.get())
            if weight <= 0 or height <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Please enter positive numeric values for weight and height.")
            return

        system = self.unit.get()
        if system == 'metric':
            height = height / 100.0

        bmi = calculate_bmi(weight, height, system)
        classification = classify_bmi(bmi)
        result_text = f"BMI: {bmi:.1f} ({classification})"
        self.label_result.config(text=result_text)

  
        with open(HISTORY_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([system, weight, height, f"{bmi:.1f}", classification])

    def show_history(self):
       
        if not os.path.exists(HISTORY_FILE):
            messagebox.showinfo("History", "No history file found.")
            return

        history_win = tk.Toplevel(self)
        history_win.title("BMI History")
        text = tk.Text(history_win, width=50, height=15)
        text.pack(padx=10, pady=10)
        with open(HISTORY_FILE, 'r') as f:
            content = f.read()
        text.insert('1.0', content)
        text.config(state='disabled')


if __name__ == '__main__':
    app = BMICalculatorApp()
    app.mainloop()
