# import ev3dev.ev3 as ev3
# import time
# import math
import tkinter
from tkinter import ttk
# import robot_controller as robo
import mqtt_remote_method_calls as com


class MyDelegate(object):

    def __init__(self, canvas):
        self.canvas = canvas
        self.xold = 400
        self.yold = 250
        self.turns = 0
        self.color = "green"

    def on_circle_draw(self, inches):

        if self.turns == -3:
            self.turns = 1
        if self.turns == 3:
            self.turns = -1

        x = 0
        y = 0

        if self.turns % 3 == 0:
            x = self.xold
            y = self.yold - inches*10
        if self.turns % 3 == 1:
            x = self.xold + inches*10
            y = self.yold
        if self.turns % 3 == 2:
            x = self.xold - inches*10
            y = self.yold
        if self.turns == 2 or self.turns == -2:
            x = self.xold
            y = self.yold + inches*10

        self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill=self.color, width=3)

        self.xold = x
        self.yold = y

    def turn_right(self):
        self.turns = self.turns + 1

    def turn_left(self):
        self.turns = self.turns - 1

    def changeblue(self):
        self.color = "blue"

    def changegreen(self):
        self.color = "green"

    def changeyellow(self):
        self.color = "yellow"


def main():
    root = tkinter.Tk()
    root.title("Find The Radiation")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid(row=0, column=0)

    control_frame = ttk.Frame(root, padding=20, relief='raised')
    control_frame.grid(row=0, column=1)

    radiation_frame = ttk.Frame(root, padding=20, relief='raised')
    radiation_frame.grid(row=0, column=2)

    # Make a tkinter.Canvas on a Frame.
    canvas = tkinter.Canvas(main_frame, background="lightgray", width=800, height=500)
    canvas.grid(row=2, column=4)

    canvas.create_oval(390, 240, 410, 260, fill="green", width=3)

    my_delegate = MyDelegate(canvas)
    mqtt_draw = com.MqttClient(my_delegate)
    mqtt_draw.connect("draw", "draw")

    count_button = tkinter.Button(radiation_frame, text="CHECK", fg="red", bg="white")
    count_button.grid()
    count_button['command'] = lambda: send_check(mqtt_client)

    radiation_label = ttk.Label(radiation_frame, text="Radiation Count")
    radiation_label.grid()

    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    inches_label = ttk.Label(control_frame, text="Inches")
    inches_label.grid(row=0, column=2)
    inches_entry = ttk.Entry(control_frame, width=8)
    inches_entry.insert(0, "6    ")
    inches_entry.grid(row=1, column=2)

    speed_entry = 300

    def bluer():
        mqtt_draw.send_message("changeblue")

    def greener():
        mqtt_draw.send_message("changegreen")

    def yellower():
        mqtt_draw.send_message("changeyellow")

    radiation_color = ttk.Checkbutton
    blue = ttk.Checkbutton(control_frame, text='Blue Sensor', command=bluer,
                           variable=radiation_color)
    green = ttk.Checkbutton(control_frame, text='Green Sensor', command=greener, variable=radiation_color)
    yellow = ttk.Checkbutton(control_frame, text='Yellow Sensor', command=yellower, variable=radiation_color)
    yellow.grid()
    green.grid()
    blue.grid()

    forward_button = ttk.Button(control_frame, text="Forward")
    forward_button.grid(row=3, column=2)
    forward_button['command'] = lambda: send_forward(mqtt_client, inches_entry, speed_entry, mqtt_draw)
    root.bind('<Up>', lambda event: send_forward(mqtt_client, inches_entry, speed_entry, mqtt_draw))

    left_button = ttk.Button(control_frame, text="Left")
    left_button.grid(row=4, column=1)
    # left_button and '<Left>' key
    left_button['command'] = lambda: send_left(mqtt_client, mqtt_draw)
    root.bind('<Left>', lambda event: send_left(mqtt_client, mqtt_draw))

    stop_button = ttk.Button(control_frame, text="Stop")
    stop_button.grid(row=4, column=2)
    # stop_button and '<space>' key (note, does not need left_speed_entry, right_speed_entry)
    stop_button['command'] = lambda: send_stop(mqtt_client)
    root.bind('<space>', lambda event: send_stop(mqtt_client))

    right_button = ttk.Button(control_frame, text="Right")
    right_button.grid(row=4, column=3)
    # right_button and '<Right>' key
    right_button['command'] = lambda: send_right(mqtt_client, mqtt_draw)
    root.bind('<Right>', lambda event: send_right(mqtt_client, mqtt_draw))

    back_button = ttk.Button(control_frame, text="Back")
    back_button.grid(row=5, column=2)
    # back_button and '<Down>' key
    back_button['command'] = lambda: send_back(mqtt_client, inches_entry, speed_entry, mqtt_draw)
    root.bind('<Down>', lambda event: send_back(mqtt_client, inches_entry, speed_entry, mqtt_draw))

    # Buttons for quit and exit
    q_button = ttk.Button(control_frame, text="Quit")
    q_button.grid(row=6, column=3)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))

    e_button = ttk.Button(control_frame, text="Exit")
    e_button.grid(row=7, column=3)
    e_button['command'] = (lambda: quit_program(mqtt_client, True))

    root.mainloop()


def clear(canvas):
    """Clears the canvas contents"""
    canvas.delete("all")


def send_forward(mqtt_client, inches, speed, delegate):
    print("Forward")
    mqtt_client.send_message("drive_inches", [int(inches.get()), int(speed)])
    delegate.send_message("on_circle_draw", [int(inches.get())])


def send_left(mqtt_client, delegate):
    print("Left")
    mqtt_client.send_message("turn_degrees", [90, 300])
    delegate.send_message("turn_left")


def send_right(mqtt_client, delegate):
    print("Right")
    mqtt_client.send_message("turn_degrees", [270, 300])
    delegate.send_message("turn_right")


def send_back(mqtt_client, inches, speed, delegate):
    print("Back")
    mqtt_client.send_message("drive_inches", [-int(inches.get()), -int(speed)])
    delegate.send_message("on_circle_draw", [-int(inches.get())])


def send_stop(mqtt_client):
    print("Stop")
    mqtt_client.send_message("drive_forever", [0, 0])


def send_check(mqtt_client):
    print("Sending Check")
    mqtt_client.send_message("check_rad")


# Quit and Exit button callbacks
def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


main()
