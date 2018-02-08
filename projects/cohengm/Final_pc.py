import ev3dev.ev3 as ev3
import time
import tkinter
from tkinter import ttk
import robot_controller as robo
import mqtt_remote_method_calls as com


def main():
    mqtt_client = None

    root = tkinter.Tk()
    root.title("MQTT Remote")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    # Make a tkinter.Canvas on a Frame.
    canvas = tkinter.Canvas(main_frame, background="lightgray", width=800, height=500)
    canvas.grid(row=1, column=2)

    # Make callbacks for mouse click events.
    canvas.bind("<Button-1>", lambda event: left_mouse_click(event, mqtt_client))

    quit_button = ttk.Button(main_frame, text="Quit")
    quit_button.grid(row=1, column=3)
    quit_button["command"] = lambda: quit_program(mqtt_client)

    my_delegate = MyDelegate(canvas)
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect("draw", "draw")

    bomb_squad = ttk.Label(main_frame, text="Bomb Squad!")
    bomb_squad.grid(row=0, column=2)

    root.mainloop()


def send_up(mqtt_client):
    print("arm_up")
    mqtt_client.send_message("arm_up")


def send_down(mqtt_client):
    print("arm_down")
    mqtt_client.send_message("arm_down")


def left_mouse_click(event, mqtt_client):
    """ Draws a circle onto the canvas (one way or another). """
    print("You clicked location ({},{})".format(event.x, event.y))
    my_color = "green"  # Make your color unique

    mqtt_client.send_message("on_circle_draw", [my_color, event.x, event.y])


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

    def on_circle_draw(self, color, x, y):
        self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill=color, width=3)


main()
