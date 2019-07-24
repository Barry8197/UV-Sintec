// Niamh Hourihan - 115374376
// 12 July 2019
// Quantum Electronics Lab - Alan Morrison
// UV-Syntec Project

//Declare pin functions on Arduino
// Motor 1 = x-axis & Motor 2 = y-axis
#define dir_2 2   // direction of motor 2
#define stp_2 3   // step of motor 2
#define MS3_2 4
#define MS2 5
#define MS1 6
#define SW_1 7    // switch of motor 1
#define SW_2 8    // switch of motor 2
#define EN_2 9    // enable pin of motor 2
#define dir_1 10  // direction of motor 1
#define stp_1 11  // step of motor 1
#define MS3_1 12
#define EN_1 13   // enable pin of motor 1
#define S1 19     // resolution switch 1
#define S2 18     // resolution switch 2

// MS1 & MS2 of both motors share connections & MS3 is separate for both motors. This is
// because whether 1/8th step or 1/16th step is implemented, both MS1 & MS2 will be HIGH.
// Default is 1/8th step.

//Declare variables for functions
char user_input;                        // user input to serial monitor
int x; int y; int n; int i;
int state1;                             // to store on or off value of switch from motor 1 (x-direction)
int state2;                             // to store on or off value of switch from motor 2 (y-direction)

// Big Easy Driver variables
int steps_per_mm = 13.3;                // how many steps per millimetre - for 1/8th microstep mode
int axisdist = 28;
int x_cm = 0;                           // distance travelled in centimetres each time a measurement is taken in x-direction
int xsteps = x_cm*10*steps_per_mm;      // Calculates number of steps needed for x_cm
int y_cm = 0;                           // number of steps travelled in y-direction during "snake" pattern - this can be changed
int ysteps = y_cm*10*steps_per_mm;      // Calculates number of steps needed for y_cm
int totsteps = axisdist*10*steps_per_mm;

// Switch variables
int s1state;                            // Resolution switch 1
int s2state;                            // Resolution switch 2

// Button variables
const int buttonPin1 = 17;              // the number of the pushbutton pin 1
const int ledPin1 = 16;                 // the number of the LED pin 1
int buttonState1 = 0;                   // current state of the button 1
int buttonPress1 = 0;
const int buttonPin2 = 15;              // the number of the pushbutton pin 2
const int ledPin2 = 14;                 // the number of the LED pin 2
int buttonState2 = 0;                   // current state of the button 2
int buttonPress2 = 0;

void setup() {
  //pins for Big Easy Driver
  pinMode(stp_1, OUTPUT);
  pinMode(dir_1, OUTPUT);
  pinMode(MS1, OUTPUT);
  pinMode(MS2, OUTPUT);
  pinMode(MS3_1, OUTPUT);
  pinMode(EN_1, OUTPUT);
  pinMode(SW_1, OUTPUT);
  pinMode(dir_2, OUTPUT);
  pinMode(stp_2, OUTPUT);
  pinMode(SW_2, OUTPUT);
  pinMode(MS3_2, OUTPUT);
  pinMode(EN_2, OUTPUT);
  
  // pins for switches are inputs
  pinMode(S1, INPUT);
  pinMode(S2, INPUT);
  
  // pins for buttons & LEDs
  pinMode(buttonPin1, INPUT);
  pinMode(ledPin1, OUTPUT);
  pinMode(buttonPin2, INPUT);
  pinMode(ledPin2, OUTPUT);
  
  resetBEDPins();                       // Set step, direction, microstep and enable pins to default states
  Serial.begin(9600);                   // Open Serial connection for debugging
  Serial.println("Begin motor control");
  //Print function list for user selection
  Serial.println("Enter number for control option:");
  Serial.println("1. Return motor to HOME position.");
  Serial.println("2. Collect data points.");
}

//Main loop
void loop() {
  Button1();                            // Button function to start collecting data points
  Button2();                            // Button function to return motor to HOME position
  ChooseResolution();                   // Switch function to select resolution
  Stepping(x);                          // Function instructs motor to take a step
  SerialMonitor();                      // Serial monitor interface
  
  digitalWrite(EN_1, LOW);              // Pull enable pin low to set FETs active and allow motor control
  digitalWrite(EN_2, LOW);
}

//Reset Big Easy Driver pins to default states
void resetBEDPins()
{
  digitalWrite(stp_1, LOW);
  digitalWrite(dir_1, LOW);
  digitalWrite(MS1, LOW);
  digitalWrite(MS2, LOW);
  digitalWrite(MS3_1, LOW);
  digitalWrite(EN_1, HIGH);
  digitalWrite(dir_2, LOW);
  digitalWrite(stp_2, LOW);
  digitalWrite(MS3_2, LOW);
  digitalWrite(EN_2, HIGH);
}

