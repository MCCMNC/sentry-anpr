/*
 *  ARDUINO ANPR PHYSICAL INTERFACE
 *  PROD BY MCCMNC
 */

#include <Servo.h>

#define LIGHT 10
#define SERVO 9

bool green_light = false; //when false - red, true - green

Servo servo;
int servo_pos = 0;

void accessBarrier(bool set){
  if(set){
    Serial.println("Opening barrier");
    servo.write(90);
  }else{
    Serial.println("Closing barrier");
    servo.write(0);
  }
}

void light(bool lightmode){
  if(lightmode){
    digitalWrite(LIGHT, 0);
    Serial.println("Green light on.");
  }else{
    digitalWrite(LIGHT, 1);
    Serial.println("Red light on.");
  }
}

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(LIGHT, OUTPUT);
  digitalWrite(LIGHT, 1);

  servo.attach(SERVO);
  Serial.begin(9600);
  servo.write(0);
}

void loop() {
  if(Serial.available() > 0){
    String request = Serial.readString();
    request.trim();

    if (request.equals("BARRIER OPEN")) {
          accessBarrier(true);
        } else if (request.equals("BARRIER CLOSE")) {
          accessBarrier(false);
        } else if (request.equals("LIGHT GREEN")) {
          light(true);
        } else if (request.equals("LIGHT RED")) {
          light(false);
        } else if (request.equals("SIGOPEN")){
          accessBarrier(true);
          delay(2000);
          light(true);
        } else if (request.equals("SIGCLOSE")){
          light(false);
          delay(2000);
          accessBarrier(false);
        } else {
          Serial.println("Incorrect command.");
        }
  }
}
