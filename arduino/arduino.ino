#include <Wire.h>
/*
RPI               Arduino Uno		Arduino Mega
--------------------------------------------
GPIO 2 (SDA) <--> Pin A4 (SDA)		Pin 20 (SDA)	Green
GPIO 3 (SCL) <--> Pin A5 (SCL)		Pin 21 (SCL)	Yellow
Ground       <--> Ground			Ground			Black
*/

#define I2CAddress 7

void setup()
{
	Serial.begin(9600);
	I2CTestSetup();
}
void loop()
{

}

void I2CTestSetup()
{
	Wire.begin(I2CAddress);
	//Wire.setClock(400000L);
	Wire.onReceive(onI2CReceive);
	Wire.onRequest(onI2CRequest);
}

void onI2CReceive(int byteCount) {
	int message[20];
	int i = 0;
	while (Wire.available()) {
		message[i] = Wire.read();
		i++;
	}
	for (int i = 0; i < 20; i++)
	{
		Serial.print(message[i]);
	}
	Serial.println("");
}

void onI2CRequest() {//fix this
	int val = 0;
	for (int i = 0; i < 32; i++)
	{
		Wire.write(val);
		val++;
	}
	val++;
	if (val > 127)
	{
		val = 0;
	}
	Serial.println("request");
}
