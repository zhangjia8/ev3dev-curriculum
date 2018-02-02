"""
  Library of EV3 robot functions that are useful in many different applications. For example things
  like arm_up, arm_down, driving around, or doing things with the Pixy camera.

  Add commands as needed to support the features you'd like to implement.  For organizational
  purposes try to only write methods into this library that are NOT specific to one tasks, but
  rather methods that would be useful regardless of the activity.  For example, don't make
  a connection to the remote control that sends the arm up if the ir remote control up button
  is pressed.  That's a specific input --> output task.  Maybe some other task would want to use
  the IR remote up button for something different.  Instead just make a method called arm_up that
  could be called.  That way it's a generic action that could be used in any task.
"""

import ev3dev.ev3 as ev3
import math
import time


class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""

    def __init__(self):
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.touch_sensor = ev3.TouchSensor()
        self.MAX_SPEED = 900

    def drive_inches(self, inches_target, speed_deg_per_second):
        """Drives in inches given an amount of inches to drive and how fast in degrees per second."""

        # Check that the motors are actually connected
        assert self.left_motor.connected
        assert self.right_motor.connected

        inches = inches_target
        speed = speed_deg_per_second
        self.left_motor.run_to_rel_pos(position_sp=inches * 90, speed_sp=speed,
                                       stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.right_motor.run_to_rel_pos(position_sp=inches * 90, speed_sp=speed,
                                        stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def turn_degrees(self, degrees_to_turn, turn_speed_sp):
        """Turing robot given in degrees to turn and speed to turn in degrees per second"""
        assert self.left_motor.connected
        assert self.right_motor.connected

        degrees = degrees_to_turn * 4.5
        speed = turn_speed_sp
        if degrees > 0:
            self.left_motor.run_to_rel_pos(position_sp=-degrees, speed_sp=speed,
                                           stop_action=ev3.Motor.STOP_ACTION_BRAKE)
            self.right_motor.run_to_rel_pos(position_sp=degrees, speed_sp=speed,
                                            stop_action=ev3.Motor.STOP_ACTION_BRAKE)
            self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)
            self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        if degrees < 0:
            self.left_motor.run_to_rel_pos(position_sp=degrees, speed_sp=speed,
                                           stop_action=ev3.Motor.STOP_ACTION_BRAKE)
            self.right_motor.run_to_rel_pos(position_sp=-degrees, speed_sp=speed,
                                            stop_action=ev3.Motor.STOP_ACTION_BRAKE)
            self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)
            self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def arm_calibration(self):
        """
            Runs the arm up until the touch sensor is hit then back to the bottom again, beeping at both locations.
            Once back at in the bottom position, gripper open, set the absolute encoder position to 0.  You are
            calibrated!
            The Snatch3r arm needs to move 14.2 revolutions to travel from the touch sensor to the open position.
            """
        self.arm_motor.run_forever(speed_sp=self.MAX_SPEED)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action="brake")
        arm_revolutions_for_full_range = 14.2 * 360
        self.arm_motor.run_to_rel_pos(position_sp=-arm_revolutions_for_full_range, speed_sp=self.MAX_SPEED)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()

        self.arm_motor.position = 0  # Calibrate the down position as 0 (this line is correct as is).

    def arm_up(self):
        """Moves the Snatch3r arm to the up position."""
        self.arm_motor.run_to_rel_pos(position_sp=14.2 * 360, speed_sp=self.MAX_SPEED)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action="brake")
        ev3.Sound.beep().wait()

    def arm_down(self):
        """Moves the Snatch3r arm to the down position."""
        self.arm_motor.run_to_abs_pos(position_sp=0)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)  # Blocks until the motor finishes running
        ev3.Sound.beep().wait()

    def shutdown(self):
        self.left_motor.stop()
        self.right_motor.stop()
        self.arm_motor.stop()
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
        print("Goodbye!")
        ev3.Sound.speak("Goodbye").wait()