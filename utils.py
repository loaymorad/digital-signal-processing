import numpy as np
import tkinter as tk
from tkinter import filedialog,  messagebox
import matplotlib.pyplot as plt


def save_signal(first_line, second_line, samples, filename):
    with open(filename, "w") as f:
        f.write(f"{first_line}\n{second_line}\n{len(samples)}\n")
        for x, y in samples:
            f.write(f"{x} {y}\n")
    messagebox.showinfo("Saved", f"Signal saved to {filename}")


def plot_signal_side_by_side(samples, title="Signal"):
    # Display continuous (left) and discrete (right) plots of a signal
    
    x = samples[:,0]
    y = samples[:,1]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12,4))

    # Continuous plot
    ax1.plot(x, y, color="blue")
    ax1.set_title("Continuous")
    ax1.set_xlabel("Sample Index")
    ax1.set_ylabel("Amplitude")

    # Discrete plot
    ax2.stem(x, y, linefmt='r-', markerfmt='ro', basefmt='k-')
    ax2.set_title("Discrete")
    ax2.set_xlabel("Sample Index")
    ax2.set_ylabel("Amplitude")

    fig.suptitle(title)
    plt.tight_layout()
    plt.show()

def select_files(min_files=1):
    files = filedialog.askopenfilenames(filetypes=[("Text files", "*.txt")])
    if not files:
        return None
    if len(files) < min_files:
        messagebox.showwarning("Not enough files", f"Select at least {min_files} file(s).")
        return None

    return files

def read_samples_from_file(signal_file):
    with open(signal_file, "r") as file:
        first_line = int(file.readline().strip())
        second_line = int(file.readline().strip())
        samples_number = int(file.readline().strip())
        samples = []
        for line in file:
            parts = line.strip().split()
            if len(parts) == 2:
                samples.append([int(parts[0]), int(parts[1])])
        samples = np.array(samples)
    return first_line, second_line, samples_number, samples

def prompt_gui(labels: list):
    gen_window = tk.Toplevel()
    gen_window.title("Prompt")

    output = []
    for i, label in enumerate(labels):
        tk.Label(gen_window, text=label).grid(row=i, column=0, padx=5, pady=5)
        entry = tk.Entry(gen_window)
        entry.grid(row=i, column=1, padx=5, pady=5)
        output.append(entry)

    return output, gen_window  # return the entries and the window so i can destroy it later
