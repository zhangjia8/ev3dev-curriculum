import ev3dev.ev3 as ev3
import time

import robot_controller as robo
import mqtt_remote_method_calls as com


class DataContainer(object):
    """ Helper class that might be useful to communicate between different callbacks."""

    def __init__(self):
        self.running = True


def main():
    print("--------------------------------------------")
    print("Finding something")
    print(" - Use IR remote channel 1 to drive around")
    print(" - Use IR remote channel 2 to for the arm")
    print(" - Press the Back button on EV3 to exit")
    print("--------------------------------------------")
    ev3.Sound.speak("Find in something")

    ev3.Leds.all_off()  # Turn the leds off
    robot = robo.Snatch3r()
    dc = DataContainer()

    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_pc()
    robot.pixy.mode = "SIG2"
    # For our standard shutdown button.
    btn = ev3.Button()
    btn.on_backspace = lambda state: handle_shutdown(state, dc)

    robot.arm_calibration()  # Start with an arm calibration in this program.

    rc1 = ev3.RemoteControl(channel=1)

    rc1.on_red_up = lambda state: handle_red_up_1(state, robot)
    rc1.on_red_down = lambda state: handle_red_down_1(state, robot)
    rc1.on_blue_up = lambda state: handle_blue_up_1(state, robot)
    rc1.on_blue_down = lambda state: handle_blue_down_1(state, robot)

    rc2 = ev3.RemoteControl(channel=2)

    rc2.on_red_up = lambda state: handle_red_up_2(state, robot)
    rc2.on_red_down = lambda state: handle_red_down_2(state, robot)
    rc2.on_blue_up = lambda state: handle_blue_up_2(state, robot)

    while dc.running:
        rc1.process()
        rc2.process()
        btn.process()

        x = robot.pixy.value(1)
        y = robot.pixy.value(2)
        width = robot.pixy.value(3)
        height = robot.pixy.value(4)
        mqtt_client.send_message("on_rectangle_update", [x, y, width, height])

        if robot.ir_sensor.proximity <= 10:
            ev3.Sound.speak("Found something!")
            time.sleep(0.01)
        time.sleep(0.25)

    print("Mission Complete.")
    ev3.Sound.speak("Mission Complete!").wait()
    mqtt_client.close()


def handle_red_up_1(button_state, robot):
    if button_state:
        robot.left_motor.run_forever(speed_sp=200)
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)

    else:
        robot.left_motor.stop()
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.BLACK)


def handle_red_down_1(button_state, robot):
    if button_state:
        robot.left_motor.run_forever(speed_sp=-200)
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED)

    else:
        robot.left_motor.stop()
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.BLACK)


def handle_blue_up_1(button_state, robot):
    if button_state:
        robot.right_motor.run_forever(speed_sp=200)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
    else:
        robot.right_motor.stop()
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.BLACK)


def handle_blue_down_1(button_state, robot):
    if button_state:
        robot.right_motor.run_forever(speed_sp=-200)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.RED)

    else:
        robot.right_motor.stop()
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.BLACK)


def handle_red_up_2(button_state, robot):
    if button_state:
        robot.arm_up()


def handle_red_down_2(button_state, robot):
    if button_state:
        robot.arm_down()


def handle_blue_up_2(button_state, robot):
    if button_state:
        robot.arm_calibration()


def handle_shutdown(button_state, dc):
    """Exit the program."""
    if button_state:
        dc.running = False


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
