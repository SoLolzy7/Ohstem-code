from motor import *
from mdv2 import *
from drivebase import *
from servo import *
from ble import *
from gamepad import *
from abutton import *
from pins import *

async def on_abutton_D3_double_pressed():
  global Auto
  robot.mode_auto = True
  neopix.show(0, hex_to_rgb('#0000ff'))
  robot.mode_auto = False

async def on_abutton_D3_pressed():
  global Auto
  Auto = 0
  robot.mode_auto = True
  neopix.show(0, hex_to_rgb('#00ff00'))
  robot.speed(100, min_speed=80)
  robot.use_gyro(False)
  await robot.forward_for(40, unit=CM, then=BRAKE)
  await robot.move_right_for(6, unit=SECOND, then=BRAKE)
  robot.mode_auto = False

async def on_abutton_D4_pressed():
  global Auto
  robot.mode_auto = True
  neopix.show(0, hex_to_rgb('#ff0000'))
  robot.mode_auto = False

async def on_abutton_D4_double_pressed():
  global Auto
  robot.mode_auto = True
  neopix.show(0, hex_to_rgb('#ffff00'))
  robot.speed(80, min_speed=50)
  await robot.forward_for(1, unit=SECOND, then=STOP)
  await robot.turn_right_for(1, unit=SECOND, then=STOP)
  await robot.forward_for(1, unit=SECOND, then=STOP)
  await motor6.run_time(speed=70, time=5*1000, then=STOP)
  await robot.move_left_for(5, unit=SECOND, then=STOP)
  robot.mode_auto = False

Auto = None
md_v2 = MotorDriverV2()
motor1 = DCMotor(md_v2, M1, reversed=False)
motor2 = DCMotor(md_v2, M2, reversed=False)
motor3 = DCMotor(md_v2, E1, reversed=False)
motor4 = DCMotor(md_v2, E2, reversed=False)
robot = DriveBase(MODE_MECANUM, m1=motor4, m2=motor3, m3=motor2, m4=motor1)
servo1 = Servo(md_v2, S1, 180)
motor5 = DCMotor(md_v2, M3, reversed=True)
motor6 = DCMotor(md_v2, M4, reversed=True)
gamepad = Gamepad()
btn_D3= aButton(D3_PIN)
btn_D4= aButton(D4_PIN)
led_D13 = Pins(D13_PIN)

def deinit():
  robot.stop()
  btn_D3.deinit()
  btn_D4.deinit()

import yolo_uno
yolo_uno.deinit = deinit

async def task_N_q_g_T():
  global Auto
  while True:
    await asleep_ms(1)
    if (gamepad.data[ARY]) > 50:
      await motor5.run_time(speed=100, time=0.25*1000, then=STOP)
    if (gamepad.data[ARY]) <= -50:
      await motor5.run_time(speed=(-100), time=0.25*1000, then=STOP)
    if gamepad.data[BTN_R1] == 1:
      motor6.run(100)
    if gamepad.data[BTN_R2] == 1:
      motor6.run(0)
    if gamepad.data[BTN_L1] == 1:
      await servo1.run_angle(angle=90, speed=100)
    if gamepad.data[BTN_L2] == 1:
      await servo1.run_angle(angle=0, speed=100)

async def task_u_B_C_r():
  global Auto
  while True:
    await asleep_ms(1)
    if False:
      pass

async def task_w_F_d_x():
  global Auto
  while True:
    await asleep_ms(1000)
    led_D13.toggle()

async def setup():
  global Auto
  print('App started')
  neopix.show(0, hex_to_rgb('#ff0000'))
  motor3.set_encoder(rpm=130, ppr=11, gears=34)
  motor4.set_encoder(rpm=130, ppr=11, gears=34)
  robot.size(wheel=80, width=360)
  servo1.limit(min=0, max=180)
  await servo1.run_angle(angle=0, speed=100)
  robot.speed(100, min_speed=60)
  neopix.show(0, hex_to_rgb('#ffffff'))

  btn_D3.double_pressed(on_abutton_D3_double_pressed)
  btn_D3.pressed(on_abutton_D3_pressed)
  btn_D4.pressed(on_abutton_D4_pressed)
  btn_D4.double_pressed(on_abutton_D4_double_pressed)
  create_task(ble.wait_for_msg())
  create_task(gamepad.run())
  create_task(robot.run_teleop(gamepad, accel_steps=3))
  create_task(task_N_q_g_T())
  create_task(task_u_B_C_r())
  create_task(task_w_F_d_x())

async def main():
  await setup()
  while True:
    await asleep_ms(100)

run_loop(main())
