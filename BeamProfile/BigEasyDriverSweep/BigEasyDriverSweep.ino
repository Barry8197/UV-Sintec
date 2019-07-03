//Declare pin functions on Arduino
#define stp 2
#define dir 3
#define MS1 4
#define MS2 5
#define MS3 6
#define EN  7
#define HOME 8

//Declare variables for functions
char user_input;
int x;
int y;
int state;

int lightSensorPin = A0;
int analogValue = 0;


void setup() {
  pinMode(stp, OUTPUT);
  pinMode(dir, OUTPUT);
  pinMode(MS1, OUTPUT);
  pinMode(MS2, OUTPUT);
  pinMode(MS3, OUTPUT);
  pinMode(EN, OUTPUT);
  pinMode(HOME, INPUT);
  resetBEDPins(); //Set step, direction, microstep and enable pins to default states
  Serial.begin(9600); //Open Serial connection for debugging
 // Serial.println("Begin motor control");
 // Serial.println();
  //Print function list for user selection
 // Serial.println("Platform Rotates Clockwise");
 // Serial.println("Enter number for control option:");
 // Serial.println("1. Sweep 180 degrees");
 // Serial.println("2. Reset Board");
 // Serial.println();
}

void loop() {
  while (Serial.available()) {
          user_input = Serial.read(); //Read user input and trigger appropriate function
          digitalWrite(EN,LOW); //Pull enable pin low to set FETs active and allow motor control
          if(user_input =='1')
          {

            Sweep();

          }
          else if(user_input =='2')
          {
           
            resetArm();

          }
          else if(user_input =='3')
          {
           
            returnHome();

          }
          else
          {
           // Serial.println("Invalid option entered.");
          }
          resetBEDPins();                    
      }

}
//Reset Big Easy Driver pins to default states
void resetBEDPins()
{
  digitalWrite(stp, LOW);
  digitalWrite(dir, LOW);
  digitalWrite(MS1, LOW);
  digitalWrite(MS2, HIGH);
  digitalWrite(MS3, LOW);
  digitalWrite(EN, HIGH);
}

//Default microstep mode function

//Forward/reverse stepping function
void Sweep()
{
    //analogValue = analogRead(lightSensorPin);
    //Serial.println(analogValue);

  for (y = 0; y <400; y++)
  {
    digitalWrite(stp, HIGH); //Trigger one step
    delayMicroseconds(1000);
    analogValue = analogRead(lightSensorPin);
    Serial.println(analogValue);
    //Serial.println(y*0.9);

    delayMicroseconds(500);  
    digitalWrite(stp, LOW); //Pull step pin low so it can be triggered again
    delayMicroseconds(500);
    //Serial.println(y/2*0.9);
  }

 // Serial.println("Enter new option");
 // Serial.println();
}

void resetArm()
{

  digitalWrite(dir, HIGH);
  Sweep();

  //Serial.println("Enter new option");
  //Serial.println();
}

void returnHome()
{

  digitalWrite(dir, HIGH);

  while(digitalRead(HOME)== HIGH){

    digitalWrite(stp, HIGH); //Trigger one step
    delayMicroseconds(1000);

    delayMicroseconds(500);  
    digitalWrite(stp, LOW); //Pull step pin low so it can be triggered again
    delayMicroseconds(500);
    
  }

}
