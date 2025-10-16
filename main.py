import tkinter as tk
from Labs.Lab1 import Lab1
from Labs.Lab2 import Lab2
from Labs.Lab3 import Lab3



def label_list(buttons, col=0):
    global row
    for text, cmd in buttons:
        row += 1
        tk.Button(window, text=text, width=20, command=cmd).grid(row=row, column=col, pady=5)
    row += 1


if __name__ == "__main__":
    window = tk.Tk()
    window.title("Signal Processing Framework")
    window.geometry("1200x800")

    row = 0

    # ========= Lab 1 =========
    lab1 = Lab1()

    label_list(
        [
         ("Read Signal", lab1.read_signal), 
         ("Add Signals", lab1.add_signals), 
         ("Multiply Signals", lab1.multiply_signal)
        ]
    )

    # ========= Lab 2 =========
    lab2 = Lab2()

    label_list(
        [
            ("Generate Signal", lab2.generate_signal), 
            ("substract Signal", lab2.substract_signals), 
            ("square Signal", lab2.square_signal), 
            ("normalize Signal", lab2.normalize_signal), 
            ("accumulation signal", lab2.accumulation_signal)
        ]
    )


    # ========= Lab 3 =========
    lab3 = Lab3()

    label_list(
        [
            ("Quantize Signal", lab3.quantize_signal)
        ]
    )

    window.mainloop()