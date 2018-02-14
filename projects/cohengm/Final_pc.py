# import ev3dev.ev3 as ev3
# import time
# import math
import tkinter
from tkinter import ttk
# import robot_controller as robo
import mqtt_remote_method_calls as com


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

    radiation_title = ttk.Label(main_frame, text="Find Radiation Poison!")
    radiation_title.grid(row=0, column=4)

    radiation_count = ttk.Label(radiation_frame, text="Radiation Spots= ")
    radiation_count.grid()

    speed_entry = 300

    inches_label = ttk.Label(control_frame, text="Inches")
    inches_label.grid(row=0, column=2)
    inches_entry = ttk.Entry(control_frame, width=8)
    inches_entry.insert(0, "6")
    inches_entry.grid(row=1, column=2)

    my_delegate = MyDelegate(canvas)
    mqtt_draw = com.MqttClient(my_delegate)
    mqtt_draw.connect("draw", "draw")

    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    forward_button = ttk.Button(control_frame, text="Forward")
    forward_button.grid(row=3, column=2)
    forward_button['command'] = lambda: send_forward(mqtt_client, inches_entry, speed_entry, mqtt_draw)
    root.bind('<Up>', lambda event: send_forward(mqtt_client, inches_entry, speed_entry, mqtt_draw))

    left_button = ttk.Button(control_frame, text="Left")
    left_button.grid(row=4, column=1)
    # left_button and '<Left>' key
    left_button['command'] = lambda: send_left(mqtt_client)
    root.bind('<Left>', lambda event: send_left(mqtt_client))

    stop_button = ttk.Button(control_frame, text="Stop")
    stop_button.grid(row=4, column=2)
    # stop_button and '<space>' key (note, does not need left_speed_entry, right_speed_entry)
    stop_button['command'] = lambda: send_stop(mqtt_client)
    root.bind('<space>', lambda event: send_stop(mqtt_client))

    right_button = ttk.Button(control_frame, text="Right")
    right_button.grid(row=4, column=3)
    # right_button and '<Right>' key
    right_button['command'] = lambda: send_right(mqtt_client)
    root.bind('<Right>', lambda event: send_right(mqtt_client))

    back_button = ttk.Button(control_frame, text="Back")
    back_button.grid(row=5, column=2)
    # back_button and '<Down>' key
    back_button['command'] = lambda: send_back(mqtt_client, inches_entry, speed_entry)
    root.bind('<Down>', lambda event: send_back(mqtt_client, inches_entry, speed_entry))

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
    delegate.send_message("on_circle_draw", ["green", 400, 200])


def send_left(mqtt_client):
    print("Left")
    mqtt_client.send_message("turn_degrees", [90, 300])


def send_right(mqtt_client):
    print("Right")
    mqtt_client.send_message("turn_degrees", [-90, 300])


def send_back(mqtt_client, inches, speed):
    print("Back")
    mqtt_client.send_message("drive_inches", [-int(inches.get()), -int(speed)])


def send_stop(mqtt_client):
    print("Stop")
    mqtt_client.send_message("drive_forever", [0, 0])


# Quit and Exit button callbacks
def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


class MyDelegate(object):

    def __init__(self, canvas):
        self.canvas = canvas
        self.radiaiton_count = 0
        self.x = 400
        self.y = 250

    def on_circle_draw(self, color, x, y):
        self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill=color, width=3)

    def found(self):
        self.radiaiton_count = 1


main()
