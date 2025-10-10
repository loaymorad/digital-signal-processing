from tkinter import simpledialog
from utils import *

class Lab1:

    def read_signal():
        files = select_files()
        if not files: 
            return

        first_line, second_line, samples_number, samples = read_samples_from_file(files[0])
        
        plot_signal_side_by_side(samples)
        
        return first_line, second_line, samples_number, samples

    def add_signals():
        files = select_files(min_files=2)
        if not files:
            return

        signals_data = [read_samples_from_file(f)[3] for f in files]
        summed_samples = signals_data[0].copy()
        for sig in signals_data[1:]:
            summed_samples[:,1] += sig[:,1]

        first_line, second_line, _, _ = read_samples_from_file(files[0])
        
        plot_signal_side_by_side(summed_samples, title="Addition Result")
        
        save_signal(first_line, second_line, summed_samples, filename="result_add.txt")

    def multiply_signal():
        files = select_files()
        if not files:
            return

        constant = simpledialog.askfloat("Input", "Enter multiplication constant: ")
        if constant is None:
            return

        signal_file = files[0]
        first_line, second_line, _, samples = read_samples_from_file(signal_file)
        samples[:,1] *= constant

        plot_signal_side_by_side(samples, title=f"{signal_file.split('/')[-1]} x {constant}")

        save_signal(first_line, second_line, samples, filename=f"result_multiply_{signal_file.split('/')[-1]}")

