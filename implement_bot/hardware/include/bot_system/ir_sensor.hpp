#ifndef IR_BOT_HPP
#define IR_BOT_HPP

#include <string>

class RangeSensor 
{
    public:
    std::string name = "";
    double pos = 0.0;

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