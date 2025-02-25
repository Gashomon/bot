// Copyright 2021 ros2_control Development Team
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include "include/bot_system/bot_system.hpp"

#include <chrono>
#include <cmath>
#include <limits>
#include <memory>
#include <vector>

#include "hardware_interface/types/hardware_interface_type_values.hpp"
#include "rclcpp/rclcpp.hpp"

namespace NewHardwareInterface
{
hardware_interface::CallbackReturn BotHardwareSystem::on_init(
  const hardware_interface::HardwareInfo & info)
{
  if (
    hardware_interface::SystemInterface::on_init(info) !=
    hardware_interface::CallbackReturn::SUCCESS)
  {
    return hardware_interface::CallbackReturn::ERROR;
  }

  cfg_.left_wheel_name = info_.hardware_parameters["left_wheel_name"];
  cfg_.right_wheel_name = info_.hardware_parameters["right_wheel_name"];
  cfg_.loop_rate = std::stof(info_.hardware_parameters["loop_rate"]);
  cfg_.device = info_.hardware_parameters["device"];
  cfg_.baud_rate = std::stoi(info_.hardware_parameters["baud_rate"]);
  cfg_.timeout_ms = std::stoi(info_.hardware_parameters["timeout_ms"]);
  cfg_.enc_counts_per_rev = std::stoi(info_.hardware_parameters["enc_counts_per_rev"]);
  
  cfg_.left_range_name = info_.hardware_parameters["left_range_name"];
  cfg_.right_range_name = info_.hardware_parameters["right_range_name"];
  // cfg_.min_range = std::stof(info_.hardware_parameters["minimum_range"]);
  // cfg_.max_range = std::stof(info_.hardware_parameters["maximum_range"]);

  cfg_.imu_name = info_.hardware_parameters["imu_name"];

  if (info_.hardware_parameters.count("pid_p") > 0)
  {
    cfg_.pid_p = std::stoi(info_.hardware_parameters["pid_p"]);
    cfg_.pid_d = std::stoi(info_.hardware_parameters["pid_d"]);
    cfg_.pid_i = std::stoi(info_.hardware_parameters["pid_i"]);
    cfg_.pid_o = std::stoi(info_.hardware_parameters["pid_o"]);
  }
  else
  {
    RCLCPP_INFO(rclcpp::get_logger("BotHardwareSystem"), "PID values not supplied, using defaults.");
  }
  
  wheel_l_.setup(cfg_.left_wheel_name, cfg_.enc_counts_per_rev);
  wheel_r_.setup(cfg_.right_wheel_name, cfg_.enc_counts_per_rev);
  range_l_.setup(cfg_.left_range_name);
  range_r_.setup(cfg_.right_range_name);
  imu_.setup(cfg_.imu_name);
  
  for (const hardware_interface::ComponentInfo & joint : info_.joints)
  {
    if (joint.command_interfaces.size() != 1)
    {
      RCLCPP_FATAL(
        rclcpp::get_logger("BotHardwareSystem"),
        "Wheel Joint '%s' has %zu command interfaces found. 1 expected.", joint.name.c_str(),
        joint.command_interfaces.size());
      return hardware_interface::CallbackReturn::ERROR;
    }

    if (joint.command_interfaces[0].name != hardware_interface::HW_IF_VELOCITY)
    {
      RCLCPP_FATAL(
        rclcpp::get_logger("BotHardwareSystem"),
        "Wheel Joint '%s' have %s command interfaces found. '%s' expected.", joint.name.c_str(),
        joint.command_interfaces[0].name.c_str(), hardware_interface::HW_IF_VELOCITY);
      return hardware_interface::CallbackReturn::ERROR;
    }

    if (joint.state_interfaces.size() != 2)
    {
      RCLCPP_FATAL(
        rclcpp::get_logger("BotHardwareSystem"),
        "Wheel Joint '%s' has %zu state interface. 2 expected.", joint.name.c_str(),
        joint.state_interfaces.size());
      return hardware_interface::CallbackReturn::ERROR;
    }

    if (joint.state_interfaces[0].name != hardware_interface::HW_IF_POSITION)
    {
      RCLCPP_FATAL(
        rclcpp::get_logger("BotHardwareSystem"),
        "Wheel Joint '%s' have '%s' as first state interface. '%s' expected.", joint.name.c_str(),
        joint.state_interfaces[0].name.c_str(), hardware_interface::HW_IF_POSITION);
      return hardware_interface::CallbackReturn::ERROR;
    }

    if (joint.state_interfaces[1].name != hardware_interface::HW_IF_VELOCITY)
    {
      RCLCPP_FATAL(
        rclcpp::get_logger("BotHardwareSystem"),
        "Wheel Joint '%s' have '%s' as second state interface. '%s' expected.", joint.name.c_str(),
        joint.state_interfaces[1].name.c_str(), hardware_interface::HW_IF_VELOCITY);
      return hardware_interface::CallbackReturn::ERROR;
    }
    
  }
  
  for(const hardware_interface::ComponentInfo & sensor : info_.sensors)
  {
    RCLCPP_INFO(rclcpp::get_logger("BotHardwareSystem"),"this is sensor '%s'", sensor.name.c_str());
    if(sensor.name.c_str() == cfg_.left_range_name || sensor.name.c_str() == cfg_.right_range_name)
    {
      if (sensor.command_interfaces.size() != 0)
      {
        RCLCPP_FATAL(
          rclcpp::get_logger("BotHardwareSystem"),
          "Range sensor '%s' has %zu command interfaces found. 1 expected.", sensor.name.c_str(),
          sensor.command_interfaces.size());
        return hardware_interface::CallbackReturn::ERROR;
      }

      if (sensor.state_interfaces.size() != 1)
      {
        RCLCPP_FATAL(
          rclcpp::get_logger("BotHardwareSystem"),
          "Range sensor '%s' has %zu state interface. 1 expected.", sensor.name.c_str(),
          sensor.state_interfaces.size());
        return hardware_interface::CallbackReturn::ERROR;
      }

      if (sensor.state_interfaces[0].name != hardware_interface::HW_IF_POSITION){
        RCLCPP_FATAL(
          rclcpp::get_logger("BotHardwareSystem"),
          "Range sensor '%s' have %s command interfaces found. '%s' expected.", sensor.name.c_str(),
          sensor.command_interfaces[0].name.c_str(), hardware_interface::HW_IF_VELOCITY);
        return hardware_interface::CallbackReturn::ERROR;
      }
    }
    
    else if(sensor.name.c_str() == cfg_.imu_name)
    {
      if (sensor.command_interfaces.size() != 0)
      {
        RCLCPP_FATAL(
          rclcpp::get_logger("BotHardwareSystem"),
          "IMU sensor '%s' has %zu command interfaces found. 1 expected.", sensor.name.c_str(),
          sensor.command_interfaces.size());
        return hardware_interface::CallbackReturn::ERROR;
      }

      if (sensor.state_interfaces.size() != 1)
      {
        RCLCPP_FATAL(
          rclcpp::get_logger("BotHardwareSystem"),
          "sensor '%s' has %zu state interface. 1 expected.", sensor.name.c_str(),
          sensor.state_interfaces.size());
        return hardware_interface::CallbackReturn::ERROR;
      }

      if (sensor.state_interfaces[0].name != hardware_interface::HW_IF_VELOCITY){
        RCLCPP_FATAL(
          rclcpp::get_logger("BotHardwareSystem"),
          "sensor '%s' have %s command interfaces found. '%s' expected.", sensor.name.c_str(),
          sensor.command_interfaces[0].name.c_str(), hardware_interface::HW_IF_VELOCITY);
        return hardware_interface::CallbackReturn::ERROR;
      }
    }
    
    else
    {
      RCLCPP_FATAL(
          rclcpp::get_logger("BotHardwareSystem"),
          "Unexpected sensor '%s'", sensor.name.c_str());
        return hardware_interface::CallbackReturn::ERROR;
    }
    
  }
  return hardware_interface::CallbackReturn::SUCCESS;
}

std::vector<hardware_interface::StateInterface> BotHardwareSystem::export_state_interfaces()
{
  std::vector<hardware_interface::StateInterface> state_interfaces;

  state_interfaces.emplace_back(hardware_interface::StateInterface(
    wheel_l_.name, hardware_interface::HW_IF_POSITION, &wheel_l_.pos));
  state_interfaces.emplace_back(hardware_interface::StateInterface(
    wheel_l_.name, hardware_interface::HW_IF_VELOCITY, &wheel_l_.vel));

  state_interfaces.emplace_back(hardware_interface::StateInterface(
    wheel_r_.name, hardware_interface::HW_IF_POSITION, &wheel_r_.pos));
  state_interfaces.emplace_back(hardware_interface::StateInterface(
    wheel_r_.name, hardware_interface::HW_IF_VELOCITY, &wheel_r_.vel));

  state_interfaces.emplace_back(hardware_interface::StateInterface(
    range_l_.name, "range", &range_l_.range));

  state_interfaces.emplace_back(hardware_interface::StateInterface(
    range_r_.name, "range", &range_r_.range));

  state_interfaces.emplace_back(hardware_interface::StateInterface(
    imu_.name, "orientation.x", &imu_.position_x));

  state_interfaces.emplace_back(hardware_interface::StateInterface(
    imu_.name, "orientation.y", &imu_.position_y));

  state_interfaces.emplace_back(hardware_interface::StateInterface(
    imu_.name, "orientation.z", &imu_.position_z));
  
  state_interfaces.emplace_back(hardware_interface::StateInterface(
    imu_.name, "orientation.w", &imu_.position_w));
  
  state_interfaces.emplace_back(hardware_interface::StateInterface(
    imu_.name, "angular_velocity.x", &imu_.angular_velocity_x));

  state_interfaces.emplace_back(hardware_interface::StateInterface(
    imu_.name, "angular_velocity.y", &imu_.angular_velocity_y));

  state_interfaces.emplace_back(hardware_interface::StateInterface(
    imu_.name, "angular_velocity.z", &imu_.angular_velocity_z));
  
  state_interfaces.emplace_back(hardware_interface::StateInterface(
    imu_.name, "angular_velocity.w", &imu_.angular_velocity_w));

  state_interfaces.emplace_back(hardware_interface::StateInterface(
    imu_.name, "linear_acceleration.x", &imu_.linear_acceleration_x));

  state_interfaces.emplace_back(hardware_interface::StateInterface(
    imu_.name, "linear_acceleration.y", &imu_.linear_acceleration_y));

  state_interfaces.emplace_back(hardware_interface::StateInterface(
    imu_.name, "linear_acceleration.z", &imu_.linear_acceleration_z));
  
  state_interfaces.emplace_back(hardware_interface::StateInterface(
    imu_.name, "linear_acceleration.w", &imu_.linear_acceleration_w));


  return state_interfaces;
}

std::vector<hardware_interface::CommandInterface> BotHardwareSystem::export_command_interfaces()
{
  std::vector<hardware_interface::CommandInterface> command_interfaces;

  command_interfaces.emplace_back(hardware_interface::CommandInterface(
    wheel_l_.name, hardware_interface::HW_IF_VELOCITY, &wheel_l_.cmd));

  command_interfaces.emplace_back(hardware_interface::CommandInterface(
    wheel_r_.name, hardware_interface::HW_IF_VELOCITY, &wheel_r_.cmd));

  return command_interfaces;
}

hardware_interface::CallbackReturn BotHardwareSystem::on_configure(
  const rclcpp_lifecycle::State & /*previous_state*/)
{
  RCLCPP_INFO(rclcpp::get_logger("BotHardwareSystem"), "Configuring ...please wait...");
  if (comms_.connected())
  {
    RCLCPP_INFO(rclcpp::get_logger("BotHardwareSystem"), "Oops ...reconnecting comms...");
    comms_.disconnect();
  }
  while(!comms_.connected())
  {
    comms_.connect(cfg_.device, cfg_.baud_rate, cfg_.timeout_ms);
    RCLCPP_INFO(rclcpp::get_logger("BotHardwareSystem"), "Connecting comms...!");
  }
  RCLCPP_INFO(rclcpp::get_logger("BotHardwareSystem"), "Successfully configured!");
  return hardware_interface::CallbackReturn::SUCCESS;
}

hardware_interface::CallbackReturn BotHardwareSystem::on_cleanup(
  const rclcpp_lifecycle::State & /*previous_state*/)
{
  RCLCPP_INFO(rclcpp::get_logger("BotHardwareSystem"), "Cleaning up ...please wait...");
  if (comms_.connected())
  {
    comms_.clearbuffs();
    comms_.send_empty_msg();
    comms_.disconnect();
  }
  RCLCPP_INFO(rclcpp::get_logger("BotHardwareSystem"), "Successfully cleaned up!");

  return hardware_interface::CallbackReturn::SUCCESS;
}


hardware_interface::CallbackReturn BotHardwareSystem::on_activate(
  const rclcpp_lifecycle::State & /*previous_state*/)
{
  RCLCPP_INFO(rclcpp::get_logger("BotHardwareSystem"), "Activating ...please wait...");
  if (!comms_.connected())
  {
    RCLCPP_INFO(rclcpp::get_logger("BotHardwareSystem"), "notconnected..");
    return hardware_interface::CallbackReturn::ERROR;
  }
  comms_.send_empty_msg();
  if (cfg_.pid_p > 0)
  {
    comms_.set_pid_values(cfg_.pid_p,cfg_.pid_d,cfg_.pid_i,cfg_.pid_o);
    RCLCPP_INFO(rclcpp::get_logger("BotHardwareSystem"), "Updating PID..");
  }
  comms_.reset_encoders();
  RCLCPP_INFO(rclcpp::get_logger("BotHardwareSystem"), "Encoders resetted!");
  RCLCPP_INFO(rclcpp::get_logger("BotHardwareSystem"), "Successfully activated!");

  return hardware_interface::CallbackReturn::SUCCESS;
}

hardware_interface::CallbackReturn BotHardwareSystem::on_deactivate(
  const rclcpp_lifecycle::State & /*previous_state*/)
{
  if (comms_.connected())
  {
    comms_.clearbuffs();
    comms_.send_empty_msg();
    comms_.disconnect();
  }
  RCLCPP_INFO(rclcpp::get_logger("BotHardwareSystem"), "Deactivating ...please wait...");
  RCLCPP_INFO(rclcpp::get_logger("BotHardwareSystem"), "Successfully deactivated!");

  return hardware_interface::CallbackReturn::SUCCESS;
}

hardware_interface::return_type BotHardwareSystem::read(
  const rclcpp::Time & /*time*/, const rclcpp::Duration & period)
{
  if (!comms_.connected())
  {
    RCLCPP_INFO(rclcpp::get_logger("BotHardwareSystem"), "notconnected");
    return hardware_interface::return_type::ERROR;
  }

  comms_.read_encoders(wheel_l_.enc, wheel_r_.enc);
  
  // RCLCPP_INFO(rclcpp::get_logger("BotHardwareSystem"), "LeftE: %d, RightE: %d", wheel_l_.enc, wheel_r_.enc);
  // RCLCPP_INFO(rclcpp::get_logger("BotHardwareSystem"), "LeftV: %f, RightV: %f", wheel_l_.vel, wheel_r_.vel);
  // if( (wheel_l_.enc >= 10000000 && wheel_l_.enc % wheel_l_.rads_per_count == 0) &&
  //     (wheel_r_.enc >= 10000000 && wheel_r_.enc % wheel_r_.rads_per_count == 0) ){
  //       comms_.reset_encoders();
  // }

  double pos_prev_l = wheel_l_.pos;
  double pos_prev_r = wheel_r_.pos;
  double delta_seconds = period.seconds();

  pos_prev_l = wheel_l_.pos;
  wheel_l_.pos = wheel_l_.calc_enc_angle();
  wheel_l_.vel = (wheel_l_.pos - pos_prev_l) / delta_seconds;

  pos_prev_r = wheel_r_.pos;
  wheel_r_.pos = wheel_r_.calc_enc_angle();
  wheel_r_.vel = (wheel_r_.pos - pos_prev_r) / delta_seconds;

  // if(wheel_l_.enc >= 90000000 || wheel_r_.enc>= 90000000) comms_.reset_encoders(); //developmental feature

  comms_.read_imu_sensor( imu_.linear_acceleration_x, imu_.linear_acceleration_y, imu_.linear_acceleration_z, 
                          imu_.angular_velocity_x, imu_.angular_velocity_y, imu_.angular_velocity_z);
  // RCLCPP_INFO(rclcpp::get_logger("BotHardwareSystem"), "x: %f, z: %f", imu_.linear_acceleration_x, imu_.angular_velocity_z);
  // comms_.read_range_sensors(range_l_.range, range_r_.range);

  // RCLCPP_INFO(rclcpp::get_logger("BotHardwareSystem"), "Successfully reading!");

  return hardware_interface::return_type::OK;
}

hardware_interface::return_type NewHardwareInterface::BotHardwareSystem::write(
  const rclcpp::Time & /*time*/, const rclcpp::Duration & /*period*/)
{
  if (!comms_.connected())
  {
    RCLCPP_INFO(rclcpp::get_logger("BotHardwareSystem"), "notconnected");
    return hardware_interface::return_type::ERROR;
  }

  int motor_l_counts_per_loop = wheel_l_.cmd / wheel_l_.rads_per_count / cfg_.loop_rate;
  int motor_r_counts_per_loop = wheel_r_.cmd / wheel_r_.rads_per_count / cfg_.loop_rate;
  comms_.set_motor_values(motor_l_counts_per_loop, motor_r_counts_per_loop);
  // if (motor_l_counts_per_loop != 0 || motor_r_counts_per_loop != 0){
  //   RCLCPP_INFO(rclcpp::get_logger("BotHardwareSystem"), "Lcmd: %f rads: %f rate: %f", wheel_l_.cmd, wheel_l_.rads_per_count, cfg_.loop_rate);
  // RCLCPP_INFO(rclcpp::get_logger("BotHardwareSystem"), "Left wheel: %d Right wheel: %d", motor_l_counts_per_loop, motor_r_counts_per_loop);
  // }
  // comms_.run_motor_pwm(20, 20);
  // RCLCPP_INFO(rclcpp::get_logger("BotHardwareSystem"), "Successfully writing!");

  return hardware_interface::return_type::OK;
}

}

#include "pluginlib/class_list_macros.hpp"
PLUGINLIB_EXPORT_CLASS(NewHardwareInterface::BotHardwareSystem, hardware_interface::SystemInterface)
