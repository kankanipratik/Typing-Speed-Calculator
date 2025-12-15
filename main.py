import tkinter as tk
import time
import random
import os

# Load random sentence from file
def get_sentence(filename):
    try:
        with open(filename, "r") as f:
            lines = f.readlines()
        return random.choice(lines).strip()
    except:
        return "Error: Missing file!"

# Accuracy calculation
def calculate_accuracy(original, typed):
    correct = 0
    length = min(len(original), len(typed))

    for i in range(length):
        if original[i] == typed[i]:
            correct += 1

    mistakes = len(original) - correct
    accuracy = (correct / len(original)) * 100
    return accuracy, mistakes


class TypingSpeedGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.geometry("850x600")

        self.start_time = None
        self.started = False
        self.sentence = ""
        self.filename = None

        tk.Label(root, text="Typing Speed Test", font=("Arial", 22, "bold")).pack(pady=10)

        # Difficulty buttons
        level_frame = tk.Frame(root)
        level_frame.pack(pady=10)

        tk.Button(level_frame, text="Easy", width=12, 
                  command=lambda: self.select_level("easy.txt")).grid(row=0, column=0, padx=5)
        tk.Button(level_frame, text="Medium", width=12, 
                  command=lambda: self.select_level("medium.txt")).grid(row=0, column=1, padx=5)
        tk.Button(level_frame, text="Hard", width=12, 
                  command=lambda: self.select_level("hard.txt")).grid(row=0, column=2, padx=5)

        self.sentence_label = tk.Label(root, text="Choose a difficulty to begin", 
                                       font=("Arial", 14), wraplength=800)
        self.sentence_label.pack(pady=10)

        # Textbox
        self.textbox = tk.Text(root, font=("Arial", 14), width=90, height=7, state="disabled")
        self.textbox.pack(pady=10)

        # Highlight colors
        self.textbox.tag_configure("correct", foreground="green")
        self.textbox.tag_configure("incorrect", foreground="red")

        # ENTER triggers submission
        self.textbox.bind("<Return>", self.enter_submit)
        self.textbox.bind("<KeyRelease>", self.highlight_text)

        # Buttons
        tk.Button(root, text="START", width=15, command=self.start_test).pack(pady=5)
        tk.Button(root, text="Submit", width=15, command=self.calculate_results).pack(pady=5)
        tk.Button(root, text="Reset", width=15, command=self.reset_test).pack(pady=5)

        self.result_label = tk.Label(root, text="", font=("Arial", 14))
        self.result_label.pack(pady=20)

    # LEVEL SELECTOR
    def select_level(self, filename):
        self.filename = filename
        
        # Convert filename → Easy/Medium/Hard
        level_name = filename.replace(".txt", "").capitalize()

        self.sentence_label.config(text=f"Selected Level: {level_name}\nClick START")

    # START button
    def start_test(self):
        if not self.filename:
            self.sentence_label.config(text="Select a level first!")
            return

        self.sentence = get_sentence(self.filename)
        self.sentence_label.config(text=self.sentence)

        self.textbox.config(state="normal")
        self.textbox.delete("1.0", tk.END)

        # Move cursor directly into text box
        self.textbox.focus_set()

        self.start_time = None
        self.started = False
        self.result_label.config(text="")

    # ENTER submission
    def enter_submit(self, event):
        self.calculate_results()
        return "break"  # prevents newline

    # Highlight correct/incorrect characters
    def highlight_text(self, event):
        typed = self.textbox.get("1.0", "end-1c")

        # Start timer when user types first character
        if typed.strip() and not self.started:
            self.start_time = time.time()
            self.started = True

        # Clear old highlights
        self.textbox.tag_remove("correct", "1.0", "end")
        self.textbox.tag_remove("incorrect", "1.0", "end")

        # Apply highlighting
        for i in range(len(typed)):
            if i < len(self.sentence):
                tag = "correct" if typed[i] == self.sentence[i] else "incorrect"
                self.textbox.tag_add(tag, f"1.{i}", f"1.{i+1}")
            else:
                self.textbox.tag_add("incorrect", f"1.{i}", f"1.{i+1}")

    # Submit results
    def calculate_results(self):
        if not self.started:
            return

        typed = self.textbox.get("1.0", "end-1c")
        end_time = time.time()
        time_taken = end_time - self.start_time

        # Prevent unrealistic 0–0.3 sec timing
        if time_taken < 0.5:
            time_taken = 0.5

        words = len(typed.split())
        wpm = (words / time_taken) * 60

        accuracy, mistakes = calculate_accuracy(self.sentence, typed)

        self.result_label.config(
            text=f"Time: {time_taken:.2f}s | WPM: {wpm:.2f} | "
                 f"Accuracy: {accuracy:.2f}% | Mistakes: {mistakes}"
        )

        self.textbox.config(state="disabled")

    # Reset button
    def reset_test(self):
        self.start_time = None
        self.started = False
        self.filename = None

        self.sentence_label.config(text="Choose a difficulty to begin")

        self.textbox.delete("1.0", tk.END)
        self.textbox.config(state="disabled")

        self.result_label.config(text="")


root = tk.Tk()
app = TypingSpeedGUI(root)
root.mainloop()
