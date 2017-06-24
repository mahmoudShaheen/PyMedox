////////////////////////////////////////////////////////////
//               @author: Mahmoud Shaheen                 //
//                MedicalBox IOT Project                  //
//               Arduino-Serial-Raspberry                 //
////////////////////////////////////////////////////////////

//Arduino Pins definition
//stepper-1
#define    stepper11       2
#define    stepper12       3
#define    stepper13       4
#define    stepper14       5
//stepper-2
#define    stepper21       6
#define    stepper22       7
#define    stepper23       8
#define    stepper24       9
//other outputs
#define    drawer         10
#define    warehouse      11
#define    relay          12
//sensors
#define    infrared        13
#define    current         A0
#define    temperature     A1
#define    lightLevel      A2

#define    doorDelay        1000
#define    warehouseDelay   1000

//variables definition
char  serialData; //for storing serial string
float tempFloat = 0; //for saving sensor data temporary
int billCount = 0; //for storing bill count added by ISR

void setup() {
  //Setting input/output Pins
  //outputs
  pinMode(  stepper11,  OUTPUT);
  pinMode(  stepper12,  OUTPUT);
  pinMode(  stepper13,  OUTPUT);
  pinMode(  stepper14,  OUTPUT);
  pinMode(  stepper21,  OUTPUT);
  pinMode(  stepper22,  OUTPUT);
  pinMode(  stepper23,  OUTPUT);
  pinMode(  stepper24,  OUTPUT);
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
