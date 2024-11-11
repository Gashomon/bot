#ifndef IMU_SENSOR_HPP
#define IMU_SENSOR_HPP

#include <string>

class Imusensor 
{
    public:
    std::string name = "";
    double position_x = 0.0;
    double position_y = 0.0;
    double position_z = 0.0;
    double position_w = 0.0;

    double angular_velocity_x = 0.0;
    double angular_velocity_y = 0.0;
    double angular_velocity_z = 0.0;
    double angular_velocity_w = 0.0;

    double linear_acceleration_x = 0.0;
    double linear_acceleration_y = 0.0;
    double linear_acceleration_z = 0.0;
    double linear_acceleration_w = 0.0;

    double velocity_x = 0.0;
    double velocity_z = 0.0;
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