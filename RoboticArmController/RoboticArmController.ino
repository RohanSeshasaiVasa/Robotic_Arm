#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

#define SERVO_MIN 100
#define SERVO_MAX 525

const int recordButton = 2;`
const int playButton = 3;

bool lastRecordState = HIGH;
bool lastPlayState = HIGH;

int angleToPulse(int angle) {
  return map(angle, 0, 180, SERVO_MIN, SERVO_MAX);
}

void moveServo(int servo, int angle) {
  pwm.setPWM(servo - 1, 0, angleToPulse(angle));
}

void setup() {
  Serial.begin(9600);

  pinMode(recordButton, INPUT_PULLUP);
  pinMode(playButton, INPUT_PULLUP);

  pwm.begin();
  pwm.setPWMFreq(50);
}

void loop() {
  bool recordState = digitalRead(recordButton);
  bool playState = digitalRead(playButton);

  if (recordState == LOW && lastRecordState == HIGH) {
    Serial.println("RECORD");
    delay(300);
  }

  if (playState == LOW && lastPlayState == HIGH) {
    Serial.println("PLAY");
    delay(300);
  }

  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');

    if (cmd.startsWith("S")) {
      int colon = cmd.indexOf(':');

      if (colon > 0) {
        int servo = cmd.substring(1, colon).toInt();
        int angle = cmd.substring(colon + 1).toInt();

        if (servo >= 1 && servo <= 4 && angle >= 0 && angle <= 180) {
          moveServo(servo, angle);
        }
      }
    }
  }

  lastRecordState = recordState;
  lastPlayState = playState;
}