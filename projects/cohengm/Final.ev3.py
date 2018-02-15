import mqtt_remote_method_calls as com
import robot_controller as robo
import ev3dev.ev3 as ev3
import time


class MyDelegate(object):

    def __init__(self):
        self.running = True


def main():
    robot = robo.Snatch3r()
    mqtt_robot = com.MqttClient(robot)
    mqtt_robot.connect_to_pc()

    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_pc()

    while True:
        if robot.color_sensor.color != ev3.ColorSensor.COLOR_RED or robot.color_sensor.color != ev3.ColorSensor.COLOR_WHITE:
            time.sleep(2)
            if robot.color_sensor.color == ev3.ColorSensor.COLOR_WHITE:
                ev3.Sound.speak("Found Radiation").wait()
                mqtt_client.send_message("check", [5])

            if robot.color_sensor.color == ev3.ColorSensor.COLOR_RED:
                ev3.Sound.speak("DETH").wait()
                robot.turn_degrees(360, 400)
            time.sleep(2)


main()
