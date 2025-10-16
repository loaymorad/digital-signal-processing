from QuantizationTests.QuanTest1 import QuantizationTest1
from QuantizationTests.QuanTest2 import QuantizationTest2

import tkinter as tk
from tkinter import messagebox
import math
from utils import *

class Lab3:
    def uniform_quantizer(signal, bits=None, levels=None):
        if bits is not None:
            levels = 2 ** bits
        elif levels is not None:
            bits = math.ceil(math.log2(levels))
        else:
            raise ValueError("You must specify either bits or levels.")

        xmin, xmax = min(signal), max(signal)
        delta = (xmax - xmin) / levels

        indices, encoded, quantized, errors = [], [], [], []

        for s in signal:
            i = int((s - xmin) / delta)
            if i == levels:  # clamp edge case
                i = levels - 1
            q = xmin + (i + 0.5) * delta
            err = q - s

            indices.append(i)
            encoded.append(format(i, f'0{bits}b'))
            quantized.append(q)
            errors.append(err)

        return indices, encoded, quantized, errors

    def quantize_signal(event=None):
        labels = ["Bits (leave empty if using Levels)", "Levels (leave empty if using Bits)"]
        entries, gen_window = prompt_gui(labels)

        def on_quantize(entries, gen_window):
            files = select_files()
            if not files:
                messagebox.showwarning("Warning", "No files selected.")
                return

            bits = entries[0].get()
            levels = entries[1].get()
            bits = int(bits) if bits else None
            levels = int(levels) if levels else None

            for signal_file in files:
                first_line, second_line, _, samples = read_samples_from_file(signal_file, read_as="float")
                signal = samples[:, 1]  # y values

                indices, encoded, quantized, errors = Lab3.uniform_quantizer(signal, bits=bits, levels=levels)

                output_name = f"quantized_{signal_file.split('/')[-1]}"
                with open(output_name, "w") as f:
                    f.write(f"{int(float(first_line))}\n{int(float(second_line))}\n{len(signal)}\n")
                    
                    if levels is not None:
                        for i, e, q, err in zip(indices, encoded, quantized, errors):
                            f.write(f"{i} {e} {q:.3f} {err:.3f}\n")
                    else:
                        for e, q in zip(encoded, quantized):
                            f.write(f"{e} {q:.3f}\n")

                # Run tests
                if levels is not None: # means test 2
                    QuantizationTest2(output_name, indices, encoded, quantized, errors)
                else:
                    QuantizationTest1(output_name, encoded, quantized)


                messagebox.showinfo("Saved", f"Saved quantized file as {output_name}")

            gen_window.destroy()

        tk.Button(gen_window, text="Quantize",
                  command=lambda: on_quantize(entries, gen_window)).grid(row=len(labels), column=0, columnspan=2, pady=10)
