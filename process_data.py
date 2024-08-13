from config import *
from ocrmodel import paddle_ocr
import datetime
import time
from dbinterface import DBInterface
from arduino_interface import ArduinoConnection
import re

def drawLine(blow):
    height, width, _ = blow.shape

    line_y = height*3//4

    start_line = (0, line_y)
    end_line = (100, line_y)

    start_line_2 = (width-100, line_y)
    end_line_2 = (width, line_y)

    blow = cv2.line(blow, start_line, end_line, (0,255,255), 2)
    blow = cv2.line(blow, start_line_2, end_line_2, (0,255,255), 2)
    
    return blow

def process_plate(frame, plate_img, x,y):
    global previous_plate

    plate_text = paddle_ocr(plate_img)
    if plate_text == "LPR01":
        return 0

    frame = drawLine(frame)
    sanitized_plate = re.sub(r'[^a-zA-Z0-9]', '', plate_text)

    if plate_text != sanitized_plate:
        print(f"[FILTER] Plate: {sanitized_plate}")
    else:
        print(f"Plate: {sanitized_plate}")

    cv2.putText(frame, sanitized_plate, (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

    saveFrame(frame, sanitized_plate)
    previous_plate = sanitized_plate

def saveFrame(frame, sanitized_plate):
    db = DBInterface(db_name="vehicles.db")

    filename = f"db_caught/{sanitized_plate}_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png"
    null_plate_filename = f"db_caught/null_plate/{sanitized_plate}_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png"

    if len(sanitized_plate) >= 6:
        cv2.imwrite(filename, frame)
        print(f"{sanitized_plate} --> {filename}")
        write_to_db(sanitized_plate, filename)

    elif len(sanitized_plate) > 0:
        cv2.imwrite(null_plate_filename, frame)
        print(f"{sanitized_plate} --> {null_plate_filename}")
        write_to_db(sanitized_plate, null_plate_filename)
    
    if checkPrivilige(sanitized_plate) and sysmode == "active":
        print(sanitized_plate, "ON WHITELIST!")
        activatePhysicalInterfaces()

def write_to_db(plate, img_dir):
    db = DBInterface(db_name="vehicles.db")
    sql_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    db.insert("history", ["regnum", "passing_date", "sysmode", "image"], [plate, sql_date, sysmode, img_dir])
    print("Function write_to_db() successfully called.")

def checkPrivilige(sanitized_plate):
    db = DBInterface(db_name="vehicles.db")
    query = db.select(f'SELECT COUNT(*) FROM whitelist WHERE regnum = "{sanitized_plate}"')
    query = int((query[0])[0])

    return (True if query > 0 else False)

def checkPreviousPlate():
    db = DBInterface(db_name="vehicles.db")
    query = db.select(f'SELECT ')

def activatePhysicalInterfaces():
    arduino_connection = ArduinoConnection()
    time.sleep(2)
    arduino_connection.send_command("SIGOPEN")
    time.sleep(10)
    arduino_connection.send_command("SIGCLOSE")
    time.sleep(1)
