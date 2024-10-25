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

<<<<<<< HEAD
#include "diffdrive_arduino/diffbot_system.hpp"
=======
#include "include/diffbot_system/diffbot_system.hpp"
>>>>>>> 74202b1cace1109667ff679b0efbdeccca8b2b9a

#include <chrono>
#include <cmath>
#include <limits>
#include <memory>
#include <vector>

#include "hardware_interface/types/hardware_interface_type_values.hpp"
#include "rclcpp/rclcpp.hpp"

<<<<<<< HEAD
namespace diffdrive_arduino
{
hardware_interface::CallbackReturn DiffDriveArduinoHardware::on_init(
=======
namespace NewHardwareInterface
{
hardware_interface::CallbackReturn DiffBotHardwareSystem::on_init(
>>>>>>> 74202b1cace1109667ff679b0efbdeccca8b2b9a
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
  if (info_.hardware_parameters.count("pid_p") > 0)
  {
    cfg_.pid_p = std::stoi(info_.hardware_parameters["pid_p"]);
    cfg_.pid_d = std::stoi(info_.hardware_parameters["pid_d"]);
    cfg_.pid_i = std::stoi(info_.hardware_parameters["pid_i"]);
    cfg_.pid_o = std::stoi(info_.hardware_parameters["pid_o"]);
  }
  else
  {
<<<<<<< HEAD
    RCLCPP_INFO(rclcpp::get_logger("DiffDriveArduinoHardware"), "PID values not supplied, using defaults.");
=======
    RCLCPP_INFO(rclcpp::get_logger("DiffBotHardwareSystem"), "PID values not supplied, using defaults.");
>>>>>>> 74202b1cace1109667ff679b0efbdeccca8b2b9a
  }
  

  wheel_l_.setup(cfg_.left_wheel_name, cfg_.enc_counts_per_rev);
  wheel_r_.setup(cfg_.right_wheel_name, cfg_.enc_counts_per_rev);


  for (const hardware_interface::ComponentInfo & joint : info_.joints)
  {
    // DiffBotSystem has exactly two states and one command interface on each joint
    if (joint.command_interfaces.size() != 1)
    {
      RCLCPP_FATAL(
<<<<<<< HEAD
        rclcpp::get_logger("DiffDriveArduinoHardware"),
=======
        rclcpp::get_logger("DiffBotHardwareSystem"),
>>>>>>> 74202b1cace1109667ff679b0efbdeccca8b2b9a
        "Joint '%s' has %zu command interfaces found. 1 expected.", joint.name.c_str(),
        joint.command_interfaces.size());
      return hardware_interface::CallbackReturn::ERROR;
    }

    if (joint.command_interfaces[0].name != hardware_interface::HW_IF_VELOCITY)
    {
      RCLCPP_FATAL(
<<<<<<< HEAD
        rclcpp::get_logger("DiffDriveArduinoHardware"),
=======
        rclcpp::get_logger("DiffBotHardwareSystem"),
>>>>>>> 74202b1cace1109667ff679b0efbdeccca8b2b9a
        "Joint '%s' have %s command interfaces found. '%s' expected.", joint.name.c_str(),
        joint.command_interfaces[0].name.c_str(), hardware_interface::HW_IF_VELOCITY);
      return hardware_interface::CallbackReturn::ERROR;
    }

    if (joint.state_interfaces.size() != 2)
    {
      RCLCPP_FATAL(
<<<<<<< HEAD
        rclcpp::get_logger("DiffDriveArduinoHardware"),
=======
        rclcpp::get_logger("DiffBotHardwareSystem"),
>>>>>>> 74202b1cace1109667ff679b0efbdeccca8b2b9a
        "Joint '%s' has %zu state interface. 2 expected.", joint.name.c_str(),
        joint.state_interfaces.size());
      return hardware_interface::CallbackReturn::ERROR;
    }

    if (joint.state_interfaces[0].name != hardware_interface::HW_IF_POSITION)
    {
      RCLCPP_FATAL(
<<<<<<< HEAD
        rclcpp::get_logger("DiffDriveArduinoHardware"),
=======
        rclcpp::get_logger("DiffBotHardwareSystem"),
>>>>>>> 74202b1cace1109667ff679b0efbdeccca8b2b9a
        "Joint '%s' have '%s' as first state interface. '%s' expected.", joint.name.c_str(),
        joint.state_interfaces[0].name.c_str(), hardware_interface::HW_IF_POSITION);
      return hardware_interface::CallbackReturn::ERROR;
    }

    if (joint.state_interfaces[1].name != hardware_interface::HW_IF_VELOCITY)
    {
      RCLCPP_FATAL(
<<<<<<< HEAD
        rclcpp::get_logger("DiffDriveArduinoHardware"),
=======
        rclcpp::get_logger("DiffBotHardwareSystem"),
>>>>>>> 74202b1cace1109667ff679b0efbdeccca8b2b9a
        "Joint '%s' have '%s' as second state interface. '%s' expected.", joint.name.c_str(),
        joint.state_interfaces[1].name.c_str(), hardware_interface::HW_IF_VELOCITY);
      return hardware_interface::CallbackReturn::ERROR;
    }
  }

  return hardware_interface::CallbackReturn::SUCCESS;
}

<<<<<<< HEAD
std::vector<hardware_interface::StateInterface> DiffDriveArduinoHardware::export_state_interfaces()
=======
std::vector<hardware_interface::StateInterface> DiffBotHardwareSystem::export_state_interfaces()
>>>>>>> 74202b1cace1109667ff679b0efbdeccca8b2b9a
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

  return state_interfaces;
}

<<<<<<< HEAD
std::vector<hardware_interface::CommandInterface> DiffDriveArduinoHardware::export_command_interfaces()
=======
std::vector<hardware_interface::CommandInterface> DiffBotHardwareSystem::export_command_interfaces()
>>>>>>> 74202b1cace1109667ff679b0efbdeccca8b2b9a
{
  std::vector<hardware_interface::CommandInterface> command_interfaces;

  command_interfaces.emplace_back(hardware_interface::CommandInterface(
    wheel_l_.name, hardware_interface::HW_IF_VELOCITY, &wheel_l_.cmd));

  command_interfaces.emplace_back(hardware_interface::CommandInterface(
    wheel_r_.name, hardware_interface::HW_IF_VELOCITY, &wheel_r_.cmd));

  return command_interfaces;
}

<<<<<<< HEAD
hardware_interface::CallbackReturn DiffDriveArduinoHardware::on_configure(
  const rclcpp_lifecycle::State & /*previous_state*/)
{
  RCLCPP_INFO(rclcpp::get_logger("DiffDriveArduinoHardware"), "Configuring ...please wait...");
=======
hardware_interface::CallbackReturn DiffBotHardwareSystem::on_configure(
  const rclcpp_lifecycle::State & /*previous_state*/)
{
  RCLCPP_INFO(rclcpp::get_logger("DiffBotHardwareSystem"), "Configuring ...please wait...");
>>>>>>> 74202b1cace1109667ff679b0efbdeccca8b2b9a
  if (comms_.connected())
  {
    comms_.disconnect();
  }
  comms_.connect(cfg_.device, cfg_.baud_rate, cfg_.timeout_ms);
<<<<<<< HEAD
  RCLCPP_INFO(rclcpp::get_logger("DiffDriveArduinoHardware"), "Successfully configured!");
=======
  RCLCPP_INFO(rclcpp::get_logger("DiffBotHardwareSystem"), "Successfully configured!");
>>>>>>> 74202b1cace1109667ff679b0efbdeccca8b2b9a

  return hardware_interface::CallbackReturn::SUCCESS;
}

<<<<<<< HEAD
hardware_interface::CallbackReturn DiffDriveArduinoHardware::on_cleanup(
  const rclcpp_lifecycle::State & /*previous_state*/)
{
  RCLCPP_INFO(rclcpp::get_logger("DiffDriveArduinoHardware"), "Cleaning up ...please wait...");
=======
hardware_interface::CallbackReturn DiffBotHardwareSystem::on_cleanup(
  const rclcpp_lifecycle::State & /*previous_state*/)
{
  RCLCPP_INFO(rclcpp::get_logger("DiffBotHardwareSystem"), "Cleaning up ...please wait...");
>>>>>>> 74202b1cace1109667ff679b0efbdeccca8b2b9a
  if (comms_.connected())
  {
    comms_.disconnect();
  }
<<<<<<< HEAD
  RCLCPP_INFO(rclcpp::get_logger("DiffDriveArduinoHardware"), "Successfully cleaned up!");
=======
  RCLCPP_INFO(rclcpp::get_logger("DiffBotHardwareSystem"), "Successfully cleaned up!");
>>>>>>> 74202b1cace1109667ff679b0efbdeccca8b2b9a

  return hardware_interface::CallbackReturn::SUCCESS;
}


<<<<<<< HEAD
hardware_interface::CallbackReturn DiffDriveArduinoHardware::on_activate(
  const rclcpp_lifecycle::State & /*previous_state*/)
{
  RCLCPP_INFO(rclcpp::get_logger("DiffDriveArduinoHardware"), "Activating ...please wait...");
=======
hardware_interface::CallbackReturn DiffBotHardwareSystem::on_activate(
  const rclcpp_lifecycle::State & /*previous_state*/)
{
  RCLCPP_INFO(rclcpp::get_logger("DiffBotHardwareSystem"), "Activating ...please wait...");
>>>>>>> 74202b1cace1109667ff679b0efbdeccca8b2b9a
  if (!comms_.connected())
  {
    return hardware_interface::CallbackReturn::ERROR;
  }
  if (cfg_.pid_p > 0)
  {
    comms_.set_pid_values(cfg_.pid_p,cfg_.pid_d,cfg_.pid_i,cfg_.pid_o);
  }
<<<<<<< HEAD
  RCLCPP_INFO(rclcpp::get_logger("DiffDriveArduinoHardware"), "Successfully activated!");
=======
  RCLCPP_INFO(rclcpp::get_logger("DiffBotHardwareSystem"), "Successfully activated!");
>>>>>>> 74202b1cace1109667ff679b0efbdeccca8b2b9a

  return hardware_interface::CallbackReturn::SUCCESS;
}

<<<<<<< HEAD
hardware_interface::CallbackReturn DiffDriveArduinoHardware::on_deactivate(
  const rclcpp_lifecycle::State & /*previous_state*/)
{
  RCLCPP_INFO(rclcpp::get_logger("DiffDriveArduinoHardware"), "Deactivating ...please wait...");
  RCLCPP_INFO(rclcpp::get_logger("DiffDriveArduinoHardware"), "Successfully deactivated!");
=======
hardware_interface::CallbackReturn DiffBotHardwareSystem::on_deactivate(
  const rclcpp_lifecycle::State & /*previous_state*/)
{
  RCLCPP_INFO(rclcpp::get_logger("DiffBotHardwareSystem"), "Deactivating ...please wait...");
  RCLCPP_INFO(rclcpp::get_logger("DiffBotHardwareSystem"), "Successfully deactivated!");
>>>>>>> 74202b1cace1109667ff679b0efbdeccca8b2b9a

  return hardware_interface::CallbackReturn::SUCCESS;
}

<<<<<<< HEAD
hardware_interface::return_type DiffDriveArduinoHardware::read(
=======
hardware_interface::return_type DiffBotHardwareSystem::read(
>>>>>>> 74202b1cace1109667ff679b0efbdeccca8b2b9a
  const rclcpp::Time & /*time*/, const rclcpp::Duration & period)
{
  if (!comms_.connected())
  {
    return hardware_interface::return_type::ERROR;
  }

  comms_.read_encoder_values(wheel_l_.enc, wheel_r_.enc);

  double delta_seconds = period.seconds();

  double pos_prev = wheel_l_.pos;
  wheel_l_.pos = wheel_l_.calc_enc_angle();
  wheel_l_.vel = (wheel_l_.pos - pos_prev) / delta_seconds;

  pos_prev = wheel_r_.pos;
  wheel_r_.pos = wheel_r_.calc_enc_angle();
  wheel_r_.vel = (wheel_r_.pos - pos_prev) / delta_seconds;

  return hardware_interface::return_type::OK;
}

<<<<<<< HEAD
hardware_interface::return_type diffdrive_arduino ::DiffDriveArduinoHardware::write(
=======
hardware_interface::return_type NewHardwareInterface::DiffBotHardwareSystem::write(
>>>>>>> 74202b1cace1109667ff679b0efbdeccca8b2b9a
  const rclcpp::Time & /*time*/, const rclcpp::Duration & /*period*/)
{
  if (!comms_.connected())
  {
    return hardware_interface::return_type::ERROR;
  }

  int motor_l_counts_per_loop = wheel_l_.cmd / wheel_l_.rads_per_count / cfg_.loop_rate;
  int motor_r_counts_per_loop = wheel_r_.cmd / wheel_r_.rads_per_count / cfg_.loop_rate;
  comms_.set_motor_values(motor_l_counts_per_loop, motor_r_counts_per_loop);
  return hardware_interface::return_type::OK;
}

}  // namespace diffdrive_arduino

#include "pluginlib/class_list_macros.hpp"
<<<<<<< HEAD
PLUGINLIB_EXPORT_CLASS(
  diffdrive_arduino::DiffDriveArduinoHardware, hardware_interface::SystemInterface)
=======
PLUGINLIB_EXPORT_CLASS(NewHardwareInterface::DiffBotHardwareSystem, hardware_interface::SystemInterface)
>>>>>>> 74202b1cace1109667ff679b0efbdeccca8b2b9a
