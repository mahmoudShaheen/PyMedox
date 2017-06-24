////////////////////////////////////////////////////////////
//               @author: Mahmoud Shaheen                 //
//                MedicalBox IOT Project                  //
//               Arduino-Serial-Raspberry                 //
////////////////////////////////////////////////////////////

//Arduino Pins definition
//Up-Down stepper
#define    upPin1       2
#define    upPin2       3
#define    upPin3       4
#define    upPin4       5
//Rotation stepper
#define    roPin1       6
#define    roPin2       7
#define    roPin3       8
#define    roPin4       9
//other outputs
#define    drawer         10
#define    warehouse      11
#define    pump          12
//sensors
#define    infrared        13
#define    current         A0
#define    temperature     A1
#define    lightLevel      A2

#define    doorDelay        1000
#define    warehouseDelay   1000
#define    roMotorDelay   10
#define    upMotorDelay   3
#define    i72   10
#define    j72   8
#define    iup   50
#define    jup   8


//variables definition
char  serialData; //for storing serial string
float tempFloat = 0; //for saving sensor data temporary
int billCount = 0; //for storing bill count added by ISR

int i,j;

/// using half step mode 
int seq[8][4]={1,0,0,0,
               1,1,0,0,
               0,1,0,0,
               0,1,1,0,
               0,0,1,0,
               0,0,1,1,
               0,0,0,1,
               1,0,0,1 };

void setup() {
  //Setting input/output Pins
  //outputs
  pinMode(  upPin1,  OUTPUT);
  pinMode(  upPin2,  OUTPUT);
  pinMode(  upPin3,  OUTPUT);
  pinMode(  upPin4,  OUTPUT);
  pinMode(  roPin1,  OUTPUT);
  pinMode(  roPin2,  OUTPUT);
  pinMode(  roPin3,  OUTPUT);
  pinMode(  roPin4,  OUTPUT);
  pinMode(  drawer,     OUTPUT);
  pinMode(  warehouse,  OUTPUT);
  pinMode(  relay,      OUTPUT);
  //inputs
  pinMode(  infrared,    INPUT);
  pinMode(  current,     INPUT);
  pinMode(  temperature, INPUT);
  pinMode(  lightLevel,  INPUT);
  //initialize Serial Communication to communicate with RPI, with Baud rate=9600
  Serial.begin(9600);
}

//Check serial buffer for any strings from Matlab and call Corresponding Function
void loop() {
  if(Serial.available() > 0) { //Check serial buffer if any data available
    serialData = Serial.read(); //read string from serial buffer
    if(serialData == 'h')
      hardwareDispense();
    else if(serialData == 'd')
      openDoor();
    else if(serialData == 'w')
      openWarehouse();
    else if(serialData == 's')
      sendSensorData();
  }
}

void hardwareDispense(){
  int bills[4];
  int total = 0;
  for (int i = 0; i<=4; i++){
    while(Serial.available() <= 0){ //wait until Matlab sends voltage on serial buffer
    }
    serialData = Serial.read(); //get the desired count from serial
    bills[i] = char2Int(serialData); //converting serial string into int
    total = total + bills[i];
  }
  //define IR sensor pin as interrupt pin to add one automatically to bills count
  attachInterrupt(digitalPinToInterrupt(infrared), counter, RISING);

  //TODO: Dispense here
  
  //check number of dispensed bills
  if(billCount == total)
    Serial.print("t");
  else if(billCount != total)
    Serial.print("f");
  billCount = 0; //resets billCount
}

void openDoor(){
  digitalWrite(drawer, HIGH);
  delay(doorDelay);
  digitalWrite(drawer, LOW);
}

void openWarehouse(){
  digitalWrite(warehouse, HIGH);
  delay(warehouseDelay);
  digitalWrite(warehouse, LOW);
}


void sendSensorData(){
  tempFloat = analogRead(temperature);
  tempFloat = tempFloat * (5 / 1024); //converting binary number to voltage (0-1024)->(0-5)
  Serial.print(tempFloat);
  tempFloat = analogRead(lightLevel);
  tempFloat = tempFloat * (5 / 1024); //converting binary number to voltage (0-1024)->(0-5)
  Serial.print(tempFloat);
}

//converting array of characters to int
int char2Int (char ch){
  String inString = ""; //empty the string
  inString += (char)ch; //add the array to the empty string
  int temp = inString.toInt(); //convert the string to int
  return temp; //return converted variable
}

//Calculate the current motor using
float getCurrent() {
  tempFloat = analogRead(current); //read from motor current sensor pin
  tempFloat = (tempFloat * 5) / 1024; //converting binary number to voltage (0-1024)->(0-5)
  tempFloat = tempFloat - 2; //subtracting sensor offset
  tempFloat = tempFloat / 0.185; //mapping sensor output 'Voltage' to 'Ampere', 185mV/A
  return tempFloat;
}

//adds one to billCount: used as ISR 'called when IR sensor detects new bill'
void counter() {
  billCount = billCount + 1;
}

//Dispensing functions
//up down motor control    
void moveUp(){
  for(i=0;i<iup;i++){
    for(j=0;j<jup;j++){
      digitalWrite(upPin1,seq[j][0]);
      digitalWrite(upPin2,seq[j][1]);
      digitalWrite(upPin3,seq[j][2]);
      digitalWrite(upPin4,seq[j][3]);
      delay(upMotorDelay);
    }
  }
}
void moveDown(){
  for(i=0;i<iup;i++){
    for(j=jup;j>0;j--){
      digitalWrite(upPin1,seq[j][0]);
      digitalWrite(upPin2,seq[j][1]);
      digitalWrite(upPin3,seq[j][2]);
      digitalWrite(upPin4,seq[j][3]);
      delay(upMotorDelay);
    }
  }
}

//// stop motors
void roMotorStop(){
  digitalWrite(roPin1,LOW);
  digitalWrite(roPin2,LOW);
  digitalWrite(roPin3,LOW);
  digitalWrite(roPin4,LOW);
}
void upMotorStop(){
  digitalWrite(upPin1,LOW);
  digitalWrite(upPin2,LOW);
  digitalWrite(upPin3,LOW);
  digitalWrite(upPin4,LOW);
}

/// use to move 72 degree     
void medicineMove(){
  for(i=0;i<i72;i++){
    for(j=0;j<j72;j++){
      digitalWrite(roPin1,seq[j][0]);
      digitalWrite(roPin2,seq[j][1]);
      digitalWrite(roPin3,seq[j][2]);
      digitalWrite(roPin4,seq[j][3]);
      delay(roMotorDelay);
    }
  }      
}
