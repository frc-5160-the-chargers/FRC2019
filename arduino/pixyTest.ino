#include <Pixy2.h>

Pixy2 pixy;

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
    pixy.line.getAllFeatures();
    // print all vectors
    for (i=0; i<pixy.line.numVectors; i++)
    {
        sprintf(buf, "line %d: ", i);
        Serial.print(buf);
        pixy.line.vectors[i].print();
    }
}