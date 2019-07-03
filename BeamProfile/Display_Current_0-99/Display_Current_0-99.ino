int digit[10] = {0b0111111, 0b0000110, 0b1011011, 0b1001111, 0b1100110, 0b1101101, 0b1111101, 0b0000111, 0b11111111, 0b1101111};  
int sensorValue0 = 0;  
int digit1, digit2;  

//will display currents from 10-99//
  
void setup()   
{ Serial.begin(9600); 
  for (int i = 2; i < 9; i++)   
  {  
    pinMode(i, OUTPUT);  
  }  
  pinMode(12, OUTPUT);  
  pinMode(13, OUTPUT);  
} 


void loop() {

int sensorValue0 = analogRead(A5);



/*R1= 101 004
 * R2= 101 003
 * R3= 1 101 500
 * R4= 1 101 800
 * assume 1~2 and 3~4
 * ratio 1:3 around 101003/1001650
 */
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

         
  }  


void dis(int num)   
{  
  for (int i = 2; i < 9; i++)   
  {  
    digitalWrite(i, bitRead(digit[num], i - 2));  
  }  
} 
