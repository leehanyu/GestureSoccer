
// ORIGINAL: www.elegoo.com
// modified for RS-IOT class in CMU

//    The direction of the car's movement
//  ENA   ENB   IN1   IN2   IN3   IN4   Description
//  HIGH  HIGH  HIGH  LOW   LOW   HIGH  Car is runing forward
//  HIGH  HIGH  LOW   HIGH  HIGH  LOW   Car is runing back
//  HIGH  HIGH  LOW   HIGH  LOW   HIGH  Car is turning left
//  HIGH  HIGH  HIGH  LOW   HIGH  LOW   Car is turning right
//  HIGH  HIGH  LOW   LOW   LOW   LOW   Car is stoped
//  HIGH  HIGH  HIGH  HIGH  HIGH  HIGH  Car is stoped
//  LOW   LOW   N/A   N/A   N/A   N/A   Car is stoped


//define L298n module IO Pin
#define ENA 5
#define ENB 6
#define IN1 7
#define IN2 8
#define IN3 9
#define IN4 11

// PWM percentage
int p20 =  51; // 0.2 * 255 = 51
int p25 =  64; // 0.25 * 255 = 63.75
int p30 =  76; // 0.3 * 255 = 76.5
int p40 = 102; // 0.4 * 255 = 102
int p50 = 127; // 0.5 * 255 = 127.5
int p70 = 178; // 0.7 * 255 = 178.5
int p90 = 229; // 0.9 * 255 = 229.5
 
int pwm1 = p50;
int pwm2 = p70;
int pwm3 = p90;

void forward() {
  //digitalWrite(ENA, HIGH); //enable L298n A channel
  //digitalWrite(ENB, HIGH); //enable L298n B channel
  analogWrite(ENA,pwm1);
  analogWrite(ENB,pwm1);
  digitalWrite(IN1, HIGH); //set IN1 hight level
  digitalWrite(IN2, LOW); //set IN2 low level
  digitalWrite(IN3, LOW); //set IN3 low level
  digitalWrite(IN4, HIGH); //set IN4 hight level
  Serial.println("Forward");//send message to serial monitor
}


void accelerate() {
  //digitalWrite(ENA, HIGH); //enable L298n A channel
  //digitalWrite(ENB, HIGH); //enable L298n B channel
  analogWrite(ENA,pwm3);
  analogWrite(ENB,pwm3);
  digitalWrite(IN1, HIGH); //set IN1 hight level
  digitalWrite(IN2, LOW); //set IN2 low level
  digitalWrite(IN3, LOW); //set IN3 low level
  digitalWrite(IN4, HIGH); //set IN4 hight level
  Serial.println("Accelerate");//send message to serial monitor
}

void back() {
  //digitalWrite(ENA, HIGH);
  //digitalWrite(ENB, HIGH);
  analogWrite(ENA,pwm1);
  analogWrite(ENB,pwm1);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  Serial.println("Back");
}

void left() {
  //digitalWrite(ENA, HIGH);
  //digitalWrite(ENB, HIGH);
  analogWrite(ENA,pwm2);
  analogWrite(ENB,pwm2);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  Serial.println("Left");
}

void right() {
  //digitalWrite(ENA, HIGH);
  //digitalWrite(ENB, HIGH);
  analogWrite(ENA,pwm2);
  analogWrite(ENB,pwm2);
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  Serial.println("Right");
}

/*define stop function*/
void stop()
{
  digitalWrite(ENA,LOW);
  digitalWrite(ENB,LOW);
  Serial.println("STP");
}

//before execute loop() function,
//setup() function will execute first and only execute once
void setup() {
  Serial.begin(9600);//open serial and set the baudrate
  pinMode(IN1, OUTPUT); //before useing io pin, pin mode must be set first
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);
}

/*put your main code here, to run repeatedly*/
void loop() {
  int buf;
  if (Serial.available()) {
    buf = Serial.read();
    switch (buf) {
    case 'f':
      forward();
      break;
    case 'a':
      accelerate();
      break;
    case 'b':
      back();
      break;
    case 'l':
      left();
      break;
    case 'r':
      right();
      break;
    case 's':
      stop();
    default:
      break;
    }
  }
}

