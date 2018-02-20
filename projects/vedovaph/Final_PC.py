#I am trying to make the interface.........
"""
Author: Patrick Vedova.
"""
import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com
import math
import ev3dev.ev3 as ev3
import robot_controller as robo


class MyDelegate(object):
    def __init__(self):
        self.color = 6

    def color_sensor(self, color):
        self.color = color

    def getColor(self):
        return self.color

score = 0
answer = 0

addition_list = ['What is 9 plus 10?','What is 27 plus 38?','What is 1 plus 6?','What is 6 plus 9?','What is 3 plus 7?']
subtraction_list = ['What is 9 minus 10?', 'What is 38 minus 27?', 'What is 6 minus 1?', 'What is 9 minus 6?', 'What is 7 minus 3?']
multiplication_list = ['What is 9 times 10?', 'What is 1 times 1?', 'What is 6 times 9?', 'What is 3 times 7?', 'What is 0 times 233?']
division_list = ['What is 10 divided by 2?', 'What is 4 divided by 1?', 'What is 9 divided by 3?', 'What is 12 divided by 6?', 'What is 16 divided by 16?']

addition_answers = [19, 65, 7, 15, 10]
subtraction_answers = [-1, 11, 5, 3, 4]
multiplication_answers = [90, 1, 36, 21, 0]
division_answers = [5, 4, 3, 2, 1]

mydelegate = MyDelegate()

Score_text = 0

def drive_forward(client):
    client.send_message("drive_forever", [500, 500])


def drive_backward(client):
    client.send_message("drive_forever", [-500, -500])


def stop_handle(client):
    client.send_message("stop", [])


def turn_left(client):
    client.send_message("turn_degrees", [90, 500])


def turn_right(client):
    client.send_message("turn_degrees", [-90, 500])

def get_question(client):
    print('get_question')
    randomNumber = 2
    #Random number between 1 and 5

    color_sensor = mydelegate.getColor()

    #addition_list = ['What is 9 + 10?','What is 27 + 38?','What is 1 + 6?','What is 6 + 9?','What is 3 + 7?']
    #addition_solutions = [19, 65, 7, 15, 10]
    #White
    if color_sensor == 6:
        question = addition_list[randomNumber]
        answer = addition_answers[randomNumber]
        root.wm_title(question)

    #subtraction_list = ['What is 9 - 10?', 'What is 38 - 27?', 'What is 6 - 1?', 'What is 9 - 6?', 'What is 7 - 3?']
    #subtraction_answers = [-1, 11, 5, 3, 4]
    #Blue
    if color_sensor == 2:
        question = subtraction_list[randomNumber]
        answer = subtraction_answers[randomNumber]
        root.wm_title(question)

    #multiplication_list = ['What is 9*10?', 'What is 1*1?', 'What is 6*9?', 'What is 3*7?', 'What is 0*233?']
    #multiplication_answers = [90, 1, 36, 21, 0]
    #Red
    if color_sensor == 5:
        question = multiplication_list[randomNumber]
        answer = multiplication_answers[randomNumber]
        root.wm_title(question)

    #division_list = ['What is 10/2?', 'What is 4/1?', 'What is 9/3?', 'What 12/6?', 'What 16/16?']
    #division_answers = [5, 4, 3, 2, 1]
    #Black
    if color_sensor == 1:
        question = division_list[randomNumber]
        answer = division_answers[randomNumber]
        root.wm_title(question)

    client.send_message('read_q', [question])

def updateScore(score1, main_frame):
    global Score_text
    Score_text += score1
    Score_label = ttk.Label(main_frame, text='(Score)')
    Score_label.grid(row=0, column=2)
    Score_entry = ttk.Label(main_frame, text=Score_text)
    Score_entry.grid(row=1, column=2)



root = tkinter.Tk()


main_frame = ttk.Frame(root, padding=70)
main_frame.grid()  # only grid call that does NOT need a row and column


answer_box_label = ttk.Label(main_frame, text="Type Answer Here")
answer_box_label.grid(row=0, column=0)
answer_box_entry = ttk.Entry(main_frame, width=8)
answer_box_entry.insert(0, "")
answer_box_entry.grid(row=1, column=0)

Control_Pad_label = ttk.Label(main_frame, text='Control Pad')
Control_Pad_label.grid(row=0, column=4)

updateScore(0, main_frame)


client = com.MqttClient(mydelegate)
client.connect_to_ev3(lego_robot_number=9)

Enter_button = ttk.Button(main_frame, text="Enter")
Enter_button.grid(row=2, column=0)
Enter_button['command'] = lambda: check_answer(answer_box_entry.get(), main_frame)
root.bind('<Enter>', lambda event: print("Enter"))

# Button for exit, need to make code just close the window/reopen the robot controller onscreen

exit_button = ttk.Button(main_frame, text="Exit")
exit_button.grid(row=4, column=5)
exit_button['command'] = lambda: exit()

# Robot control buttons
forward_button = ttk.Button(main_frame, text="Forward")
forward_button.grid(row=1, column=4)
forward_button['command'] = lambda: drive_forward(client)
root.bind('<Up>', lambda event: print("Forward key"))

left_button = ttk.Button(main_frame, text="Left")
left_button.grid(row=2, column=3)
left_button['command'] = lambda: turn_left(client)
root.bind('<Left>', lambda event: print("Left key"))

stop_button = ttk.Button(main_frame, text="Stop")
stop_button.grid(row=2, column=4)
stop_button['command'] = lambda: stop_handle(client)
root.bind('<space>', lambda event: print("Stop key"))

right_button = ttk.Button(main_frame, text="Right")
right_button.grid(row=2, column=5)
right_button['command'] = lambda: turn_right(client)
root.bind('<Right>', lambda event: print("Right key"))

back_button = ttk.Button(main_frame, text="Back")
back_button.grid(row=3, column=4)
back_button['command'] = lambda: drive_backward(client)
root.bind('<Down>', lambda event: print("Back key"))

read_question_button = ttk.Button(main_frame, text="Read Question")
read_question_button.grid(row=4, column=3)
read_question_button['command'] = lambda: get_question(client)


def check_answer(value, main_frame):
    ansList = []
    ansIndex = 0
    for k in range(5):

        if root.wm_title() == addition_list[k]:
            ansIndex = k
            ansList = addition_answers

        if root.wm_title() == subtraction_list[k]:
            ansIndex = k
            ansList = subtraction_answers

        if root.wm_title() == multiplication_list[k]:
            ansIndex = k
            ansList = multiplication_answers
        if root.wm_title() == division_list[k]:
            ansIndex = k
            ansList = division_answers
    print(ansList[ansIndex])
    print(value)
    print(int(ansList[ansIndex]) == int(value))
    if int(ansList[ansIndex]) == int(value):
        score = 10
        client.send_message('read_q', ['correct'])
    else:
        score = -10
        client.send_message('read_q', ['you are wrong haha'])
    updateScore(score, main_frame)



def main():
    """ Constructs a GUI """
    #This interface would pop up if the robot went over a white tile and would prompt the user to answer an addition prob

    root.mainloop()


main()






