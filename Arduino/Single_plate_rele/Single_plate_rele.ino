//Librerias
#include <AccelStepper.h>
#include <Adafruit_PWMServoDriver.h>
#include <EEPROM.h> 

//-----------------------General-------------------------
char incomingByte;

//-----------------------Steppers------------------------
#define EN 8
//-------Carrete--Eje Y

#define c_DIR 6   /* Pin de dirección para el eje carrete */
#define c_STEP 3  /* Pin de pasos para el eje carrete */
AccelStepper c_stepper(AccelStepper::DRIVER, c_STEP, c_DIR);


long cc = 100; //100 para operacion noraml, 1 para debug

long m_1 = 74 * cc;//TODO Debe quedar definido el metro, luego en las funciones a,b,c se multiplica por este valor
long m_5 = 380 * cc;
long m_10 = 860 * cc;

int ponderador = 9700; //ponderador que se usa para subir y bajar carrete manual

int c_speed = 1000;
int c_max_speed = 1000;



//-------Bomba--Eje X

#define b_DIR 5   /* Pin de dirección para el eje bomba */
#define b_STEP 2  /* Pin de pasos para el eje bomba */
AccelStepper b_stepper(AccelStepper::DRIVER, b_STEP, b_DIR);

long water_renovation = -70000; //60.000 para renovacion real, 600 para pruebas

int b_speed = 400;
int b_max_speed = 500;



//-----------------------Current Sensor------------------------

//int IN1 = 11; //Z End Stop (M1)
//int IN2 = 12; //Spin Enable (M1)
//int ENA = 10; //Y End Stop (M1)
//int IN3 = 13; //SpinDir (M2)
//int IN4 = A3; //Coolant (M2)
//int ENB = 9; //X End Stop (M2)



int current_pin = A3;

float current_limit = 0.18;
float sensor_sensitivity = 0.1; // condicion del sensor de 10 A

//----------------------Reles----------------------------------------

int relay1 = 10;
int relay2 = 9; //Energia placa


//int next_valve = 1; // quedo de cuando habian valvulas, esperando a la reimplamentacion


//----------------------Servos-------------------------------------------------

Adafruit_PWMServoDriver servos = Adafruit_PWMServoDriver();

int posA_0 = 190;
int posA_180 = 500;

int posB_0 = 190;
int posB_180 = 450;

int servo_enable_pin = 11;


uint8_t sd_index = 15; //superior - derecho
uint8_t id_index = 1; //superior - izquierdo
uint8_t ii_index = 14; //inferior - derecho
uint8_t si_index = 0; //inferior - izquierdo
