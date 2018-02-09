# import ev3dev.ev3 as ev3
# import time
import math
import tkinter
from tkinter import ttk
# import robot_controller as robo
import mqtt_remote_method_calls as com


def main():
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title("Bomb Squad")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    # Make a tkinter.Canvas on a Frame.
    canvas = tkinter.Canvas(main_frame, background="lightgray", width=800, height=500)
    canvas.grid(row=1, column=2)

    canvas.create_oval(390, 240, 410, 260, fill="red", width=3)

    # Make callbacks for mouse click events.
    canvas.bind("<Button-1>", lambda event: clicked(event, canvas, 500))

    quit_button = ttk.Button(main_frame, text="Quit")
    quit_button.grid(row=1, column=3)
    quit_button["command"] = lambda: quit_program(mqtt_client)

    my_delegate = MyDelegate(canvas)
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect("draw", "draw")

    bomb_squad = ttk.Label(main_frame, text="Find Some Bombs!")
    bomb_squad.grid(row=0, column=2)

    root.mainloop()


def clicked(event, canvas, speed):

    my_delegate = MyDelegate(canvas)
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect("draw", "draw")

    print("You clicked location ({},{})".format(event.x, event.y))
    my_color = "green"  # Color of circle
    mqtt_client.send_message("on_circle_draw", [my_color, event.x, event.y])

    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    x = math.fabs(event.x - my_delegate.eventxold)
    y = math.fabs(event.y - my_delegate.eventyold)
    # distance = math.sqrt(x**2 + y**2)/10
    angle = math.tan(y/x)*180/math.pi
    degrees = 10

    # Upper Right Quadrant
    if event.x >= 400 and event.y <= 250:
        degrees = angle
    print("Deg: ", degrees)
    print("X: ", x)
    print("Y: ", y)
    # # Upper Left Quadrant
    # if event.x <= 400 & event.y <= 250:
    #     degrees = -(90-angle)
    # # Lower Right Quadrant
    # if event.x >= 400 & event.y >= 250:
    #     degrees = 90 + angle
    # # Lower Left Quadrant
    # if event.x <= 400 & event.y >= 250:
    #     degrees = -(90 + angle)
    # print("turn_degrees")
    mqtt_client.send_message("turn_degrees", [degrees, speed])
    # print("drive_inches")
    # mqtt_client.send_message("drive_inches", [distance, speed])
    my_delegate.eventxold = event.x
    my_delegate.eventyold = event.y


def clear(canvas):
    """Clears the canvas contents"""
    canvas.delete("all")


def quit_program(mqtt_client):
    """For best practice you should close the connection.  Nothing really "bad" happens if you
       forget to close the connection though. Still it seems wise to close it then exit."""
    if mqtt_client:
        mqtt_client.close()
    exit()


class MyDelegate(object):

    def __init__(self, canvas):
        self.canvas = canvas
        self.eventxold = 400
        self.eventyold = 250

    def on_circle_draw(self, color, x, y):
        self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill=color, width=3)


main()
