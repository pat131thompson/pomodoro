from tkinter import *
import math

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
BLACK = '#000000'
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
cycle_num = 0
timer = None

"""
------------------------
TIMER, COUNTDOWN & RESET
------------------------
all the functionality for the Pomodoro App comes from three functions;

start_count_down
(1) adds 1 to the cycle_num global variable.  This will allow differentiation between UX during the running
    of the app
(2) constant values from above are calculated in seconds for work time and the two break periods.  
    each is given a variable.
(3) the pomodoro technique naturally breaks into eight phases (variable cycle_num)
    if / elif / else statements define display functionality depending on the cycle_num
    each of these statements trigger the count_down() function
(4) the start_count_down function which is tied to the start button (command)
count_down
(1) this is triggered by the start_count_down() function
(2) the 'count' argument delivered to the count_down function is passed from the start_count_down() trigger 
(3) the math module (math.floor) and modulo calculations provide rounded down minutes and seconds for counting down.
    these are then presented as f-strings on the canvas.
(4) work sessions completed are marked by a check box (three work sessions per pomodoro cycle).  these are
    represented by appearing check marks created from a loop through a range.
reset_timer
(1) command tied to the reset button.
(2) uses the tkinter window.after_cancel method to then cancel the timer functionality
(3) display properties of "Timer" and losing the check marks are adjusted and cycle_num is set to zero
"""


def start_count_down():
    global cycle_num
    cycle_num += 1
    work_time_in_sec = WORK_MIN * 60
    short_break_in_sec = SHORT_BREAK_MIN * 60
    long_break_in_sec = LONG_BREAK_MIN * 60
    if cycle_num == 8:
        count_down(long_break_in_sec)
        title_label.config(text="BREAK", fg=RED)
    elif cycle_num % 2 == 0:
        count_down(short_break_in_sec)
        title_label.config(text="BREAK", fg=PINK)
    else:
        count_down(work_time_in_sec)
        title_label.config(text="WORK!", fg=GREEN)


def count_down(count):
    count_min = math.floor(count/60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        start_count_down()
        mark = ""
        work_sessions = math.floor(cycle_num/2)
        for n in range(work_sessions):
            mark += "✓"
        check_label.config(text=mark)


def reset_timer():
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Timer")
    check_label.config(text="")
    global cycle_num
    cycle_num = 0


"""
--------
UI SETUP
--------
(1) tkinter window is created and given a title and some dimensions (larger than the image that will be imported)
(2) an object of the canvas class is created and given dimensions consistent with the image size to be inserted
(3) a tomato_img variable is created referencing the image to be imported to the canvas (canvas.create_image)
(4) this tomato_img is positioned in the centre of the canvas widget using the grid method
(5) text is then layered onto the canvas (canvas.create_text)
(6) a title label is created, customised and placed using the grid method
(7) start and reset buttons are created and placed (commands are associated)
(8) checkmark label is added and positioned at the bottom
"""
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00.00", fill="black", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)
title_label = Label(text="Timer", font=(FONT_NAME, 35, "bold"), fg=GREEN, bg=YELLOW)
title_label.grid(column=1, row=0)
start_button = Button(text="Start", fg=BLACK, highlightthickness=0, command=start_count_down)
start_button.grid(column=0, row=2)
reset_button = Button(text="Reset", fg=BLACK, highlightthickness=0, command=reset_timer)
reset_button.grid(column=2, row=2)
check_label = Label(fg=GREEN, bg=YELLOW, font=(FONT_NAME, 20, "bold"))
check_label.grid(column=1, row=3)
window.mainloop()
