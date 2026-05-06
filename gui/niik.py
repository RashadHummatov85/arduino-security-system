import tkinter as tk
import tkinter.messagebox as msg
import os
import serial
import time

# ==============================
# COLORS
# ==============================
BG       = "#0e0e10"
SURFACE  = "#18181c"
SURFACE2 = "#222228"
BORDER   = "#2e2e38"
ACCENT   = "#e8ff47"
P1_COLOR = "#4fc3f7"
P2_COLOR = "#ff8a65"
TEXT     = "#f0f0f0"
MUTED    = "#888888"
DANGER   = "#ff4757"

# ==============================
# SERIAL CONNECTION
# ==============================
try:
    ser = serial.Serial("COM5", 9600)
    time.sleep(2)
    serial_connected = True
except:
    print("⚠️ Serial not connected")
    serial_connected = False

# ==============================
# WINDOW
# ==============================
root = tk.Tk()
root.title("Reaction Game")
root.geometry("520x900")
root.configure(bg=BG)
root.resizable(False, False)

# ==============================
# GAME VARIABLES
# ==============================
p1_score = 0
p2_score = 0
round_number = 1
game_over = False
game_active = False

# ==============================
# HELPER — styled frame line
# ==============================
def divider(parent):
    tk.Frame(parent, bg=BORDER, height=1).pack(fill="x", padx=20, pady=8)

# ==============================
# HEADER
# ==============================
header = tk.Frame(root, bg=BG)
header.pack(fill="x", padx=24, pady=(20, 0))

tk.Label(header, text="REACTION.", font=("Arial Black", 26),
         bg=BG, fg=TEXT).pack()
tk.Label(header, text="2-PLAYER REFLEX BATTLE",
         font=("Courier", 9), bg=BG, fg=MUTED).pack(pady=(2, 0))

divider(root)

# ==============================
# PLAYER INPUTS
# ==============================
players_frame = tk.Frame(root, bg=BG)
players_frame.pack(fill="x", padx=24, pady=(0, 12))
players_frame.columnconfigure(0, weight=1)
players_frame.columnconfigure(1, weight=1)

def player_block(parent, col, label, color):
    f = tk.Frame(parent, bg=SURFACE, bd=0)
    f.grid(row=0, column=col, padx=(0 if col == 0 else 8, 0), sticky="ew")
    # colored top bar
    tk.Frame(f, bg=color, height=3).pack(fill="x")
    inner = tk.Frame(f, bg=SURFACE)
    inner.pack(fill="x", padx=10, pady=8)
    tk.Label(inner, text=label, font=("Courier", 9),
             bg=SURFACE, fg=color).pack(anchor="w")
    e = tk.Entry(inner, bg=SURFACE2, fg=color, insertbackground=TEXT,
                 relief="flat", font=("Arial", 13, "bold"),
                 bd=6, highlightthickness=1,
                 highlightbackground=BORDER, highlightcolor=ACCENT)
    e.pack(fill="x", pady=(4, 0))
    return e

p1_entry = player_block(players_frame, 0, "PLAYER 1", P1_COLOR)
p2_entry = player_block(players_frame, 1, "PLAYER 2", P2_COLOR)

p1_entry.insert(0, "Player 1")
p2_entry.insert(0, "Player 2")

# ==============================
# STATUS BAR
# ==============================
status_frame = tk.Frame(root, bg=SURFACE, bd=0,
                        highlightthickness=1, highlightbackground=BORDER)
status_frame.pack(fill="x", padx=24, pady=8)

status_inner = tk.Frame(status_frame, bg=SURFACE)
status_inner.pack(fill="x", padx=12, pady=10)

dot_canvas = tk.Canvas(status_inner, width=10, height=10,
                       bg=SURFACE, highlightthickness=0)
dot_canvas.pack(side="left", padx=(0, 10))
dot = dot_canvas.create_oval(1, 1, 9, 9, fill=MUTED, outline="")

status_label = tk.Label(status_inner, text="Enter names and press Start",
                        font=("Courier", 10), bg=SURFACE, fg=MUTED)
status_label.pack(side="left")

