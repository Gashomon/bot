#ifndef IR_BOT_HPP
#define IR_BOT_HPP

#include <string>

class Imusensor 
{
    public:
    std::string name = "";
    double vel = 0.0;

    Imusensor() = default;
    Imusensor(const std::string &sensorName)
    {
        setup(sensorName);
    };

    void setup(const std::string &sensorName)
    {
        name = sensorName;
    }
    
};

#endif