import mqtt_remote_method_calls as com
import robot_controller as robo
import ev3dev.ev3 as ev3
import time


def main():
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()

    while True:
        if robot.color_sensor.color == ev3.ColorSensor.COLOR_WHITE:
            ev3.Sound.speak("Found Radiation").wait()
            mqtt_client.send_message("found")
        time.sleep(2)


main()
