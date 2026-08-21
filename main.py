import tkinter as tk
from PIL import Image,ImageTk
import time
from math import floor

from config import * 
reps = 1
reset = False
check_marks = []

#Basic Layout
app = tk.Tk()
# app.geometry('550x550')
app.config(bg=YELLOW,pady=30,padx=120)
app.title("POMODORO")

#Big on screen title 3 modes TIMER WORK BREAK
state_label = tk.Label(app,text="Timer",font=(TITLE_FONT_NAME,50))
state_label.config(fg=GREEN,bg=YELLOW,pady=30)
state_label.grid(column=1,row=0,columnspan=1)

#centre image of a tomato tomato.png plus timer itself 
image = Image.open("tomato.png")
tomato_photo = ImageTk.PhotoImage(image)
tomato_image_label = tk.Label(app,text=f"00:00",image=tomato_photo,compound='center',bg=YELLOW,font=(FONT_NAME,35,'bold'),fg='white')
tomato_image_label.grid(column=1,row=1)

#TODO change the code to alter the text here and no the label above 
#create the image text(timer) pair using canvas
#
# canvas = tk.Canvas(width=200,height=224,bg=YELLOW,highlightthickness=0)
# tomato_image = tk.PhotoImage(file='tomato.png')
# canvas.create_image(100,112,tomato_image)
# canvas.create_text(100,130,text="00:00",fill='white',font=(FONT_NAME,35,'bold'))

def reset_var_reset():
    '''use this function to be able to run the start timer func again after reset when button is pressed '''
    global reset
    reset = False
def start_timer_5(minutes=SHORT_BREAK_MIN-1,seconds=59):
    if reset:
        return
    if seconds == 0 and  minutes != 0 :
        seconds = 59
        returned_min = minutes - 1
    else:
        returned_min = minutes
    state_label.config(text="Short Break",fg=PINK)
    tomato_image_label.config(text=f"{returned_min:02d}:{seconds:02d}")
    if minutes == 0 and seconds == 0 :
        return 
    returned_sec = seconds - 1
    app.after(after_var_delay,start_timer_5,returned_min,returned_sec)

def start_timer_20(minutes=LONG_BREAK_MIN-1,seconds=59):
    if reset:
        return 
    if seconds == 0 and  minutes != 0 :
        seconds = 59
        returned_min = minutes - 1
    else:
        returned_min = minutes
    state_label.config(text="Long Break",fg=PINK)
    tomato_image_label.config(text=f"{returned_min:02d}:{seconds:02d}")
    # maybe later you add a big check mark for finishing all 
    if minutes == 0 and seconds == 0 :
        return 
    returned_sec = seconds - 1
    app.after(after_var_delay,start_timer_20,returned_min,returned_sec)

def start_timer_25(minutes=WORK_MIN-1,seconds=59):
    global check_marks
    start_button.config(state='disabled')
    #if reset button is pressed
    if reset:
        return 
    #if seconds = 0 and there are minutes left turn second to 59 after pausing at 0 for a second 

    state_label.config(text="Timer Started")
    tomato_image_label.config(text=f"{minutes:02d}:{seconds:02d}")
    if minutes == 0 and seconds == 0 :
        check_marks.append(CHECK_MARK_EMOJI)
        display_check_marks()
        if check_for_completion():
            reset_var_reset()
            start_timer_20()
            return
        start_timer_5()
        return
    if seconds == 0 and  minutes != 0 :
        returned_sec = 59
        returned_min = minutes - 1
    else:
        returned_min = minutes
        returned_sec = seconds - 1
    app.after(after_var_delay,start_timer_25,returned_min,returned_sec)

start_button = tk.Button(app,text="Start",font=(FONT_NAME,10),command=lambda: [reset_var_reset() ,start_timer_25()],width=5,state='active',padx=10,pady=10)
start_button.grid(column=0,row=2)

def reset_timer():
    '''Used when the reset button is pressed'''
    global reset,check_marks
    reset = True
    tomato_image_label.config(text='00:00')
    start_button.config(state='active')
    if len(check_marks) == 4:
        check_marks = []
    return

reset_button = tk.Button(app,text="Reset",font=(FONT_NAME,10),command=lambda: [reset_timer()] ,width=5,padx=10,pady=10)
reset_button.grid(column=2,row=2)

def display_check_marks():
    '''used to display check markes every successfull 25 minutes'''
    check_marks_label = tk.Label(text=f"{" ".join(check_marks)}",font=(FONT_NAME,15,),bg=YELLOW,width=5)
    check_marks_label.config(padx=100,pady=30)
    check_marks_label.grid(column=1,row=4,columnspan=1)


def check_for_completion():
    '''used to check wether user completed 4 25 minutes sessions to start 20 minutes break'''
    if len(check_marks) == 4:
        return True
    

app.mainloop()
