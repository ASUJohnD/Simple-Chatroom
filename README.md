# Simple Chatroom
This program is a networking CLI application that is similar to the social media app "Twitter" and was made for the ASU networking class to demonstrate the utility of Sockets in applications. This application is also known as "Tweeter" or "Socket Project" and more information about the implementation can be found in the Socket-Project PDF file. The main purpose of this project is to create a server (tracker.py) which would be able to communicate to several different clients (user.py) from different IP addresses and would allow tweets to propogate from one user to several. Each user would also have a unique handle (ex: @user) which they would use for the given commands such as "follow" or "tweet".

## Demonstration
The video demonstrations below show how to use the application with the different commands.

### First Implementation
The video below shows the commands "register", "follow", "drop", "exit", and "query handles".

[![video](https://img.youtube.com/vi/BhuDkGbBUnk/hqdefault.jpg)](https://www.youtube.com/watch?v=BhuDkGbBUnk)

### Final Implementation
The video below shows the "tweet" command and the logical rings that allow the users to tweet only to the users following them. It also shows the clients initializing three ports (left, middle, right) for the server which are used in the logical rings.

[![video](https://img.youtube.com/vi/LR7CfPxcLtA/hqdefault.jpg)](https://www.youtube.com/watch?v=LR7CfPxcLtA)

## Installation
This program only uses the python source files in the project as well as the python libraries "sys", "socket", "threading", "queue", and "json". Only python/python3 is needed to run the source files so a standard terminal would be able to run the project.

## Usage
The application requires that both the tracker.py and user.py files are running and there should be at least 2 user.py instances as this would show the full functionality of the application. 

First, run tracker.py and user.py. Ideally, these would be on different systems with different IP addresses but it's fine to have them on the same system.
```bash
python3 tracker.py
python3 user.py
```

Second, run another user.py instance on another system. This can also be achieved by SSHing into another system on the system with the already running programs.
```bash
python3 user.py
```

Now, the register command would need to be used on the user applications to communicate to the tracker.py (server). Ensure the ports are different amongst users.
```bash
register [@user_handle] [IP_address] [left_Port] [middle_port] [right_port]
```

All other commands are referenced in the Socket Project PDF and the video demonstrations above.

## License
Simple Chatroom/Tweeter is licensed under the [MIT LICENSE](LICENSE).