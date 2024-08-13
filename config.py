import csv

lpr = { # DO NOT WRITE HERE
    "username":     "",
    "password":     "",
    "ip_addr":      "",
}

with open("camera.csv", mode='r', newline='') as file:
    reader = csv.reader(file)
    for i, row in enumerate(reader):
        if i == 1:
            lpr["username"] = row[0]
            lpr["ip_addr"] = row[1]
            lpr["password"] = row[2]
            print(f'Camera set by config with IP {lpr["ip_addr"]}')
            break

motion_level = None
sysmode = ['passive','active'][1] # 0 - passive | 1 - active / barrier mode
active_socket = True

import cv2
import numpy as np
import paddleocr
import socketio

ocrp = paddleocr.PaddleOCR(show_log=False, use_angle_cls=True, lang='en')
stream = cv2.VideoCapture(f'rtsp://{lpr["username"]}:{lpr["password"]}@{lpr["ip_addr"]}/')
#stream = cv2.VideoCapture("./sample_content/video_for_testing.mp4")
plate_cascade = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')

sio = socketio.Client()

if active_socket:
    try:
        sio.connect('http://localhost:681')   
    except Exception as e:
        print("[SOCKET Err]", e, "\nContinuing without SOCKET.")
        active_socket = False