def set_status(text, mode="idle"):
    status_label.config(text=text)
    if mode == "active":
        dot_canvas.itemconfig(dot, fill=ACCENT)
        status_label.config(fg=TEXT)
    elif mode == "go":
        dot_canvas.itemconfig(dot, fill=DANGER)
        status_label.config(fg=DANGER)
    else:
        dot_canvas.itemconfig(dot, fill=MUTED)
        status_label.config(fg=MUTED)

# ==============================
# SCOREBOARD
# ==============================
score_frame = tk.Frame(root, bg=SURFACE,
                       highlightthickness=1, highlightbackground=BORDER)
score_frame.pack(fill="x", padx=24, pady=8)

score_inner = tk.Frame(score_frame, bg=SURFACE)
score_inner.pack(fill="x", padx=16, pady=14)

# P1 side
p1_block = tk.Frame(score_inner, bg=SURFACE)
p1_block.pack(side="left", fill="x", expand=True)
p1_name_lbl = tk.Label(p1_block, text="PLAYER 1",
                        font=("Arial Black", 10), bg=SURFACE, fg=P1_COLOR)
p1_name_lbl.pack(anchor="w")
p1_pips = tk.Frame(p1_block, bg=SURFACE)
p1_pips.pack(anchor="w", pady=(4, 0))

pip1 = []
for i in range(3):
    c = tk.Canvas(p1_pips, width=26, height=6, bg=SURFACE, highlightthickness=0)
    c.pack(side="left", padx=2)
    r = c.create_rectangle(0, 0, 26, 6, fill=BORDER, outline="")
    pip1.append((c, r))

# Center score
center = tk.Frame(score_inner, bg=SURFACE)
center.pack(side="left", padx=20)
score_label = tk.Label(center, text="0  :  0",
                       font=("Arial Black", 28), bg=SURFACE, fg=TEXT)
score_label.pack()

# P2 side
p2_block = tk.Frame(score_inner, bg=SURFACE)
p2_block.pack(side="right", fill="x", expand=True)
p2_name_lbl = tk.Label(p2_block, text="PLAYER 2",
                        font=("Arial Black", 10), bg=SURFACE, fg=P2_COLOR)
p2_name_lbl.pack(anchor="e")
p2_pips = tk.Frame(p2_block, bg=SURFACE)
p2_pips.pack(anchor="e", pady=(4, 0))

pip2 = []
for i in range(3):
    c = tk.Canvas(p2_pips, width=26, height=6, bg=SURFACE, highlightthickness=0)
    c.pack(side="left", padx=2)
    r = c.create_rectangle(0, 0, 26, 6, fill=BORDER, outline="")
    pip2.append((c, r))

def update_pips():
    for i, (c, r) in enumerate(pip1):
        c.itemconfig(r, fill=P1_COLOR if i < p1_score else BORDER)
    for i, (c, r) in enumerate(pip2):
        c.itemconfig(r, fill=P2_COLOR if i < p2_score else BORDER)
    score_label.config(text=f"{p1_score}  :  {p2_score}")
    p1 = p1_entry.get().strip() or "Player 1"
    p2 = p2_entry.get().strip() or "Player 2"
    p1_name_lbl.config(text=p1.upper())
    p2_name_lbl.config(text=p2.upper())

# ==============================
# MATCH HISTORY
# ==============================
divider(root)
tk.Label(root, text="MATCH HISTORY", font=("Courier", 9),
         bg=BG, fg=MUTED).pack(anchor="w", padx=24)

history_frame = tk.Frame(root, bg=SURFACE,
                         highlightthickness=1, highlightbackground=BORDER)
history_frame.pack(fill="x", padx=24, pady=6)

history_list = tk.Listbox(history_frame, bg=SURFACE, fg=MUTED,
                           selectbackground=SURFACE2,
                           font=("Courier", 10), bd=0,
                           highlightthickness=0, height=5,
                           activestyle="none")
history_list.pack(fill="x", padx=4, pady=4)

