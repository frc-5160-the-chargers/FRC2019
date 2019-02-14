#include <Pixy2.h>

Pixy2 pixy;

bool a = true;

void setup()
{
    Serial.begin(9600);
    pixy.init();
    pixy.changeProg("line");
}

void loop()
{
    int8_t i;
    char buf[128];
    pixy.line.getMainFeatures();

    pixy.line.vectors[0].print();
    Serial.println("");

    pixy.setLamp(a?1:0, a?1:1);
    a = a;
}