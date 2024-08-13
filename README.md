# About the project
This project involves Automatic Number Plate Recognition (ANPR) with the help of Optical Character Recognition (OCR) and object detection algorithms through OpenCV. The project utilizes an [Express](https://expressjs.com/) web server as a secure admin interface and control panel. This system can be used in a private parking as access control combined with a barrier or as a passive surveillance system.

## Install and setup
```
chmod +x setup.sh
./setup.sh
```
### License plate isolation and recognition
![img](https://i.imgur.com/y6yFTtw_d.webp?maxwidth=360&fidelity=grand)

## Libraries and Frameworks
* [OpenCV](https://opencv.org/) - Video feed processing
* [HAAR Cascade Classifier](https://docs.opencv.org/3.4/db/d28/tutorial_cascade_classifier.html) - License plate isolation
* [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) - Extracting text from license plates
* [SQLite](https://www.sqlite.org/) - Database access
* [Express](https://expressjs.com/), [NodeJS](https://nodejs.org/en) - Web server
* [SocketIO](https://socket.io/) - Live camera feed to web server
* [BCrypt](https://www.npmjs.com/package/bcrypt) - Password hashing

## Work modes
##### As of now there are two main work modes.
###### Change modes in `config.py` 
* `Active` mode opens the barrier only to authorized vehicles
* `Passive` mode monitors passing traffic leaving the barrier open for any vehicle
