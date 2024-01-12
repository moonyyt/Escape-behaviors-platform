# Escape-behaviours-platform
@[toc]
## Introduction

` Technical summary：Spyder python C# STM32 Keil`


The python program has a file composition: 
* escape behaviour.py.
Its main components include the following:
Firstly, we acquire the real-time video stream from the webcam, identify and save the kinematic parameters of the robot predator and the mouse, including the coordinate position, the relative distance, and the moving speed of the mouse.
Then according to the relative positions of the robot predator and the mouse, the required speed and direction information of the slide is transmitted to the servomotor drive system, so that the robot predator will start the chase towards the mouse at a constant speed.

The hardware driver compiled by C has six main files (They should be downloaded together): 
* CORE
* HARDWARE
* OBJ
* STM32F10x_FWLib
* SYSTEM
* USER
The main functions of the programme in the STM32 are as follows:
Firstly receive and decode the direction and speed signals (digital signals) from the python program
Secondly, convert the direction signals to high and low level signals (0 or 1) and output them via IO ports PE1 and PE6.
Third, convert the speed signals into pulse signals of corresponding frequencies and output them through the PA7 and PD12 ports. The servo motor makes 1 revolution (about 7.5cm) for every 16,000 pulses it receives
## Installation Environment

* escape behaviour.py.
The programme can be run in any software that can compile a python environment, here we recommend using Spyder from Anaconda. Spyder is a powerful Python IDE (Integrated Development Environment) that combines writing, running and debugging Python programs.
 It can be downloaded from: [Anaconda](https://www.anaconda.com/)
 It is worth noting that when using the programme, you can install the appropriate extension packages using the following statement:
 

```
// opencv
pip install opencv-python
```
```
// numpy
pip install numpy
```
```
// serial
pip install serial
```
* STM32 (C#)
The programme needs to be compiled on Keil5, which you can download via [Keil](https://www.keil.com/download/).
After successful compilation, we need to burn the compiled file (CONTROL.hex file in the OBJ folder into the STM32 microcontroller via the serial port). Serial debugging software and information can be downloaded through [XCOM](http://47.111.11.73/docs/index.html).

## Document Description
* escape behaviour.py.
The programme can be downloaded and compiled and run directly in Spyder.

* STM32 (C#)
Key Code:
Main function: main.c
Serial Communication: HARDWARE-serial.c
pid control: HARDWARE-pid.c
pwm wave: HARDWARE-timer.c

## Other description


> **Data organisation**
>Experiment data and code.rar

> **Experimental video**
>Movies 1-10.rar
>Movies 11-20.rar