//Returns both motors to HOME position (0,0) before calculating data points
void HOME()
{
  state1 = digitalRead(SW_1);
  digitalWrite(dir_1, LOW);             // Pull direction pin low to move left
  digitalWrite(MS1, HIGH);              // Pull MS1,MS2 high and MS3 high to set logic to 1/16th microstep resolution. Or
  digitalWrite(MS2, HIGH);              // Pull MS1 and MS2 high, and MS3 low to set logic to 1/8th microstep resolution.
  digitalWrite(MS3_1, LOW);
  state2 = digitalRead(SW_2);
  digitalWrite(dir_2, LOW);             // Pull direction pin low to move backwards
  digitalWrite(MS3_2, LOW);
  
  while(state1 == 0)
    {
      Stepping(stp_1);                  // Step of Motor 1 takes one step forward
      state1 = digitalRead(SW_1);       // Continuously reads the state of the switch
    }
    digitalWrite(EN_1, HIGH);           //Outside of the 'while' loop when state==1, motion stops.
    
    while(state2 == 0)
    {
      Stepping(stp_2);                  // Step of Motor 2 takes one step forward
      state2 = digitalRead(SW_2);
    }
    digitalWrite(EN_2, HIGH);
}

// Function for Motor 1 moving right
void DataPointsx_right()
{
  digitalWrite(EN_1, LOW);
  digitalWrite(dir_1, HIGH);            // Pull direction pin high to move right
  
  digitalWrite(MS1, HIGH);
  digitalWrite(MS2, HIGH);
  digitalWrite(MS3_1, LOW);
  
  for(x = 0; x<(totsteps/xsteps); x++)
  {
    for(n = 0; n<xsteps; n++)
    {
      Stepping(stp_1);
    }
    delay(500);
  }

 delay(200); 
}

// Function for Motor 1 moving left
void DataPointsx_left()
{
  digitalWrite(EN_1, LOW); 
  digitalWrite(dir_1, LOW);             // Pull direction pin high to move right
  
  digitalWrite(MS1, HIGH);
  digitalWrite(MS2, HIGH);
  digitalWrite(MS3_1, LOW);
  
  for(x = 0; x<(totsteps/xsteps); x++)
  {
    for(n = 0; n<xsteps; n++)
    {
      Stepping(stp_1);
    }
    delay(500);
  }

 delay(200); 
}

// Function for Motor 2
void DataPointsy()
{
  digitalWrite(EN_2, LOW);
  digitalWrite(dir_2, HIGH);            // Pull direction pin high to move forward
  
  digitalWrite(MS1, HIGH);
  digitalWrite(MS2, HIGH);
  digitalWrite(MS3_2, LOW);
  
  for(n = 0; n<ysteps; n++)
  {
    Stepping(stp_2);
  }
  
 delay(200); 
}

// Function to select resolution using a switch: high, medium or low
int ChooseResolution()
{
  s1state = digitalRead(S1);
  s2state = digitalRead(S2);
  
  if((s1state==0) && (s2state==0))      // High resolution
  {
    x_cm = 1;
    y_cm = 1;
    xsteps = x_cm*10*steps_per_mm;
    ysteps = y_cm*10*steps_per_mm;
  }
  else if((s1state==0) && (s2state==1)) // Medium resolution
  {
    x_cm = 4;
    y_cm = 4;
    xsteps = x_cm*10*steps_per_mm;
    ysteps = y_cm*10*steps_per_mm;
  }
  else if((s1state==1) && (s2state==0)) // Low resolution
  {
    x_cm = 7;
    y_cm = 7;
    xsteps = x_cm*10*steps_per_mm;
    ysteps = y_cm*10*steps_per_mm;
  }
}

// Function to allow button 1 to start motor collecting data points
int Button1()
{
  ChooseResolution();
  digitalWrite(EN_1, LOW);              // Pull enable pin low to set FETs active and allow motor control
  digitalWrite(EN_2, LOW);
  // read the state of the pushbutton value:
  buttonPress1 = digitalRead(buttonPin1);
  if(buttonPress1 == HIGH)
  {
    buttonState1 = HIGH;
  }

  // check if the pushbutton is pressed.
  if(buttonState1 == HIGH)
  {
    digitalWrite(ledPin1, HIGH);
    for(i=0; i<(totsteps/(2*ysteps)); i++)
    {
      DataPointsx_right();
      DataPointsy();
      DataPointsx_left();
      DataPointsy();
    }
    DataPointsx_right();
    HOME();
  }
  else
  {
    digitalWrite(ledPin1, LOW);
    
  }
}

// Function to allow button to return motor to HOME position
int Button2()
{
  ChooseResolution();
  
  digitalWrite(EN_1, LOW);
  digitalWrite(EN_2, LOW);
  // read the state of the pushbutton value:
  buttonPress2 = digitalRead(buttonPin2);
  if(buttonPress2 == HIGH)
  {
    buttonState2 = HIGH;
  }

  // check if the pushbutton is pressed.
  if(buttonState2 == HIGH)
  {
    digitalWrite(ledPin2, HIGH);
    HOME();
  }
  else
  {
    digitalWrite(ledPin2, LOW);
    
  }
}

int Stepping(int x)
{
  digitalWrite(x,HIGH);                 // Trigger one step forward
  delay(1);
  digitalWrite(x,LOW);                  // Pull step pin low so it can be triggered again
  delay(1);
}

// Funcion to allow user input in serial monitor for motor control
int SerialMonitor()
{
  while(Serial.available())
  {
    user_input = Serial.read();         // Read user input and trigger appropriate function
    if(user_input =='1')
    {
      HOME();
    }
    else if(user_input == '2')
    {
      for(i=0; i<(totsteps/(2*ysteps)); i++)
      {
        DataPointsx_right();
        DataPointsy();
        DataPointsx_left();
        DataPointsy();
      }
      DataPointsx_right();
      HOME();
    }
  }
}
