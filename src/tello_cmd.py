import cmd
import sys
import argparse

from tello import Tello

class ArgumentParser(argparse.ArgumentParser):
  def __init__(self, func, **kwarg):
    super().__init__(description=func.__doc__, **kwarg)

  def error(self, message):
    print(message, file=sys.stderr)
    self.print_help(sys.stderr)
  
  def parse_args(self, args=None, namespace=None):
    result = self.parse_known_args(args, namespace)
    if result == None:
      return False
    return super().parse_args(args, namespace)

def add_distance_arg(parser, name = 'x'):
  parser.add_argument(name, type=int, nargs=1, help='a distance in centimeters')
  return parser

def add_angle_arg(parser, name = 'x'):
  parser.add_argument(name, type=int, nargs=1, help='an angle in degrees')
  return parser

def add_direction_arg(parser, name = 'x'):
  parser.add_argument(name, type=string, nargs=1, help='a direction', choices=['l', 'r', 'f', 'b'])
  return parser

def add_speed_arg(parser, name = 'speed'):
  parser.add_argument(name, type=int, nargs=1, help='a speed in centimeters per second')
  return parser

# https://docs.python.org/3/library/cmd.html#cmd-example
class TelloCmd(cmd.Cmd):
  intro = 'Welcome to the tello shell.   Type help or ? to list commands.\n'
  prompt = '(tello) '
  file = None
  tello = Tello()
  
  def __init__(self):
    self.tello.send_command('command')
    super().__init__()

  # ----- basic commands -----
  # https://dl-cdn.ryzerobotics.com/downloads/Tello/Tello%20SDK%202.0%20User%20Guide.pdf
  def do_command(self, arg):
    'Enter SDK mode'
    self.tello.send_command('command')
  
  def do_takeoff(self, arg):
    'Auto takeoff'
    self.tello.send_command('takeoff')
  
  def do_land(self, arg):
    'Auto landing'
    self.tello.send_command('land')
  
  def do_streamon(self, arg):
    'Enable video stream'
    self.tello.send_command('streamon')
  
  def do_streamoff(self, arg):
    'Disable video stream'
    self.tello.send_command('streamoff')
  
  def do_emergency(self, arg):
    'Stop motors immediately'
    self.tello.send_command('emergency')
  
  def do_up(self, arg):
    'up x: Ascend to "x" cm. x=20-500: up 40'
    parser = ArgumentParser(self.do_up, prog='up')
    if add_distance_arg(parser).parse_args(arg.split()):
      self.tello.send_command('up ' + arg)
  
  def do_down(self, arg):
    'down x: Descend to "x" cm. x=20-500: down 40'
    parser = ArgumentParser(self.do_down, prog='down')
    if add_distance_arg(parser).parse_args(arg.split()):
      self.tello.send_command('down ' + arg)
  
  def do_left(self, arg):
    'left x: Fly left for "x" cm. x=20-500: left 40'
    parser = ArgumentParser(self.do_left, prog='left')
    if add_distance_arg(parser).parse_args(arg.split()):
      self.tello.send_command('left ' + arg)
  
  def do_right(self, arg):
    'right x: Fly right for "x" cm. x=20-500: right 40'
    parser = ArgumentParser(self.do_right, prog='right')
    if add_distance_arg(parser).parse_args(arg.split()):
      self.tello.send_command('right ' + arg)
  
  def do_forward(self, arg):
    'forward x: Fly forward for "x" cm. x=20-500: forward 40'
    parser = ArgumentParser(self.do_forward, prog='forward')
    if add_distance_arg(parser).parse_args(arg.split()):
      self.tello.send_command('forward ' + arg)
  
  def do_back(self, arg):
    'back x: Fly backward for "x" cm. x=20-500: back 40'
    parser = ArgumentParser(self.do_back, prog='back')
    if add_distance_arg(parser).parse_args(arg.split()):
      self.tello.send_command('back ' + arg)
  
  def do_cw(self, arg):
    'cw x: Rotate "x" degrees clockwise. x=1-360: cw 60'
    parser = ArgumentParser(self.do_cw, prog='cw')
    if add_angle_arg(parser).parse_args(arg.split()):
      self.tello.send_command('cw ' + arg)
  
  def do_ccw(self, arg):
    'ccw x: Rotate "x" degrees counterclockwise. x=1-360: ccw 60'
    parser = ArgumentParser(self.do_ccw, prog='ccw')
    if add_angle_arg(parser).parse_args(arg.split()):
      self.tello.send_command('ccw ' + arg)
  
  def do_flip(self, arg):
    'flip x: Flip in "x" direction. x={l,r,f,w} (left, right, forward, backward): flip r'
    parser = ArgumentParser(self.do_flip, prog='flip')
    if add_direction_arg(parser).parse_args(arg.split()):
      self.tello.send_command('flip ' + arg)
  
  def do_go(self, arg):
    'go x y z speed: Fly to "x" "y" "z" at "speed" (cm/s). x=-500-500, y=-500-500, z=-500-500, speed=10-100. Note: x, y and z values can\'t be set between -20-20 simultaneously: go 100 200 300 20'
    parser = ArgumentParser(self.do_go, prog='go')
    add_distance_arg(parser, name='x')
    add_distance_arg(parser, name='y')
    add_distance_arg(parser, name='z')
    add_speed_arg(parser, name='speed')
    if parser.parse_args(arg.split()):
      self.tello.send_command('go ' + arg)

  # TODO Add missing commands
  # stop
  # curve
  # go
  # jump
  # speed
  # rc
  # wifi
  # mon
  # moff
  # mdirection
  # ap
  # speed?
  # battery?
  # time?
  # wifi?
  # sdk?
  # sn?

  # ----- record and playback -----
  def do_record(self, arg):
    'Save future commands to filename:  record commands.cmd'
    self.file = open(arg, 'w')
  
  def do_playback(self, arg):
    'Playback commands from a file:  playback commands.cmd'
    self.close()
    with open(arg) as f:
      self.cmdqueue.extend(f.read().splitlines())

  # ----- exit -----
  def do_exit(self, arg):
    'Exit this program'
    return True

  # ----- overrides -----

  def default(self, line):
    # Pass on unrecognized command
    print('Unrecognized command. Passing on without verifying arguments.', file=sys.stderr)
    self.tello.send_command(line)

  def precmd(self, line):
    line = line.lower()
    # if self.file and 'playback' not in line:
    #   print(line, file=self.file)
    return line

  def close(self):
    if self.file:
      self.file.close()
      self.file = None


if __name__ == '__main__':
  TelloCmd().cmdloop()
