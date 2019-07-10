//Declare pin functions on Arduino
#define stp 11
#define dir 12
#define MS1 A1
#define MS2 A2
#define MS3 A3
#define EN  13
#define HOME A4

//Declare variables for functions
char user_input;
int x;
int y;
int state;

int digit[10] = {0b0111111, 0b0000110, 0b1011011, 0b1001111, 0b1100110, 0b1101101, 0b1111101, 0b0000111, 0b11111111, 0b1101111};  
int sensorValue0 = 0;  
int digit1, digit2;  

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
 { Serial.begin(9600); 
  for (int i = 2; i < 10; i++)   
  {  
    pinMode(i, OUTPUT);  
  }  
  pinMode(12, OUTPUT);  
  pinMode(13, OUTPUT);  
} 

 
}

void loop() {
  int sensorValue0 = analogRead(A5);

  float voltage = (sensorValue0) * (5.0 / 1023.0);
float diffvoltage =voltage/10;

//float voltage = (101003/1001650) *(sensorValue0) * (5.0 / 1023.0);

//multiply by ratio to account for the gain//

int resistanceOUT = 5.3;

int current = 1000*diffvoltage/resistanceOUT;
Serial.println(current);
    digit2 = current / 10;  
    //digit2 is for the tens place and will be an integer//
    digit1 = current - digit2*10 ; 
    //digit1 is for the ones place and will be an integer//


 
      digitalWrite(12, HIGH);  
      digitalWrite(13, LOW);  
      dis(digit2);  
     
   delay(10); 
   
      digitalWrite(13, HIGH);  
      digitalWrite(12, LOW);  
      dis(digit1);
        
   delay(10); 

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

void dis(int num)   
{  
  for (int i = 2; i < 9; i++)   
  {  
    digitalWrite(i, bitRead(digit[num], i - 2));  
  }  
} 
