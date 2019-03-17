#include <Pixy2.h>

Pixy2 pixy;

void setup() {
    // start serial comms
    Serial.begin(9600);
    // set up pixycam
    pixy.init();
    pixy.changeProg("line");
    pixy.setLamp(1, 0);
}

void loop() {
    pixy.line.getMainFeatures();
    pixy.line.vectors[0].print();
}