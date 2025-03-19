// Copyright 2016 Open Source Robotics Foundation, Inc.
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

#include <chrono>
#include <memory>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"


#include <iostream>
#include <sys/types.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <string.h>
#include <string>

#include <signal.h> // for ctrl + C

using namespace std;
// mspm

using namespace std::chrono_literals;

class ServerPub : public rclcpp::Node
{
  public:
    ServerPub()
    : Node("bot_server")
    {
      publisher_ = this->create_publisher<std_msgs::msg::String>("server_cmd", 10);
      auto message = std_msgs::msg::String();

      cout << "Beginning..." << endl;
      int listening = socket(AF_INET, SOCK_STREAM, 0);

      if (listening == -1)
      {
          cerr << "Can't create a socket! Quitting" << endl;
          rclcpp::shutdown();
      }
      cout << "Socket created..." << endl;

      // Bind the ip address and port to a socket
      sockaddr_in hint;
      hint.sin_family = AF_INET;
      hint.sin_port = htons(8888);
      hint.sin_addr.s_addr = INADDR_ANY;
      // inet_pton(AF_INET, "0.0.0.0", &hint.sin_addr);
      cout << "Socket Binded..." << endl;

      // listen to any IP address 
      bind(listening, (sockaddr*)&hint, sizeof(hint));

      cout << "Getting IPs..." << endl;
      // Tell Winsock the socket is for listening
      listen(listening, SOMAXCONN);
      cout << "Listening to IPs..." << endl;

      // Close listening socket
      // close(listening);
    
      // While loop: accept and echo message back to client
      char buf[4096];

      // Wait for a connection
      // cout << "Waiting..." << endl;
      sockaddr_in client;
      socklen_t clientSize = sizeof(client);

      int clientSocket = accept(listening, (sockaddr*)&client, &clientSize);
      // cout << "Client Connected..." << endl;

      cout << "RCL started..." << endl;
      while (true)
        {
          cout << "Loop Entered..." << endl;
            memset(buf, 0, 4096);
    
            // Wait for client to send data
            int bytesReceived = recv(clientSocket, buf, 4096, 0);
            if (bytesReceived == -1)
            {
                cout << "Error in recv(). Quitting" << endl;
                RCLCPP_INFO(this->get_logger(), "err recv");
                break;
                close(clientSocket);
                sockaddr_in client;
                socklen_t clientSize = sizeof(client);

                clientSocket = accept(listening, (sockaddr*)&client, &clientSize);
            }
    
            if (bytesReceived == 0)
            {
                cout << "Client disconnected " << endl;
                RCLCPP_INFO(this->get_logger(), "cli dis");
                // break;
                close(clientSocket);
                sockaddr_in client;
                socklen_t clientSize = sizeof(client);

                clientSocket = accept(listening, (sockaddr*)&client, &clientSize);
            }
            message.data = buf;        
            RCLCPP_INFO(this->get_logger(), "Publishing: '%s'", message.data.c_str());
            // RCLCPP_INFO(node->get_logger(), buf);
            publisher_->publish(message);
            
            // Echo message back to client
            // send(clientSocket, buf, bytesReceived + 1, 0);
            // if

            // Register signal and signal handler
            signal(SIGINT, signal_callback_handler);
        }
    }

      void static signal_callback_handler(int signum) {
        cout << "server shutting down..." << signum << endl;
        // RCLCPP_INFO(->get_logger(), "server shutting down...");
        // Terminate program
        // exit(signum);
        rclcpp::shutdown();
      }

    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;

    
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<ServerPub>());
  rclcpp::shutdown();
  return 0;
}
