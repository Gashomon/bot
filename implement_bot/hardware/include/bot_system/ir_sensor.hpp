#ifndef IR_SENSOR_HPP
#define IR_SENSOR_HPP

#include <string>

class RangeSensor 
{
    public:
    std::string name = "";
    double range = 0.0;

    RangeSensor() = default;
    RangeSensor(const std::string &sensorName)
    {
        setup(sensorName);
    };

    void setup(const std::string &sensorName)
    {
        name = sensorName;
    }

};

#endif