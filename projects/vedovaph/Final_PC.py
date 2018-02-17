#I am trying to make the interface.........
"""
Author: Patrick Vedova.
"""
import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com
import math
import ev3dev.ev3 as ev3

score = 0
answer = 0
client = com.MqttClient

def main():
    """ Constructs a GUI """
    #This interface would pop up if the robot went over a white tile and would prompt the user to answer an addition problem



    def check_answer(value, answer, score):

        if int(value.get()) == answer:
            score = score + 10
        else:
            score = score - 10
        return score



    def get_question():

        randomNumber = 2
        #Random number between 1 and 5

        color_sensor = ev3.ColorSensor()

        addition_list = ['What is 9 + 10?','What is 27 + 38?','What is 1 + 6?','What is 6 + 9?','What is 3 + 7?']
        addition_solutions = [19, 65, 7, 15, 10]
        if color_sensor == ev3.ColorSensor.COLOR_WHITE:
            question = addition_list[randomNumber]
            answer = addition_solutions[randomNumber]

        subtraction_list = ['What is 9 - 10?', 'What is 38 - 27?', 'What is 6 - 1?', 'What is 9 - 6?', 'What is 7 - 3?']
        subtraction_answers = [-1, 11, 5, 3, 4]
        if color_sensor == ev3.ColorSensor.COLOR_BLUE:
            question = subtraction_list[randomNumber]
            answer = subtraction_answers[randomNumber]


        multiplication_list = ['What is 9*10?', 'What is 1*1?', 'What is 6*9?', 'What is 3*7?', 'What is 0*233?']
        multiplication_answers = [90, 1, 36, 21, 0]
        if color_sensor == ev3.ColorSensor.COLOR_RED:
            question = multiplication_list[randomNumber]
            answer = multiplication_answers[randomNumber]


        division_list = ['What is 10/2?', 'What is 4/1?', 'What 9/3?', 'What 12/6?', 'What 16/16?']
        division_answers = [5, 4, 3, 2, 1]
        if color_sensor == ev3.ColorSensor.COLOR_GREEN:
            question = division_list[randomNumber]
            answer = division_answers[randomNumber]


        #I Need to use statement: return [question, answer] and figure out how to make that work



    root = tkinter.Tk()
    root.title(get_question())

    main_frame = ttk.Frame(root, padding=70)
    main_frame.grid()  # only grid call that does NOT need a row and column

    answer_box_label = ttk.Label(main_frame, text="Type Answer Here")
    answer_box_label.grid(row=0,column=0)
    answer_box_entry = ttk.Entry(main_frame, width=8)
    answer_box_entry.insert(0, "")
    answer_box_entry.grid(row=1,column=0)

    Control_Pad_label = ttk.Label(main_frame, text='Control Pad')
    Control_Pad_label.grid(row=0, column=4)

    Score_label = ttk.Label(main_frame, text='(Score)')
    Score_label.grid(row=0,column=2)
    #Score_entry needs to be more sophisticated
    Score_entry = ttk.Label(main_frame, text= score)
    Score_entry.grid(row=1, column=2)


    Enter_button = ttk.Button(main_frame, text="Enter")
    Enter_button.grid(row=2,column=0)
    # Enter_button['command'] = lambda:
    root.bind('<Enter>', lambda event: print("Enter"))


    # Button for exit, need to make code just close the window/reopen the robot controller onscreen

    exit_button = ttk.Button(main_frame, text="Exit")
    exit_button.grid(row=4,column=5)
    exit_button['command'] = lambda: exit()

    #Robot control buttons
    forward_button = ttk.Button(main_frame, text="Forward")
    forward_button.grid(row=1,column=4)
    forward_button['command'] = lambda: drive_forward(client)
    root.bind('<Up>', lambda event: print("Forward key"))

    left_button = ttk.Button(main_frame, text="Left")
    left_button.grid(row=2,column=3)
    left_button['command'] = lambda: print("Left button")
    root.bind('<Left>', lambda event: print("Left key"))

    stop_button = ttk.Button(main_frame, text="Stop")
    stop_button.grid(row=2,column=4)
    stop_button['command'] = lambda: print("Stop button")
    root.bind('<space>', lambda event: print("Stop key"))

    right_button = ttk.Button(main_frame, text="Right")
    right_button.grid(row=2,column=5)
    right_button['command'] = lambda: print("Right button")
    root.bind('<Right>', lambda event: print("Right key"))

    back_button = ttk.Button(main_frame, text="Back")
    back_button.grid(row=3,column=4)
    back_button['command'] = lambda: print("Back button")
    root.bind('<Down>', lambda event: print("Back key"))

    read_question_button = ttk.Button(main_frame, text="Read Question")
    read_question_button.grid(row=4, column=3)
    read_question_button['command'] = lambda: print("Read Question")




    def drive_forward(client):
       client.send_message('drive_forever', [500, 500])

    root.mainloop()





main()






