# Tello EDU Drone Python Playground
Simple python CLI wrapper for the drones UDP API.
This allows you to control the drone via the command line and see the responses.

Added value:
- Basic parameter checks before sending to drone (are required arguments present and of correct type). Does not enforce int value ranges.
- List and explain the available commands.

## Getting started
Connect to the drone's WIFI network.

1. `$ python3 src/tello_cmd.py`
2. `(tello) takeoff`
3. `(tello) land`
4. `(tello) exit

## Supported commands
View via `(tello) help`.

- command
- takeoff
- land
- streamon
- streamoff
- emergency
- up
- down
- left
- right
- forward
- back
- cw
- ccw
- flip
- go
- record (meta command, not passed to drone)
- playback (meta command, not passed to drone)
- exit (meta command, not passed to drone)

## Unsupported commands
Any unrecognized command is passed to the drone as-is. However, the arguments are not checked for existence and type.

- stop
- curve
- go
- jump
- speed
- rc
- wifi
- mon
- moff
- mdirection
- ap
- speed?
- battery?
- time?
- wifi?
- sdk?
- sn?

## Using Docker
1. `docker build -t tello .`
1. `docker run --network=host -it tello`

## Further Reading
- [Ryze example](https://github.com/dji-sdk/Tello-Python/tree/master/Tello_Video)
- [Tensorflow example](https://github.com/markwinap/TensorFlow-Tello-Object_Detection-)
