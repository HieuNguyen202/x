#include <Wire.h>
#include <Adafruit_MotorShield.h>
/*
RPI               Arduino Uno		Arduino Mega
--------------------------------------------
GPIO 2 (SDA) <--> Pin A4 (SDA)		Pin 20 (SDA)	Green
GPIO 3 (SCL) <--> Pin A5 (SCL)		Pin 21 (SCL)	Yellow
Ground       <--> Ground			Ground			Black
*/

#define I2CAddress 7
//Adafruit_MotorShield AFMS = Adafruit_MotorShield();
//Adafruit_DCMotor *myMotor = AFMS.getMotor(1);
//int command = 2;
//int speed = 0;
int val = 0;


void setup()
{
	Serial.begin(9600);
	Serial.println("started");
	I2CTestSetup();
	//MotorSetup();
}
void loop()
{
	//Wire.requestFrom(8, 32);
}
void I2CTestSetup()
{
	Wire.begin(I2CAddress);
	Wire.setClock(100000L);
	Wire.onReceive(onI2CReceive);
	Wire.onRequest(onI2CRequest);
}
void I2CTestLoop() {
}

void MotorSetup()
{
	//AFMS.begin();  // create with the default frequency 1.6KHz
	//myMotor->run(FORWARD);
}
void MotorLoop()
{
	//Serial.println(String(command) + " " + String(speed));
	
	//delay(200);
}

void drive()
{
	//switch (command)
	//{
	//case 1:
	//	myMotor->run(FORWARD);
	//	break;
	//case 2:
	//	myMotor->run(BACKWARD);
	//	break;
	//default:
	//	break;
	//}
	//myMotor->setSpeed(speed);
}
void onI2CReceive(int byteCount) {
	int message[2];
	int i = 0;
	while (Wire.available()) {
		message[i] = Wire.read();
		i++;
	}
	//for (int i = 0; i < 32; i++)
	//{
	//	Serial.println(message[i]);
	//}
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

