import cv2
import numpy as np
import threading
import time
import base64
from config import *
from process_data import process_plate, drawLine
from arduino_interface import ArduinoConnection

try:
    dummy_connection = ArduinoConnection()
    time.sleep(5)

    if sysmode == "passive":
        print("PASSIVE MODE ON")
        arduino_connection.send_command("SIGOPEN")
        time.sleep(2)
except Exception as e:
    print("[SerialErr]", e)


def send_frame_SOCK(frame):
    if active_socket:
        _, encoded_frame = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 60])

        frame_bytes = encoded_frame.tobytes()
        base64_frame = base64.b64encode(frame_bytes)
        binary_frame = encoded_frame.tobytes()
        sio.emit('frame', binary_frame)

ocr_thread = None
previous_plate = None

def cap_frame():
    frame = None
    ret, frame = stream.read()
    if ret:
        return frame
    else:
        print("Error loading RTSP stream.")

def process():
    global ocr_thread

    while True:
        frame = cap_frame()
        if frame is None:
            break
        height, width, _ = frame.shape

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        for (x, y, w, h) in plates:
            if y > height*1//5: #and y < height*3//4+100:
                frame = drawLine(frame)
                plate = gray[y:y+h, x:x+w]
                cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), 1)

                if not (ocr_thread and ocr_thread.is_alive()):
                    ocr_thread = threading.Thread(target=process_plate, args=(frame, plate, x, y))
                    ocr_thread.start()
                else:
                    print(".", end="")
                cv2.putText(frame, "DET", (20,height-20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

        #frame = cv2.resize(frame, (width // 2, height // 2)) # speed 

        send_frame_SOCK(cv2.resize(frame, (width // 2, height // 2)))

        cv2.namedWindow("LPR01 Live", cv2.WINDOW_KEEPRATIO)
        cv2.imshow("LPR01 Live", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

process()

if __name__ == "__main__":
    ocr_thread = None
    print("Exiting...")
    sio.disconnect()
    stream.release()
    cv2.destroyAllWindows()