import mqtt_remote_method_calls as com
import robot_controller as robo
import ev3dev.ev3 as ev3
import time


def main():
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()

    ev3.Sound.beep()

    # while robot.color_sensor.color == ev3.ColorSensor.COLOR_WHITE:
    #     robot.drive_forever(0, 0)
    #     ev3.Sound.speak("Found Bomb").wait()

    robot.loop_forever()


main()
