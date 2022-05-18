
void setup() 
{                
  /* Initialize serial */
  Serial.begin(115200); 

  //-----------------------Steppers------------------------
  pinMode(EN, OUTPUT); 
    
  c_stepper.setMaxSpeed(c_max_speed);
  c_stepper.setSpeed(c_speed);

  b_stepper.setMaxSpeed(b_max_speed);
  b_stepper.setSpeed(b_speed);

  enable_steppers("no");

  //------------------------current sensor---------------
  pinMode(current_pin, INPUT);

  //----------------------Valve---------------------
  pinMode(relay1,OUTPUT);
  pinMode(relay2,OUTPUT);
  rele('0');



    
}

void q(){
  Serial.println("nano");
}
