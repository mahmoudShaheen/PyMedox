////////////////////////////////////////////////////////////
//               @author: Mahmoud Shaheen                 //
//                MedicalBox IOT Project                  //
//               Arduino-Serial-Raspberry                 //
////////////////////////////////////////////////////////////

//Arduino Pins definition
//stepper-1 "up/down" pump
#define    upPin1       2
#define    upPin2       3
#define    upPin3       4
#define    upPin4       5
//stepper-2 "rotation" plate
#define    roPin1       6
#define    roPin2       7
#define    roPin3       8
#define    roPin4       9
//other outputs
#define    drawer       10
#define    warehouse    11
#define    pump         12
//sensors
#define    infrared     13
#define    current      A0
#define    temperature  A1
#define    lightLevel   A2

#define    doorDelay        1000 //time to keep door motor working
#define    warehouseDelay   1000 //time to keep warehouse motor working
#define    releaseBillDelay 1000 //to wait untill bill released
#define    getBillDelay     1000 //to wait until bill catched for sure
#define    upStepperDelay   3    //to wait before up/down steps
#define    roStepperDelay   10   //to wait before rotation steps

#define    currentThreeshold 5    //current where pump gets a bill
#define    currentOffset     2    //offset for current sensor
#define    maxUpSteps        100  //maximum number of steps pump should move
#define    step72            10   //steps required to rotate 72 degrees

//variables definition
char  serialData;             //for storing serial string
float tempFloat       = 0;    //for saving sensor data temporary
int billCount         = 0;    //for storing bill count added by ISR
int selectedWarehouse = 0;    //to know what warehouse is above the door "0 is the empty one"

/// using half step mode
int seq[8][4]={ {1,0,0,0},
                {1,1,0,0},
                {0,1,0,0},
                {0,1,1,0},
                {0,0,1,0},
                {0,0,1,1},
                {0,0,0,1},
                {1,0,0,1} };


void setup() {
  //Setting input/output Pins
  //outputs
  pinMode(  upPin1,     OUTPUT);
  pinMode(  upPin2,     OUTPUT);
  pinMode(  upPin3,     OUTPUT);
  pinMode(  upPin4,     OUTPUT);
  pinMode(  roPin1,     OUTPUT);
  pinMode(  roPin2,     OUTPUT);
  pinMode(  roPin3,     OUTPUT);
  pinMode(  roPin4,     OUTPUT);
  pinMode(  drawer,     OUTPUT);
  pinMode(  warehouse,  OUTPUT);
  pinMode(  pump,       OUTPUT);
  //inputs
  pinMode(  infrared,    INPUT);
  pinMode(  current,     INPUT);
  pinMode(  temperature, INPUT);
  pinMode(  lightLevel,  INPUT);
  //initialize Serial Communication to communicate with RPI, with Baud rate=9600
  Serial.begin(9600);
}

//Check serial buffer for any strings from RPI and call Corresponding Function
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

//adds one to billCount: used as ISR 'called when IR sensor detects new bill'
void counter() {
  billCount = billCount + 1;
}

//Calculate the current pump using
float getCurrent() {
  tempFloat = analogRead(current); //read from motor current sensor pin
  tempFloat = (tempFloat * 5) / 1024; //converting binary number to voltage (0-1024)->(0-5)
  tempFloat = tempFloat - currentOffset; //subtracting sensor offset
  tempFloat = tempFloat / 0.185; //mapping sensor output 'Voltage' to 'Ampere', 185mV/A
  return tempFloat;
}

//dispenses given bill array
//array is given via serial port from RPI
void hardwareDispense(){
  int bills[4];
  int total = 0;
  for (int i = 0; i<=4; i++){
    while(Serial.available() <= 0){ //wait until RPI sends voltage on serial buffer
    }
    serialData = Serial.read(); //get the desired count from serial
    bills[i] = char2Int(serialData); //converting serial string into int
    total = total + bills[i];
  }
  //define IR sensor pin as interrupt pin to add one automatically to bills count
  attachInterrupt(digitalPinToInterrupt(infrared), counter, RISING);

  //dispense bill array
  for (int i = 0 ; i < 4; i++){
    for (int j = bills[i]; j > 0; j--){
      dispenseOneBill(i+1); //dispense one bill of warehouse number i+1
      //as warehouse 0 is the empty one and 1 to 4 is the drugs' warehouses
    }
  }
  stopMotors(); //stop all motors "set all pins to low"
  //check number of dispensed bills
  if(billCount == total)
    Serial.print("t");
  else if(billCount != total)
    Serial.print("f");
  billCount = 0; //resets billCount
}

//dispense one bill from given warehouse number
void dispenseOneBill(int warehouseNumber){
  moveToWarehouse(warehouseNumber); //move to drug warehouse
  getBill(); //get one bill using pump
  moveToWarehouse(0); //return to empty warehouse
  releaseBill(); //release bill to the door
}

//move to given warehouse number
void moveToWarehouse(int warehouseNumber){
  int steps = 0;
  if(warehouseNumber == 0){
    steps = 5 - selectedWarehouse;
  }else{ //empty warehouse selected
    steps = warehouseNumber;
  }
  for (int i = 0; i < steps; i++){ //move the required steps
    moveOneStep(); //moves 72 degree to select next warehouse
  }
}

//get one bill using pump
void getBill(){
  int steps = 0; //for storing steps to return to initial position again
  digitalWrite(pump, HIGH); //activates the pump
  while(getCurrent() < currentThreeshold && steps < maxUpSteps){ //go down until gets one bill
    stepDown(); //move one step down
  }
  delay(getBillDelay); //to wait until bill catched for sure
  for(int i = 0; i<steps; i++){ //retun to initial position
    stepUp(); //move one step up
  }
}

//release bill to the door
void releaseBill(){
  digitalWrite(pump, LOW); //disable the pump
  delay(releaseBillDelay); //to wait untill bill released
}

//moves 72 degree to select next warehouse
void moveOneStep(){
  for(int i = 0; i < step72; i++){
    for(int j = 0; j <= 7; j++){
      digitalWrite(upPin1, seq[i][0]);
      digitalWrite(upPin2, seq[i][1]);
      digitalWrite(upPin3, seq[i][2]);
      digitalWrite(upPin4, seq[i][3]);
      delay(roStepperDelay);
    }
  }
}

//move one step up
void stepUp(){
  for(int i = 0; i <= 7; i++){
    digitalWrite(upPin1, seq[i][0]);
    digitalWrite(upPin2, seq[i][1]);
    digitalWrite(upPin3, seq[i][2]);
    digitalWrite(upPin4, seq[i][3]);
    delay(upStepperDelay);
  }
}

//move one step down
void stepDown(){
  for(int i = 7; i >= 0; i--){
    digitalWrite(upPin1, seq[i][0]);
    digitalWrite(upPin2, seq[i][1]);
    digitalWrite(upPin3, seq[i][2]);
    digitalWrite(upPin4, seq[i][3]);
    delay(upStepperDelay);
  }
}

//stop all motors "set all pins to low"
void stopMotors(){
  //up/down stepper
  digitalWrite(upPin1, LOW);
  digitalWrite(upPin2, LOW);
  digitalWrite(upPin3, LOW);
  digitalWrite(upPin4, LOW);
  //rotation stepper
  digitalWrite(roPin1, LOW);
  digitalWrite(roPin2, LOW);
  digitalWrite(roPin3, LOW);
  digitalWrite(roPin4, LOW);
  //pump
  digitalWrite(pump, LOW);
}
