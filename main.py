import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import random
import os

HISTORY_FILE = "history.txt"

LEVELS = {
    "Easy": {"range": 50, "max_tries": 15},
    "Medium": {"range": 100, "max_tries": 10},
    "Hard": {"range": 200, "max_tries": 7}
}

class NumberGuessGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Number Guessing Game 🎯")
        self.geometry("420x500")
        self.resizable(False, False)
        self.configure(bg="#2E4053")
        
        self.player_name = None
        self.secret_number = None
        self.tries = 0
        self.game_over = False
        self.level = "Medium"
        self.max_tries = LEVELS[self.level]["max_tries"]
        self.number_range = LEVELS[self.level]["range"]
        
        self.create_widgets()
        self.ask_player_name()
        self.new_game()

    def create_widgets(self):
        self.title_label = tk.Label(self, text="Number Guessing Game", font=("Helvetica", 20, "bold"), fg="#F7DC6F", bg="#2E4053")
        self.title_label.pack(pady=15)

        # Level selector
        level_frame = tk.Frame(self, bg="#2E4053")
        level_frame.pack(pady=5)

        level_label = tk.Label(level_frame, text="Select Level:", font=("Arial", 12), fg="#F7DC6F", bg="#2E4053")
        level_label.pack(side='left', padx=5)

        self.level_var = tk.StringVar(value=self.level)
        self.level_dropdown = ttk.Combobox(level_frame, values=list(LEVELS.keys()), textvariable=self.level_var, state="readonly", width=10)
        self.level_dropdown.pack(side='left')
        self.level_dropdown.bind("<<ComboboxSelected>>", self.level_changed)

        # Info Frame
        self.info_frame = tk.Frame(self, bg="#34495E")
        self.info_frame.pack(pady=10, padx=10, fill='x')

        self.name_label = tk.Label(self.info_frame, text="Player: -", font=("Arial", 12), fg="#FDFEFE", bg="#34495E")
        self.name_label.pack(side='left', padx=5)

        self.level_label = tk.Label(self.info_frame, text=f"Level: {self.level}", font=("Arial", 12), fg="#FDFEFE", bg="#34495E")
        self.level_label.pack(side='left', padx=10)

        self.tries_label = tk.Label(self.info_frame, text="Tries: 0", font=("Arial", 12), fg="#FDFEFE", bg="#34495E")
        self.tries_label.pack(side='right', padx=5)

        # Guess Frame
        self.guess_frame = tk.Frame(self, bg="#2E4053")
        self.guess_frame.pack(pady=10)

        self.guess_label = tk.Label(self.guess_frame, text=f"Enter your guess (1-{self.number_range}):", font=("Arial", 14), fg="#F7DC6F", bg="#2E4053")
        self.guess_label.pack(pady=5)

        self.guess_entry = tk.Entry(self.guess_frame, font=("Arial", 14), width=10, justify='center')
        self.guess_entry.pack(pady=5)
        self.guess_entry.bind("<Return>", lambda event: self.check_guess())

        self.check_button = tk.Button(self.guess_frame, text="Guess", font=("Arial", 12), bg="#58D68D", fg="black", width=10, command=self.check_guess)
        self.check_button.pack(pady=5)

        # Feedback
        self.feedback_label = tk.Label(self, text="", font=("Arial", 14, "bold"), fg="#F7DC6F", bg="#2E4053")
        self.feedback_label.pack(pady=10)

        # Buttons Frame
        self.buttons_frame = tk.Frame(self, bg="#2E4053")
        self.buttons_frame.pack(pady=20)

        self.reset_button = tk.Button(self.buttons_frame, text="Reset Game", font=("Arial", 12), bg="#EB984E", fg="black", width=12, command=self.new_game)
        self.reset_button.grid(row=0, column=0, padx=10)

        self.history_button = tk.Button(self.buttons_frame, text="Show History", font=("Arial", 12), bg="#5DADE2", fg="black", width=12, command=self.show_history)
        self.history_button.grid(row=0, column=1, padx=10)

    def ask_player_name(self):
        name = simpledialog.askstring("Player Name", "Enter your name:", parent=self)
        if name and name.strip():
            self.player_name = name.strip()
        else:
            self.player_name = "Player1"
        self.name_label.config(text=f"Player: {self.player_name}")

    def level_changed(self, event=None):
        selected = self.level_var.get()
        if selected in LEVELS:
            self.level = selected
            self.number_range = LEVELS[self.level]["range"]
            self.max_tries = LEVELS[self.level]["max_tries"]
            self.level_label.config(text=f"Level: {self.level}")
            self.guess_label.config(text=f"Enter your guess (1-{self.number_range}):")
            self.new_game()

    def new_game(self):
        self.secret_number = random.randint(1, self.number_range)
        self.tries = 0
        self.game_over = False
        self.feedback_label.config(text="")
        self.tries_label.config(text=f"Tries: {self.tries}")
        self.guess_entry.config(state=tk.NORMAL)
        self.check_button.config(state=tk.NORMAL)
        self.guess_entry.delete(0, tk.END)
        print(f"[DEBUG] Secret number is: {self.secret_number}")  # Debug

    def check_guess(self):
        if self.game_over:
            return

        guess = self.guess_entry.get()
        if not guess.isdigit():
            messagebox.showwarning("Invalid input", f"Please enter a valid integer between 1 and {self.number_range}.")
            self.guess_entry.delete(0, tk.END)
            return

        guess = int(guess)
        if not (1 <= guess <= self.number_range):
            messagebox.showwarning("Out of range", f"Your guess must be between 1 and {self.number_range}.")
            self.guess_entry.delete(0, tk.END)
            return

        self.tries += 1
        self.tries_label.config(text=f"Tries: {self.tries}")

        if guess < self.secret_number:
            self.feedback_label.config(text="Too low! Try again.", fg="#F1948A")
        elif guess > self.secret_number:
            self.feedback_label.config(text="Too high! Try again.", fg="#F1948A")
        else:
            self.feedback_label.config(text=f"🎉 Correct! The number was {self.secret_number}.", fg="#58D68D")
            self.game_over = True
            self.guess_entry.config(state=tk.DISABLED)
            self.check_button.config(state=tk.DISABLED)
            self.save_history(win=True)
            self.ask_play_again()
            return

        self.guess_entry.delete(0, tk.END)

        if self.tries >= self.max_tries:
            self.feedback_label.config(text=f"😞 You lost! The number was {self.secret_number}.", fg="#E74C3C")
            self.game_over = True
            self.guess_entry.config(state=tk.DISABLED)
            self.check_button.config(state=tk.DISABLED)
            self.save_history(win=False)
            self.ask_play_again()

    def ask_play_again(self):
        answer = messagebox.askyesno("Play Again?", "Do you want to play again?")
        if answer:
            self.new_game()
        else:
            self.quit()

    def save_history(self, win):
        result = "Win" if win else "Loss"
        line = f"{self.player_name},{self.level},{result},{self.tries}\n"
        try:
            with open(HISTORY_FILE, "a") as file:
                file.write(line)
        except Exception as e:
            print(f"Error saving history: {e}")

    def show_history(self):
        if not os.path.exists(HISTORY_FILE):
            messagebox.showinfo("History", "No game history found.")
            return
        
        try:
            with open(HISTORY_FILE, "r") as file:
                lines = file.readlines()
        except Exception as e:
            messagebox.showerror("Error", f"Cannot read history: {e}")
            return

        if not lines:
            messagebox.showinfo("History", "No game history found.")
            return
        
        history_text = "Player - Level - Result - Tries\n" + "-"*32 + "\n"
        for line in lines[-10:]:  # Show last 10 games
            parts = line.strip().split(",")
            if len(parts) == 4:
                pname, lvl, res, tries = parts
                history_text += f"{pname} - {lvl} - {res} - {tries}\n"
        
        messagebox.showinfo("Game History (last 10)", history_text)

if __name__ == "__main__":
    app = NumberGuessGame()
    app.mainloop()
