Title: Pixhawk连接摇杆进行仿真
Date: 2017-12-02
Category: 学习总结
Tags: Pixhawk, Joystick, Simulation, 摇杆， 仿真
Slug: pixhawk_joystick
Summary: 对Pixhawk代码中的仿真接口模块进行了更改，使其能够直接通过USB接口读取控制摇杆的输入，实现对其飞控代码的仿真飞行控制

<h3 id="1">1. 问题</h3>
最近有这样一个需求: 对Pixhawk软件中的控制算法进行更改后，需要对其控制算法、各模式间的切换等进行全面地仿真测试，避免实际飞行时炸机的损失。
按照[官方文档中的方法](https://dev.px4.io/en/simulation/)， 可利用Gazebo, QGroundControl等配合完成大部分的大部分的测试，还可连接控制摇杆/手柄(Joystick/Gamepad), 将其作为手动输入。同事付老师帮忙给了一个Made in China的Saitek Cyborg evo摇杆，按照官网方法进行配置，发现在仿真中无法通过其设置手动、增稳、自动等飞行模式，一查，原来仅有[高端的Sony的摇杆才能支持模式切换](https://docs.qgroundcontrol.com/en/SetupView/Joystick.html#sony-playstation-34-controllers)。 只好想办法省钱，通过更改软件解决无法通过摇杆切换模式的问题。

<center><img src="/images/px4_joystick/Joystick.jpg"　height="400"/></center> 

<h3 id="2">2. 问题分析</h3>
PX4原有的仿真环境交联关系如下图：
<center><img src="/images/px4_joystick/SITL1.png"　height="448"/></center> 
从图中可以看出摇杆的输入通过QGroundControl地面站读取后，转发给控制软件。若能通过控制软件直接读取摇杆输入，如下图：
<center><img src="/images/px4_joystick/SITL2.png" height="448"/></center> 

在控制软件中读取摇杆输入后，对其解析，将按键消息打包为软件能识别的模式切换指令消息，并按照PX4软件中的消息发布订阅机制将其发送至负责模式切换的模块，即能解决前述问题。因此须分以下两步达到目标:

  1. 读取摇杆输入，正确解析其消息；
  2. 将摇杆消息打包为软件可识别的Topic, 将其发布；

事后想了一下官网中通过QGroundControl转发摇杆数据，而非通过控制软件直接读取的原因可能如下:

1. 方便对不同摇杆进行校准操作. 因最终软件需要的控制量数据均需要进行归一化处理, 可通过QGroundControl对不同类型摇杆进行统一校准操作；
2. 可保持软件的通用性，在SITL, HITL, 或实际飞行时均可通过Joystick控制飞行。



<h3 id="3">3. 解决方案</h3>
<h4 id="3.1">3.1. 读取摇杆输入</h4>
首选需要弄清如何读取摇杆输入. 以谷歌找到的一个[linux官方文档](https://www.kernel.org/doc/Documentation/input/joystick-api.txt)及[代码工程](https://github.com/drewnoakes/joystick)为参考，写了如下一个简单测试程序读取摇杆输入，测试环境为Ubuntu 16.04LTS.

```c++
#include <iostream>
#include <sys/stat.h>
#include <unistd.h>
#include <stdio.h>
#include <sys/types.h>
#include <sys/fcntl.h>
#include <time.h>

using namespace std;

#define JS_EVENT_BUTTON 0x01 // button pressed/released
#define JS_EVENT_AXIS   0x02 // joystick moved
#define JS_EVENT_INIT   0x80 // initial state of device

typedef struct{
	unsigned int  time;     /* event timestamp in milliseconds */
	short         value;    /* value: for buttons: 1/0 = down/up; axes: -32767~32767*/
	unsigned char type;     /* event type */
	unsigned char number;   /* axis/button number */
}JS_EVENT;

int main() {
	//open the joystick device, the name might be different
	int fd = open("/dev/input/js0", O_RDONLY); 

	if(fd<0) {
		printf("can not open joystick!\n");
		return 1;
	}

	struct stat sbuf;

	stat("/dev/input/js0", &sbuf);
	printf("/etc/hosts file size = %ld\n", sbuf.st_rdev);

	JS_EVENT event = {0};

	int bytes = 0;

	while (true) {
		// Restrict rate
		usleep(1000);

		// Attempt to sample an event from the joystick
		bytes = read(fd, &event, sizeof(JS_EVENT));

		if (bytes == sizeof(JS_EVENT)) {
			if (event.type & JS_EVENT_BUTTON) {
				printf("Button %u  is %s\n", event.number, event.value == 0 ? "up" : "down");
			}

			if (event.type & JS_EVENT_AXIS) {
				printf("Axis %u is at position %d\n", event.number, event.value);
			}
		}
	}
	return 0;
}
```
使用如下命令编译
```bash
g++ -g -o readJoy main.cpp
```
通过USB连接Saitek Cyborg evo摇杆, 执行程序,得到如下结果:
<center><img src="/images/px4_joystick/readJoyStick.png"/></center>  

代码中通过JS_EVENT结构体读取数据，该数据结构中的type表示了摇杆事件类型(轴移动或按键)， 而number和value则分别表示了哪一个轴/按键的事件值。
拟通过摇杆的各轴作为roll, pitch, yaw, throttle控制，以按键控制模式切换。为了进行下一步工作，须测试得出各轴的极限位置下软件采到的事件值: 

Axis   |  Meaning  |       Value      |  Direction 
-------|-----------|------------------|------------
axis0  |  Roll     |     -32767~32767 |	left~right
axis1  |  Pitch    |     32767~-32767 |	backward~forward
axis2  |  Throttle |     32767~-32767 | min~max
axis3  |  Yaw      |     -32767~32767 | left~right

<h4 id="3.2">3.2. 修改Pixhawk源码</h4>
读取解析到摇杆的动作事件数据仅是第一步，为将其集成至Pixhawk中的软件模块，还需注意以下问题:

1. 上述示例代码中的read()函数为阻塞调用，若直接将其放入某个线程中，没有事件发生时，会导致该线程阻塞而无法执行其他语句，须使用linux提供的poll()接口，仅当查询到有事件发生才调用read()读设备文件上的消息;
2. 须按照Pixhawk的消息订阅/发布(publish/subscribe)机制将摇杆消息打包成软件可识别的消息，在此我们将其打包为**manual_control_setpoint**消息。因为事实上软件中sensors模块中rc_update.cpp将原始的遥控器消息也解析为**manual_control_setpoint**消息，并将其发布。位置控制模块订阅该消息，获取其中的各轴控制量信息。特别需要注意的是Commander模块也订阅该消息，在Commander.cpp中的set_main_state_rc()函数中，根据该消息中的模式设置变量设置飞机的模式。需要根据该函数逆推出发生各模式按键事件后，应该给manual_control_setpoint消息中所需填充的正确值，以期得到目标模式。
3. 按照上述思路更改代码后，发现按压摇杆上对应按键后，有时无法切换模式的问题。排查发现发布消息的频率过快(6ms)，很可能导致消息队列满，使Commander模块无法接收到新消息，从而无法切换模式的问题。将发布消息的周期改为50ms, 该问题再无复现。

最终通过摇杆上的按键0,1,2分别控制手动、增稳、自动三种模式，以其四个轴(axis)控制滚转、俯仰、偏航及油门。在PX4/Firmware的v1.6.5稳定版代码基础上，对[simulator_mavlink.cpp](https://github.com/oneWayOut/Firmware/blob/cai_readJS/src/modules/simulator/simulator_mavlink.cpp)文件更改，插入部分代码，均在**#ifdef ENABLE_JOYSTICK ... #endif** 预处理块内，详见https://github.com/oneWayOut/Firmware上的[cai_readJS](https://github.com/oneWayOut/Firmware/tree/cai_readJS)分支。


在代码目录的终端中输入以下命令，可对其进行测试:
```bash
make posix gazebo_plane
```

连接QGroundControl后，即可模拟飞行操作。





