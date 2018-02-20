#Code that will be uploaded to the robot

import time
import ev3dev.ev3 as ev3
import mqtt_remote_method_calls as com
import robot_controller as robo

robot = robo.Snatch3r()
client = com.MqttClient(robot)
client.connect_to_pc(lego_robot_number=9)

def main():
    while True:
        time.sleep(0.2)
        client.send_message("color_sensor", [robot.color_sensor.color])





main()