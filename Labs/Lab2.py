import numpy as np
import tkinter as tk
from tkinter import messagebox
from utils import *

class Lab2:
    def generate_signal():
        labels = ["signal type", "Amplitude (A)", "Analog Frequency (Hz)", "Sampling Frequency (Hz)", "Phase Shift (radians)"]
        entries, gen_window = prompt_gui(labels)

        def on_generate(entries, gen_window):
            signal_type = str(entries[0].get())
            A = float(entries[1].get())
            f_analog = float(entries[2].get())
            f_s = float(entries[3].get())
            theta = float(entries[4].get())


            # Generate signal
            t_end = 1  # duration 1 second
            t = np.arange(0, t_end, 1/f_s)
            if signal_type.lower() == "sin":
                y = A * np.sin(2 * np.pi * f_analog * t + theta)
            elif signal_type.lower() == "cos":
                y = A * np.cos(2 * np.pi * f_analog * t + theta)

            x = np.arange(len(t))
            samples = np.column_stack((x, y))

            save_signal(0, 0, samples, f"generated_{signal_type}.txt")
            gen_window.destroy()

        tk.Button(gen_window, text="Generate", command=lambda: on_generate(entries, gen_window)).grid(row=len(labels), column=0, columnspan=2, pady=10)

    def substract_signals():
        files = select_files(min_files=2)
        if not files:
            return

        signals_data = [read_samples_from_file(f)[3] for f in files]
        result_samples = signals_data[0].copy()
        for sig in signals_data[1:]:
            result_samples[:,1] -= sig[:,1]

        first_line, second_line, _, _ = read_samples_from_file(files[0])

        save_signal(first_line, second_line, result_samples, filename="result_subtract.txt")

    def square_signal():
        files = select_files(min_files=1)
        if not files:
            return

        signal_file = files[0]
        first_line, second_line, _, samples = read_samples_from_file(signal_file)
        samples[:,1] = np.square(samples[:,1])

        save_signal(first_line, second_line, samples, filename=f"squared_{signal_file.split('/')[-1]}")

    def normalize_signal():
        labels = ["File to normalize", "Normalization type (0-1 or -1 to 1)"]
        entries, gen_window = prompt_gui(labels)

        def on_normalize(entries, gen_window):
            files = select_files()
            if not files:
                return

            norm_type = entries[1].get()
            if norm_type not in ["0-1", "-1 to 1"]:
                messagebox.showerror("Error", "Normalization type must be '0-1' or '-1 to 1'")
                return

            for signal_file in files:
                first_line, second_line, _, samples = read_samples_from_file(signal_file)
                min_val, max_val = samples[:,1].min(), samples[:,1].max()

                if norm_type == "0-1":
                    samples[:,1] = (samples[:,1] - min_val) / (max_val - min_val)
                else:  # -1 to 1
                    samples[:,1] = 2 * (samples[:,1] - min_val) / (max_val - min_val) - 1

                # plot_signal_side_by_side(samples, title=f"Normalized {signal_file.split('/')[-1]}")
                save_signal(first_line, second_line, samples, filename=f"normalized_{signal_file.split('/')[-1]}")

            gen_window.destroy()

        tk.Button(gen_window, text="Normalize", command=lambda: on_normalize(entries, gen_window)).grid(row=len(labels), column=0, columnspan=2, pady=10)

    def accumulation_signal():
        files = select_files(min_files=1)
        if not files:
            return

        signal_file = files[0]
        first_line, second_line, _, samples = read_samples_from_file(signal_file)
        
        accumulated = []
        total = 0
        for y in samples[:,1]:
            total += y
            accumulated.append(total)
        
        samples[:,1] = np.array(accumulated)

        plot_signal_side_by_side(samples, title=f"Accumulated {signal_file.split('/')[-1]}")
        save_signal(first_line, second_line, samples, filename=f"accumulated_{signal_file.split('/')[-1]}")

