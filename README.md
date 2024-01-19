# Escape-behaviors-platform
## Background

` Technical summary：Spyder python C# STM32 Keil`

### Overview
 **A real-time interactive platform** to study the escape behavior of rodents when a terrestrial threat is approaching. The software includes the main program written in Python and the hardware control written in C. The hardware consists of three parts: the arena, the control unit for the two-dimensional slides, and the webcam for data acquisition. 
 
Here, we will describe how to install and use the software and hardware modules of the platform.

### Overview of the workflow
The following figures illustrate the workflow of a real-time interactive platform.

[![hardware-fiigure1.png](https://img-blog.csdnimg.cn/img_convert/891ccf37bad712c4b0c62bbc9195a5e9.png#pic_center)](https://postimg.cc/p9bwy5Rw)

[![hardware-figure2.png](https://img-blog.csdnimg.cn/img_convert/813a456049219aea223f6ab8a6872db8.png#pic_center)](https://postimg.cc/JySGsqG1)

The following figure shows the flowchart of software design for real-time closed-loop control.

[![software-fiigure.png](https://img-blog.csdnimg.cn/img_convert/354dabab249dd7634292a7639c49c9fe.png#pic_center)](https://postimg.cc/wysFN02F)

The python program has a file composition: 
* escape behavior.py.

The hardware driver compiled by C has seven main files (They should be downloaded together): 
* CORE
* HARDWARE
* OBJ
* STM32F10x_FWLib
* SYSTEM
* USER

## Installation
### Step 1: Install Python via Anaconda
The program can be run in any software that can compile a python environment, here we recommend using Spyder from Anaconda. Spyder (Python ≥ 3.7) is a powerful Python IDE (Integrated Development Environment) that combines writing, running and debugging Python programs.
 It can be downloaded from: [Anaconda](https://www.anaconda.com/).
 It is worth noting that when using the program, you can install the appropriate extension packages using the following statement:
 

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
### Step 2: Install Keil
The program needs to be compiled on Keil5, which you can download via [Keil](https://www.keil.com/download/).
### Step 3: Write the program to STM32 via XCOM
After successful compilation, we need to burn the compiled file (CONTROL.hex file in the OBJ folder into the STM32 microcontroller via the serial port). Serial debugging software and information can be downloaded through [XCOM](http://47.111.11.73/docs/index.html).

## User Guides
You can download the python program and run directly in Spyder.
>escape behaviour.py.

If you want to get the C program, you can open CONTROL.uvprojx in the USER folder from Keil.
> **USER**
>CONTROL.uvprojx

> **Other codes descriptions**
>Main function: USER\main.c
Serial communication: HARDWARE\serial\serial.c
Pid control: HARDWARE\PID\pid.c
PWM wave: HARDWARE\TIMER\timer.c

## Hardware
If you want to control the servo motor driver from STM32, you can refer to the following circuit design.

[
![Signal-adaptation-circuit.png](https://img-blog.csdnimg.cn/img_convert/f6e2abef3446966e3b690b10ffc5fa81.png#pic_center)](https://postimg.cc/GBC6RM0W)

Ports PE6 and PE7 in the STM32 give direction and velocity signal, respectively, which are passed through an amplifier circuit to ports 43 and 39 of the servo motor driver.

## Other files
>Raw Experiment Movies
