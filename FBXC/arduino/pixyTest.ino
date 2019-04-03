#include <Pixy2.h>

Pixy2 pixy;

int samplingRate = 0; // number of samples to get every second so as not to screw up the buffer on the arduino

void setup() {
    // start serial comms
    Serial.begin(9600);
    // set up pixycam
    pixy.init();
    pixy.changeProg("line");
    // pixy.setLamp(1, 0);
}

void loop() {
    pixy.line.getMainFeatures();
    pixy.line.vectors[0].print();
    // delay((int) (1000/samplingRate));
}