import mqtt_remote_method_calls as com
import robot_controller as robo


def main():
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc(lego_robot_number=9)
    # robot.loop_forever()


main()