# ==============================
# LEADERBOARD
# ==============================
divider(root)
tk.Label(root, text="LEADERBOARD", font=("Courier", 9),
         bg=BG, fg=MUTED).pack(anchor="w", padx=24)

lb_frame = tk.Frame(root, bg=SURFACE,
                    highlightthickness=1, highlightbackground=BORDER)
lb_frame.pack(fill="x", padx=24, pady=6)

leaderboard_list = tk.Listbox(lb_frame, bg=SURFACE, fg=TEXT,
                               selectbackground=SURFACE2,
                               font=("Courier", 11, "bold"), bd=0,
                               highlightthickness=0, height=3,
                               activestyle="none")
leaderboard_list.pack(fill="x", padx=4, pady=4)

# ==============================
# BUTTONS
# ==============================
divider(root)

btn_frame = tk.Frame(root, bg=BG)
btn_frame.pack(fill="x", padx=24, pady=(0, 20))
btn_frame.columnconfigure(0, weight=1)
btn_frame.columnconfigure(1, weight=1)

def make_btn(parent, text, cmd, row, col, span=1, style="normal"):
    bg_c = ACCENT if style == "primary" else SURFACE
    fg_c = "#0e0e10" if style == "primary" else (DANGER if style == "danger" else TEXT)
    b = tk.Button(parent, text=text, command=cmd,
                  bg=bg_c, fg=fg_c, activebackground=SURFACE2,
                  activeforeground=TEXT, relief="flat",
                  font=("Arial", 10, "bold"), cursor="hand2",
                  padx=10, pady=10, bd=0)
    b.grid(row=row, column=col, columnspan=span,
           sticky="ew", padx=(0, 0 if col == 1 else 8), pady=4)
    return b

make_btn(btn_frame, "START GAME", lambda: start_game(), 0, 0, span=2, style="primary")
make_btn(btn_frame, "NEW GAME",   lambda: new_game(),   1, 0)
make_btn(btn_frame, "RESET LEADERBOARD", lambda: reset_leaderboard(), 1, 1, style="danger")
make_btn(btn_frame, "DELETE PLAYER RECORDS", lambda: reset_ _records(), 2, 0, span=2, style="danger")

# ==============================
# FILE SAVE
# ==============================
def save_result(player, opponent, result):
    filename = f"{player}.txt"
    if not os.path.exists(filename):
        open(filename, "w").close()
    with open(filename, "a") as file:
        file.write(f"{result} vs {opponent}\n")

# ==============================
# LEADERBOARD LOGIC
# ==============================
def load_leaderboard():
    if not os.path.exists("leaderboard.txt"):
        return []
    with open("leaderboard.txt", "r") as f:
        return [line.strip() for line in f.readlines()]

def save_leaderboard(board):
    with open("leaderboard.txt", "w") as f:
        for name in board:
            f.write(name + "\n")

def update_leaderboard(winner, loser):
    board = load_leaderboard()
    if winner not in board:
        board.append(winner)
    if loser not in board:
        board.append(loser)
    w_index = board.index(winner)
    l_index = board.index(loser)
    if w_index > l_index:
        board[w_index], board[w_index - 1] = board[w_index - 1], board[w_index]
    save_leaderboard(board)
    display_leaderboard()

def display_leaderboard():
    leaderboard_list.delete(0, tk.END)
    for i, name in enumerate(load_leaderboard()):
        prefix = "★ " if i == 0 else f"{i+1}.  "
        leaderboard_list.insert(tk.END, f"  {prefix}{name}")
        if i == 0:
            leaderboard_list.itemconfig(i, fg=ACCENT)

# ==============================
# RESET FUNCTIONS
# ==============================
def reset_leaderboard():
    if msg.askyesno("Confirm", "Clear leaderboard?"):
        if os.path.exists("leaderboard.txt"):
            os.remove("leaderboard.txt")
        leaderboard_list.delete(0, tk.END)

def reset_player_records():
    if msg.askyesno("Confirm", "Delete ALL player records?"):
        for file in os.listdir():
            if file.endswith(".txt") and file != "leaderboard.txt":
                os.remove(file)
        history_list.delete(0, tk.END)
        history_list.insert(tk.END, "  All records deleted")

