#include <Sabertooth.h>
#include <Wire.h>
/*
RPI               Arduino Uno		Arduino Mega
--------------------------------------------
GPIO 2 (SDA) <--> Pin A4 (SDA)		Pin 20 (SDA)	Green
GPIO 3 (SCL) <--> Pin A5 (SCL)		Pin 21 (SCL)	Yellow
Ground       <--> Ground			Ground			Black
*/

Sabertooth ST(128);
#define I2CAddress 7

int val = -127;
long count = 0;

void setup()
{
	Serial.begin(9600);
	SabertoothTXPinSerial.begin(9600);
	ST.autobaud();
	ST.motor(1, 0);
	I2CTestSetup();
	pinMode(8, INPUT_PULLUP);
	pinMode(9, INPUT_PULLUP);
	//attachInterrupt(digitalPinToInterrupt(8), print, CHANGE);
	//attachInterrupt(digitalPinToInterrupt(9), print, CHANGE);
}
void loop()
{

}

void I2CTestSetup()
{
	Wire.begin(I2CAddress);
	Wire.setClock(400000L);
	Wire.onReceive(onI2CReceive);
	Wire.onRequest(onI2CRequest);
}

void onI2CReceive(int byteCount) {
	int message[3];
	int i = 0;
	while (Wire.available()) {
		message[i] = Wire.read();
		i++;
	}
	
	int command = message[0];
	switch (command)
	{
	case 1:
		ST.motor(message[1], (signed char)message[2]); //motorID = message[1]; motorPower = message[2]
		break;
	default:
		break;
	}
}

void onI2CRequest() {//fix this
	for (int i = 0; i < 32; i++)
	{
		Wire.write(val);
	}
	val++;
	if (val > 127)
	{
		val = 0;
	}
}

void print()
{
	//Serial.println(count);
	//count++;
}

