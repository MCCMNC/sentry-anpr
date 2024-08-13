import serial
import time
from serial.tools import list_ports

class ArduinoConnection:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ArduinoConnection, cls).__new__(cls)
            cls._instance.arduino_port = cls._instance.find_arduino_port("ttyACM0")
            cls._instance.ser = None
            cls._instance.connected = False 
            cls._instance.connect()
        return cls._instance
    
    def __init__(self, descr="ttyACM0"):
        if self._instance is not None:
            return
        self._instance = self
        self.arduino_port = self.find_arduino_port(descr)
        self.ser = None
        self.connected = False
        self.connect()
        print("Connecting to arduino NOW")

    def find_arduino_port(self, descr):
        arduino_ports = []
        ports = list_ports.comports()
        for port in ports:
            if descr in port.description: 
                arduino_ports.append(port.device)

        if len(arduino_ports) == 0:
            print("No Arduino found.")
            return False
        elif len(arduino_ports) >= 1:
            return arduino_ports[0]

    def connect(self):
        if not self.arduino_port:
            return False

        try:
            self.ser = serial.Serial(self.arduino_port, 9600, timeout=1)
            self.connected = True
            print("Connected to Arduino on port:", self.arduino_port)
            return True
        except Exception as e:
            print("[SERIALErr] Failed to connect to Arduino:", e)
            return False

    def disconnect(self):
        if self.connected:
            self.ser.close()
            self.connected = False

    def send_command(self, command):
        if not self.connected:
            return False

        self.ser.write(bytes(command, 'utf-8'))
        time.sleep(0.1)
        return True