# ==============================
# START / NEW GAME
# ==============================
def start_game():
    global game_active, game_over
    if game_over:
        set_status("Press NEW GAME first")
        return
    p1 = p1_entry.get().strip()
    p2 = p2_entry.get().strip()
    if p1 == "" or p2 == "":
        set_status("Enter player names")
        return
    game_active = True
    update_pips()
    set_status("Waiting for Arduino...", "active")
    if serial_connected:
        ser.write(b"START\n")

def new_game():
    global p1_score, p2_score, round_number, game_over, game_active
    if serial_connected:
        ser.write(b"RESET\n")
    p1_score = 0
    p2_score = 0
    round_number = 1
    game_over = False
    game_active = False
    update_pips()
    set_status("New game ready")

# ==============================
# SERIAL READER
# ==============================
def read_serial():
    global p1_score, p2_score, round_number, game_over, game_active

    if not game_active or game_over:
        root.after(50, read_serial)
        return

    if serial_connected and ser.in_waiting:
        data = ser.readline().decode().strip()
        print(data)

        p1 = p1_entry.get().strip()
        p2 = p2_entry.get().strip()
        round_finished = False

        if data == "GO":
            set_status("GO!!!", "go")

        elif data == "P1_FALSE" and p2_score < 3:
            p2_score += 1
            history_list.insert(tk.END,
                f"  R{round_number}  {p1} FALSE START  →  {p1_score}-{p2_score}")
            history_list.itemconfig(tk.END, fg=DANGER)
            save_result(p2, p1, "WIN (FALSE START)")
            save_result(p1, p2, "LOSS (FALSE START)")
            round_finished = True

        elif data == "P2_FALSE" and p1_score < 3:
            p1_score += 1
            history_list.insert(tk.END,
                f"  R{round_number}  {p2} FALSE START  →  {p1_score}-{p2_score}")
            history_list.itemconfig(tk.END, fg=DANGER)
            save_result(p1, p2, "WIN (FALSE START)")
            save_result(p2, p1, "LOSS (FALSE START)")
            round_finished = True

        elif data.startswith("P1:") and p1_score < 3:
            t = float(data.split(":")[1]) / 1000
            p1_score += 1
            history_list.insert(tk.END,
                f"  R{round_number}  {p1} wins  {t:.3f}s  →  {p1_score}-{p2_score}")
            history_list.itemconfig(tk.END, fg=P1_COLOR)
            save_result(p1, p2, f"WIN ({t:.3f}s)")
            save_result(p2, p1, f"LOSS ({t:.3f}s)")
            round_finished = True

        elif data.startswith("P2:") and p2_score < 3:
            t = float(data.split(":")[1]) / 1000
            p2_score += 1
            history_list.insert(tk.END,
                f"  R{round_number}  {p2} wins  {t:.3f}s  →  {p1_score}-{p2_score}")
            history_list.itemconfig(tk.END, fg=P2_COLOR)
            save_result(p2, p1, f"WIN ({t:.3f}s)")
            save_result(p1, p2, f"LOSS ({t:.3f}s)")
            round_finished = True

        if p1_score == 3:
            history_list.insert(tk.END, f"  ★  WINNER: {p1.upper()}")
            history_list.itemconfig(tk.END, fg=ACCENT)
            update_leaderboard(p1, p2)
            game_over = True
            game_active = False
            set_status(f"{p1} wins the match!", "active")

        elif p2_score == 3:
            history_list.insert(tk.END, f"  ★  WINNER: {p2.upper()}")
            history_list.itemconfig(tk.END, fg=ACCENT)
            update_leaderboard(p2, p1)
            game_over = True
            game_active = False
            set_status(f"{p2} wins the match!", "active")

        update_pips()
        history_list.yview_moveto(1)

        if round_finished and not game_over:
            round_number += 1
            set_status("Next round...", "active")
            root.after(1000, lambda: ser.write(b"START\n"))

    root.after(50, read_serial)

# ==============================
# INIT
# ==============================
display_leaderboard()
update_pips()
read_serial()

root.mainloop()