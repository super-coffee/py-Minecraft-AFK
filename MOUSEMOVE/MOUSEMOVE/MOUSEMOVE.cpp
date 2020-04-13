﻿#include <iostream>
#include <windows.h>
#include <math.h>

#define PI 3.141

INPUT pos1;
INPUT pos2;

int main(int argc, char **argv)
{
	//int distance = atoi(argv[1]);double degree = atof(argv[2]);
	//int timeUsage = atoi(argv[3]);int step = atoi(argv[4]);
	int distance = 1000;float degree = 90;
	int timeUsage = 5;int step = 4;
	int deltaX = step*sin(degree*(PI/180)) + 0.5;
	int deltaY = step*cos(degree*(PI/180)) + 0.5;
	int repeatTimes = ((distance * 2) / step) % 2 ? ((distance * 2) / step) + 1: (distance * 2) / step;
	int TER = ((timeUsage * 1000 )/repeatTimes);
	pos1.type = pos2.type = INPUT_MOUSE;
	pos1.mi.dx = deltaX;pos1.mi.dy = deltaY;
	pos2.mi.dx = -deltaX;pos2.mi.dy = -deltaY;
	int count = repeatTimes;bool direction = true;
	while (count)
	{
		if (direction)
		{
			SendInput(1, &pos1, sizeof(pos1));
			count -= 1;
			if (count == (int)(repeatTimes / 4) * 3)
			{
				direction = false;
			}
			Sleep(TER);
		}
		else
		{
			SendInput(1, &pos2, sizeof(pos2));
			count -= 1;
			if (count == (int)(repeatTimes / 4))
			{
				direction = true;
			}
			Sleep(TER);
		}
	}
	//std::cout << distance << std::endl;
	//std::cout << degree << std::endl;
	//std::cout << timeUsage << std::endl;
	//std::cout << step << std::endl;
	//std::cout << argc << std::endl;
	//Sleep(5000);
	return 0;
}