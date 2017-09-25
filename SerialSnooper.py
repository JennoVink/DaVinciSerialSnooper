import serial
import serial.tools.list_ports

import ctypes

import win32api
import win32con
import time
import threading


class DataReader:
    # config / callibration variables
    def __init__(self):
        self.thrG = 40.0
        self.thrA = 0.05
        self.accellOffset = 0.0
        self.state = -1
        self.lastInput = None
        self.enabled = True

        SendInput = ctypes.windll.user32.SendInput

        self.ser = None
        try:
            comPort = None

            ports = list(serial.tools.list_ports.comports())
            if len(ports) == 0:
                print('There are no com ports available')
                raise Exception('There are no com ports available')

            if len(ports) == 1:
                print('1 comport found: ', ports[0])
                comPort = ports[0].device

            for p in ports:
                # todo: add to a listbox
                # print(p.description)
                pass

            self.ser = serial.Serial(comPort, baudrate=115200, timeout=0.01)
        except Exception:
            print('Something is wrong with the COM-port.')
            return

        t = threading.Thread(target=self.startLoop)
        t.start()

    def setAccellOffset(self, value):
        if self.lastInput == None:
            print('There is no input generated at all by the sensor... Exiting')
            return

        gForceZ = 0.0
        rotY = 0.0
        try:
            gForceZ = float(self.lastInput[0])
            rotY = float(self.lastInput[1][:-3])
            self.state = 2
        except:
            return

        self.accellOffset = rotY
        print(self.accellOffset)

    def updateState(self):
        if not self.enabled:
            return

        data = self.ser.readline().decode('ascii').split('X')
        if len(data) == 1:
            return

        print(data)
        self.lastInput = data

        gForceZ = 0.0
        rotY = 0.0
        try:
            gForceZ = float(data[0])
            rotY = float(data[1][:-3])
        except:
            return

        if rotY > self.thrG and gForceZ < -self.thrA and self.state != 0:
            self.state = 0
            print("Q")


        if rotY < - self.thrG and gForceZ > self.thrA and self.state != 1:
            self.state = 1
            print("E")


        if abs(gForceZ - self.accellOffset) < self.thrA and self.state != 2:
            self.state = 2
            win32api.keybd_event(0x25, 0, win32con.KEYEVENTF_KEYUP, 0)
            win32api.keybd_event(0x27, 0, win32con.KEYEVENTF_KEYUP, 0)
            print("N")


    def startLoop(self):
        print('hello from startloop :)')
        time.sleep(3)

        while 1:
            if self.state is 0:
                win32api.keybd_event(0x25, 0, 0, 0)
                # win32api.keybd_evenat(0x25, 0, win32con.KEYEVENTF_KEYUP, 0)
            if self.state is 1:
                win32api.keybd_event(0x27, 0, 0, 0)
                # win32api.keybd_event(0x27, 0, win32con.KEYEVENTF_KEYUP, 0)
            self.updateState()

    def updateSensitivity(self, value):
        self.thrG = value

    def toggleEnabledButton(self):
        self.enabled = not self.enabled
        win32api.keybd_event(0x25, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(0x27, 0, win32con.KEYEVENTF_KEYUP, 0)
        print(self.enabled)