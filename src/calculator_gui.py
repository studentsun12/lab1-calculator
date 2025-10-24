import tkinter as tk
from tkinter import messagebox
from src.utils.calculator import Calculators


class CalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор - Лабораторная 1")
        self.root.geometry("300x400")
        self.root.resizable(False, False)

        self.calc = Calculators()
        self.create_widgets()

        self.current_operation = None
        self.first_number = 0
        self.waiting_for_second_number = False

    def create_widgets(self):
        self.display = tk.Entry(self.root, font=('Arial', 18), justify='right', bd=10, relief='ridge')
        self.display.grid(row=0, column=0, columnspan=4, sticky='ew', padx=10, pady=10)
        self.display.insert(0, "0")

        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+',
            'C', '⌫'
        ]

        row = 1
        col = 0

        for button in buttons:
            if button == '=':
                cmd = lambda: self.calculate()
                btn = tk.Button(self.root, text=button, font=('Arial', 14),
                                command=cmd, bg='orange', fg='white', height=2, width=5)
            elif button == 'C':
                cmd = lambda: self.clear()
                btn = tk.Button(self.root, text=button, font=('Arial', 14),
                                command=cmd, bg='red', fg='white', height=2, width=5)
            elif button == '⌫':
                cmd = lambda: self.backspace()
                btn = tk.Button(self.root, text=button, font=('Arial', 14),
                                command=cmd, bg='lightgray', height=2, width=5)
            else:
                cmd = lambda x=button: self.button_click(x)
                btn = tk.Button(self.root, text=button, font=('Arial', 14),
                                command=cmd, bg='lightblue', height=2, width=5)

            btn.grid(row=row, column=col, padx=2, pady=2)

            col += 1
            if col > 3:
                col = 0
                row += 1

        info_label = tk.Label(self.root, text="Лабораторная работа 1 - Калькулятор с формой",
                              font=('Arial', 10), fg='gray')
        info_label.grid(row=row + 1, column=0, columnspan=4, pady=10)

    def button_click(self, value):
        current = self.display.get()

        if self.waiting_for_second_number:
            self.display.delete(0, tk.END)
            self.waiting_for_second_number = False

        if value in ['+', '-', '*', '/']:
            try:
                self.first_number = float(current)
                self.current_operation = value
                self.waiting_for_second_number = True
            except ValueError:
                messagebox.showerror("Ошибка", "Введите число перед операцией!")
        else:
            if current == "0" or current == "Error":
                self.display.delete(0, tk.END)
            self.display.insert(tk.END, value)

    def clear(self):
        self.display.delete(0, tk.END)
        self.display.insert(0, "0")
        self.current_operation = None
        self.waiting_for_second_number = False

    def backspace(self):
        current = self.display.get()
        if current and current != "0":
            new_text = current[:-1]
            self.display.delete(0, tk.END)
            self.display.insert(0, new_text if new_text else "0")

    def calculate(self):
        try:
            second_number = float(self.display.get())

            if self.current_operation == '+':
                result = self.calc.add(self.first_number, second_number)
            elif self.current_operation == '-':
                result = self.calc.subtract(self.first_number, second_number)
            elif self.current_operation == '*':
                result = self.calc.multiply(self.first_number, second_number)
            elif self.current_operation == '/':
                result = self.calc.divide(self.first_number, second_number)
            else:
                result = second_number

            if result == int(result):
                result = int(result)
            else:
                result = round(result, 10)

            self.display.delete(0, tk.END)
            self.display.insert(0, str(result))

        except ZeroDivisionError:
            messagebox.showerror("Ошибка", "Деление на ноль невозможно!")
            self.clear()
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректный ввод!")
            self.clear()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")
            self.clear()

        self.current_operation = None
        self.waiting_for_second_number = False


def main():
    root = tk.Tk()
    app = CalculatorGUI(root)
    root.mainloop()