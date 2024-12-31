#ifndef ESP_COMMS_HPP
#define ESP_COMMS_HPP

#include <cstring>
#include <sstream>
#include <cstdlib>
#include <libserial/SerialPort.h>
#include <iostream>

using namespace LibSerial;
BaudRate convert_baud_rate(int baud_rate)
{
  // Just handle some common baud rates
  switch (baud_rate)
  {
    case 1200: return BaudRate::BAUD_1200;
    case 1800: return BaudRate::BAUD_1800;
    case 2400: return BaudRate::BAUD_2400;
    case 4800: return BaudRate::BAUD_4800;
    case 9600: return BaudRate::BAUD_9600;
    case 19200: return BaudRate::BAUD_19200;
    case 38400: return BaudRate::BAUD_38400;
    case 57600: return BaudRate::BAUD_57600;
    case 115200: return BaudRate::BAUD_115200;
    case 230400: return BaudRate::BAUD_230400;
    default:
      std::cout << "Error! Baud rate " << baud_rate << " not supported! Default to 57600" << std::endl;
      return BaudRate::BAUD_57600;
  }
}

class EspComms
{

public:

  EspComms() = default;

  void connect(const std::string &serial_device, int32_t baud_rate, int32_t timeout_ms)
  {  
    timeout_ms_ = timeout_ms;
    serial_conn_.Open(serial_device);
    serial_conn_.SetBaudRate(convert_baud_rate(baud_rate));
  }

  void disconnect()
  {
    serial_conn_.Close();
  }

  bool connected() const
  {
    return serial_conn_.IsOpen();
  }


  std::string send_msg(const std::string &msg_to_send, bool print_output = false)
  {
    serial_conn_.FlushIOBuffers(); // Just in case
    serial_conn_.Write(msg_to_send);

    std::string response = "";
    try
    {
      // Responses end with \r\n so we will read up to (and including) the \n.
      serial_conn_.ReadLine(response, '\n', timeout_ms_);
    }
    catch (const LibSerial::ReadTimeout&)
    {
        std::cerr << "The ReadByte() call has timed out. This is sent." << std::endl ;
        std::cout << "Sent: " << msg_to_send << " Recv: " << response << std::endl;
    }

    if (print_output)
    {
      std::string msg = msg_to_send.substr(0, msg_to_send.length()-1);
      std::cout << "Sent: " << msg_to_send << " Recv: " << response << std::endl;
    }

    return response;
  }

  void send_empty_msg()
  {
    std::string response = send_msg("\r");
  }
  
  void set_motor_values(int val_1, int val_2)
  {
    std::stringstream ss;
    ss << "m " << val_1 << " " << val_2 << "\r";
    send_msg(ss.str());
  }

  void run_motor_pwm(int val_1, int val_2)
  {
    std::stringstream ss;
    ss << "o " << val_1 << " " << val_2 << "\r";
    send_msg(ss.str());
  }

  void set_pid_values(int k_p, int k_d, int k_i, int k_o)
  {
    std::stringstream ss;
    ss << "u " << k_p << ":" << k_d << ":" << k_i << ":" << k_o << "\r";
    send_msg(ss.str());
  }

  void reset_encoders(){
    std::string response = send_msg("r\r");
  }

  void read_encoders(int &enc_1, int &enc_2)
  {
    std::string response = send_msg("e\r");

    std::string delimiter = " ";
    size_t del_pos = response.find(delimiter);
    std::string token_1 = response.substr(0, del_pos);
    std::string token_2 = response.substr(del_pos + delimiter.length());

    enc_1 = std::atoi(token_1.c_str());
    enc_2 = std::atoi(token_2.c_str());
  }

    void read_range_sensors(double &sensor_1, double &sensor_2)
  {
    std::string response = send_msg("l\r");

    std::string delimiter = " ";
    size_t del_pos = response.find(delimiter);
    std::string token_1 = response.substr(0, del_pos);
    std::string token_2 = response.substr(del_pos + delimiter.length());

    sensor_1 = std::atof(token_1.c_str());
    sensor_2 = std::atof(token_2.c_str());
  }

    void read_imu_sensor(double &vel_x, double &vel_y, double &vel_z, double &ang_x, double &ang_y, double &ang_z)
  {
    std::string response = send_msg("i\r");

    std::string delimiter = " ";
    // size_t del_pos = response.find(delimiter);
    // std::string token_1 = response.substr(0, del_pos);
    // std::string token_2 = response.substr(del_pos + delimiter.length());

    std::string subtoken = "";
    int start, end = -1*delimiter.size();
    int cnt = 0;
    do {
        start = end + delimiter.size();
        end = response.find(delimiter, start);
        // cout << s.substr(start, end - start) << endl; //need to add std:: if no namespace
        subtoken = response.substr(start, end - start);

        if(cnt == 0)      vel_x = std::atof(subtoken.c_str());
        else if(cnt == 1) vel_y = std::atof(subtoken.c_str());
        else if(cnt == 2) vel_z = std::atof(subtoken.c_str());
        else if(cnt == 3) ang_x = std::atof(subtoken.c_str());
        else if(cnt == 4) ang_y = std::atof(subtoken.c_str());
        else if(cnt == 5) ang_z = std::atof(subtoken.c_str());

        cnt++;
    } while (end != -1);
    
    // vel_x = std::atof(token_1.c_str());
    // vel_y = std::atof(token_1.c_str());
    // vel_z = std::atof(token_1.c_str());
    // ang_x = std::atof(token_2.c_str());
    // ang_y = std::atof(token_2.c_str());
    // ang_z = std::atof(token_2.c_str());
  }
private:
    SerialPort serial_conn_;
    int timeout_ms_;
};

#endif // DIFFDRIVE_ARDUINO_ARDUINO_COMMS_HPP