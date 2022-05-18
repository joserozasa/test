//Librerias
#include <AccelStepper.h>
#include <EEPROM.h> 

//-----------------------General-------------------------
char incomingByte;

//-----------------------Steppers------------------------
#define EN 8
//-------Carrete--Eje Y

#define c_DIR 6   /* Pin de dirección para el eje carrete */
#define c_STEP 3  /* Pin de pasos para el eje carrete */
AccelStepper c_stepper(AccelStepper::DRIVER, c_STEP, c_DIR);


long cc = 100; //10 a 100 para operacion noraml, 1 para debug

long m_1 = 74 * cc;//TODO Debe quedar definido el metro, luego en las funciones a,b,c se multiplica por este valor
long m_5 = 380 * cc;
long m_10 = 800 * cc;

int ponderador = 9700; //9700 o 970ponderador que se usa para subir y bajar carrete manual

int c_speed = 1000;
int c_max_speed = 1000;



//-------Bomba--Eje X

#define b_DIR 5  /* Pin de dirección para el eje bomba */
#define b_STEP 2  /* Pin de pasos para el eje bomba */
AccelStepper b_stepper(AccelStepper::DRIVER, b_STEP, b_DIR);

long water_renovation = -80000; //600 a 60.000 para renovacion real, 600 para pruebas

int b_speed = 400;
int b_max_speed = 500;


//----------------------Reles----------------------------------------

int relay2 = 10; //EndStopY
int relay1 = 9; //Energia placa -- Endtop X

//-----------------------Current Sensor------------------------


int current_pin = A3;

float current_limit = 0.17;
float sensor_sensitivity = 0.1; // condicion del sensor de 10 A
