import tkinter as tk
from random import choice

def play_game(user_choice):
    choices = ["Rock", "Paper", "Scissors"]
    computer_choice = choice(choices)
    result = ""
    if user_choice == computer_choice:
        result = "It's a tie!"
    elif (user_choice == "Rock" and computer_choice == "Scissors") or \
         (user_choice == "Paper" and computer_choice == "Rock") or \
         (user_choice == "Scissors" and computer_choice == "Paper"):
        result = "You win!"
        scores["You"] += 1
    else:
        result = "Computer wins!"
        scores["Computer"] += 1

    update_scoreboard()
    result_label.config(text=f"Computer chose {computer_choice}\n\n{result}")

def update_scoreboard():
    you_score_label.config(text=str(scores["You"]))
    computer_score_label.config(text=str(scores["Computer"]))

def reset_game():
    scores["You"] = 0
    scores["Computer"] = 0
    update_scoreboard()
    result_label.config(text="")

def show_game_interface():
    play_button.place_forget()  
    main_frame.pack(fill=tk.BOTH, expand=True)  

root = tk.Tk()
root.title("Rock-Paper-Scissors")
root.configure(bg="#F0F0F0")  

window_width = 650
window_height = 350
root.minsize(window_width, window_height)
root.maxsize(window_width, window_height)

scores = {"You": 0, "Computer": 0}

play_button = tk.Button(root, text="Play", font=("Helvetica", 16), command=show_game_interface, bg="#A9A9A9", fg="white", width=10, height=2)
play_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

main_frame = tk.Frame(root, bg="#F0F0F0")

left_frame = tk.Frame(main_frame, padx=10, pady=10, bg="#D3D3D3", bd=2, relief="groove")
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

right_frame = tk.Frame(main_frame, padx=10, pady=10, bg="#D3D3D3", bd=2, relief="groove")
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

scoreboard_title = tk.Label(right_frame, text="Scoreboard", font=("Helvetica", 16), bg="#D3D3D3")
scoreboard_title.pack()

scoreboard_frame = tk.Frame(right_frame, bg="#D3D3D3")
scoreboard_frame.pack()

you_label = tk.Label(scoreboard_frame, text="You", font=("Helvetica", 14), bg="#D3D3D3")
you_label.grid(row=0, column=0, padx=10, pady=10)

you_score_label = tk.Label(scoreboard_frame, text="0", font=("Helvetica", 14), bg="#D3D3D3")
you_score_label.grid(row=1, column=0, padx=10, pady=10)

computer_label = tk.Label(scoreboard_frame, text="Computer", font=("Helvetica", 14), bg="#D3D3D3")
computer_label.grid(row=0, column=1, padx=10, pady=10)

computer_score_label = tk.Label(scoreboard_frame, text="0", font=("Helvetica", 14), bg="#D3D3D3")
computer_score_label.grid(row=1, column=1, padx=10, pady=10)

buttons_frame = tk.Frame(left_frame, bg="#D3D3D3")
buttons_frame.pack(pady=20)

rock_button = tk.Button(buttons_frame, text="Rock", font=("Helvetica", 14), command=lambda: play_game("Rock"), bg="#A9A9A9", fg="white", width=10, height=2)
rock_button.grid(row=0, column=0, padx=10, pady=10)

paper_button = tk.Button(buttons_frame, text="Paper", font=("Helvetica", 14), command=lambda: play_game("Paper"), bg="#A9A9A9", fg="white", width=10, height=2)
paper_button.grid(row=0, column=1, padx=10, pady=10)

scissors_button = tk.Button(buttons_frame, text="Scissors", font=("Helvetica", 14), command=lambda: play_game("Scissors"), bg="#A9A9A9", fg="white", width=10, height=2)
scissors_button.grid(row=0, column=2, padx=10, pady=10)

result_label = tk.Label(left_frame, text="", font=("Helvetica", 14), pady=20, bg="#D3D3D3")
result_label.pack()

reset_button = tk.Button(left_frame, text="Reset Game", font=("Helvetica", 14), command=reset_game, bg="#A9A9A9", fg="white", width=15, height=2)
reset_button.pack(side=tk.BOTTOM, pady=20)

root.mainloop()
