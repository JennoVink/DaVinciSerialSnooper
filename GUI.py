import kivy
kivy.require('1.0.6') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown

import serial
import serial.tools.list_ports

import ctypes

import win32api
import win32con
import time
import threading

class MainScreen(GridLayout):

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.dataReader = DataReader()

        self.VK_CODE = {'backspace': 0x08,
                   'tab': 0x09,
                   'clear': 0x0C,
                   'enter': 0x0D,
                   'shift': 0x10,
                   'ctrl': 0x11,
                   'alt': 0x12,
                   'pause': 0x13,
                   'caps_lock': 0x14,
                   'esc': 0x1B,
                   'spacebar': 0x20,
                   'page_up': 0x21,
                   'page_down': 0x22,
                   'end': 0x23,
                   'home': 0x24,
                   'left_arrow': 0x25,
                   'up_arrow': 0x26,
                   'right_arrow': 0x27,
                   'down_arrow': 0x28,
                   'select': 0x29,
                   'print': 0x2A,
                   'execute': 0x2B,
                   'print_screen': 0x2C,
                   'ins': 0x2D,
                   'del': 0x2E,
                   'help': 0x2F,
                   '0': 0x30,
                   '1': 0x31,
                   '2': 0x32,
                   '3': 0x33,
                   '4': 0x34,
                   '5': 0x35,
                   '6': 0x36,
                   '7': 0x37,
                   '8': 0x38,
                   '9': 0x39,
                   'a': 0x41,
                   'b': 0x42,
                   'c': 0x43,
                   'd': 0x44,
                   'e': 0x45,
                   'f': 0x46,
                   'g': 0x47,
                   'h': 0x48,
                   'i': 0x49,
                   'j': 0x4A,
                   'k': 0x4B,
                   'l': 0x4C,
                   'm': 0x4D,
                   'n': 0x4E,
                   'o': 0x4F,
                   'p': 0x50,
                   'q': 0x51,
                   'r': 0x52,
                   's': 0x53,
                   't': 0x54,
                   'u': 0x55,
                   'v': 0x56,
                   'w': 0x57,
                   'x': 0x58,
                   'y': 0x59,
                   'z': 0x5A,
                   'numpad_0': 0x60,
                   'numpad_1': 0x61,
                   'numpad_2': 0x62,
                   'numpad_3': 0x63,
                   'numpad_4': 0x64,
                   'numpad_5': 0x65,
                   'numpad_6': 0x66,
                   'numpad_7': 0x67,
                   'numpad_8': 0x68,
                   'numpad_9': 0x69,
                   'multiply_key': 0x6A,
                   'add_key': 0x6B,
                   'separator_key': 0x6C,
                   'subtract_key': 0x6D,
                   'decimal_key': 0x6E,
                   'divide_key': 0x6F,
                   'F1': 0x70,
                   'F2': 0x71,
                   'F3': 0x72,
                   'F4': 0x73,
                   'F5': 0x74,
                   'F6': 0x75,
                   'F7': 0x76,
                   'F8': 0x77,
                   'F9': 0x78,
                   'F10': 0x79,
                   'F11': 0x7A,
                   'F12': 0x7B,
                   'F13': 0x7C,
                   'F14': 0x7D,
                   'F15': 0x7E,
                   'F16': 0x7F,
                   'F17': 0x80,
                   'F18': 0x81,
                   'F19': 0x82,
                   'F20': 0x83,
                   'F21': 0x84,
                   'F22': 0x85,
                   'F23': 0x86,
                   'F24': 0x87,
                   'num_lock': 0x90,
                   'scroll_lock': 0x91,
                   'left_shift': 0xA0,
                   'right_shift ': 0xA1,
                   'left_control': 0xA2,
                   'right_control': 0xA3,
                   'left_menu': 0xA4,
                   'right_menu': 0xA5,
                   'browser_back': 0xA6,
                   'browser_forward': 0xA7,
                   'browser_refresh': 0xA8,
                   'browser_stop': 0xA9,
                   'browser_search': 0xAA,
                   'browser_favorites': 0xAB,
                   'browser_start_and_home': 0xAC,
                   'volume_mute': 0xAD,
                   'volume_Down': 0xAE,
                   'volume_up': 0xAF,
                   'next_track': 0xB0,
                   'previous_track': 0xB1,
                   'stop_media': 0xB2,
                   'play/pause_media': 0xB3,
                   'start_mail': 0xB4,
                   'select_media': 0xB5,
                   'start_application_1': 0xB6,
                   'start_application_2': 0xB7,
                   'attn_key': 0xF6,
                   'crsel_key': 0xF7,
                   'exsel_key': 0xF8,
                   'play_key': 0xFA,
                   'zoom_key': 0xFB,
                   'clear_key': 0xFE,
                   '+': 0xBB,
                   ',': 0xBC,
                   '-': 0xBD,
                   '.': 0xBE,
                   '/': 0xBF,
                   '`': 0xC0,
                   ';': 0xBA,
                   '[': 0xDB,
                   '\\': 0xDC,
                   ']': 0xDD,
                   "'": 0xDE,
                   '`': 0xC0}

        self.cols = 2

        self.button = Button(text='Click here to set the zero-point', font_size=14)
        self.add_widget(self.button)

        self.enableButton = Button(text='Click here to stop the sensor', font_size=14)
        self.enableButton.background_color = (255,0,0, .3)
        self.add_widget(self.enableButton)

        # self.cols = 2
        sensitivityLabel = Label(text='Sensitivity (now: 40')
        self.add_widget(sensitivityLabel)
        self.sensitivitySlider = Slider(value_track=True, value=40, min=0.5, max=80, value_track_color=[1, 0, 0, 1])
        self.add_widget(self.sensitivitySlider)

        # create a dropdown with 10 buttons
        self.dropdown = DropDown()

        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            btn = Button(text='%s' % p, size_hint_y=None)

            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(btn)

            print(p)

        if len(ports) == 0:
            btn = Button(text='No comports found...' , size_hint_y=None, height=44)

            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(btn)

        # create select comp port button
        comPortLabel = Label(text='Select com port')
        self.add_widget(comPortLabel)

        self.mainbutton = Button(text='Select a COM port', size_hint=(0.5, None))
        self.add_widget(self.mainbutton)

        self.mainbutton.bind(on_release=self.dropdown.open)

        # zero point bigness
        self.rotationArea = Label(text='Adjust rotation ratio area')
        self.add_widget(self.rotationArea)

        self.rotationRatioSlider = Slider(value_track=True, value=0.5, min=0.01, max=1,
                                                value_track_color=[1, 0, 0, 1])
        self.add_widget(self.rotationRatioSlider)

        # keymapping:
        # left key:
        self.leftKeyDropdown = DropDown()
        self.rightKeyDropdown = DropDown()

        for key, keyCode in self.VK_CODE.items():
            print(key)
            btn = Button(text='%s' % key, size_hint_y=None, height=25)
            btn2 = Button(text='%s' % key, size_hint_y=None, height=25)

            btn.bind(on_release=lambda btn: self.leftKeyDropdown.select(btn.text))
            self.leftKeyDropdown.add_widget(btn)

            btn2.bind(on_release=lambda btn: self.rightKeyDropdown.select(btn.text))
            self.rightKeyDropdown.add_widget(btn2)

        self.leftKeyDropdownButton = Button(text='Select a left key', size_hint=(0.5, None))
        self.add_widget(self.leftKeyDropdownButton)

        self.leftKeyDropdownButton.bind(on_release=self.leftKeyDropdown.open)

        self.rightKeyDropdownButton = Button(text='Select a right key', size_hint=(0.5, None))
        self.add_widget(self.rightKeyDropdownButton)

        self.rightKeyDropdownButton.bind(on_release=self.rightKeyDropdown.open)


        def setZeroPoint(instance):
            self.dataReader.setAccellOffset(self)

        def toggleSensor(instance):
            self.dataReader.toggleEnabledButton()
            self.enableButton.text = 'Click here to stop the sensor' if self.dataReader.enabled else 'Click here to start the sensor'
            self.enableButton.background_color = (255,0,0, .3) if self.dataReader.enabled else (0, 255, 0, 0.3)

        def OnSliderValueChange(instance, value):
            sensitivityLabel.text = "Sensitivity (now: " + str(value) + ")"
            self.dataReader.updateSensitivity(value)

        def OnRatioSliderChange(instance, value):
            self.rotationArea.text = "Rotation ration(now: " + str(value) + ")"
            self.dataReader.updateSensitivityFactor(value)

        def comPortChanged(instance, value):
            self.mainbutton.text = value
            self.dataReader.initSerialPort(value[:4])

        def leftButtonChanged(instance, value):
            self.leftKeyDropdownButton.text = 'left key: ' + value
            self.dataReader.remapButton('left', self.VK_CODE[value])

        def rightButtonChanged(instance, value):
            self.rightKeyDropdownButton.text = 'right key: ' + value
            self.dataReader.remapButton('right', self.VK_CODE[value])

        self.sensitivitySlider.bind(value=OnSliderValueChange)
        self.rotationRatioSlider.bind(value=OnRatioSliderChange)
        self.button.bind(on_press=setZeroPoint)
        self.enableButton.bind(on_press=toggleSensor)
        self.dropdown.bind(on_select=comPortChanged)
        self.leftKeyDropdown.bind(on_select=leftButtonChanged)
        self.rightKeyDropdown.bind(on_select=rightButtonChanged)



#note: pyinstaller was not happy inserting the dependency: (adding it in the .spec file as hidden import didn't work. Fix:
class DataReader:
    # config / callibration variables
    def __init__(self):
        # sensitivity:
        self.rotationSensitivity = 40.0

        # zeropoint zone.
        self.thrA = 0.05
        self.accellOffset = 0.0
        self.state = -1
        self.lastInput = None
        self.rotationSensitivityFactor = 1;
        self.enabled = True

        self.leftKey = 0x25
        self.rightKey = 0x27

        t = threading.Thread(target=self.startLoop)
        t.start()

    def initSerialPort(self, comport):
        # print(comport)
        self.ser = None
        try:
            self.ser = serial.Serial(comport, baudrate=115200, timeout=0.01)
        except Exception:
            print('Something is wrong with the COM-port.')
            return
        if self.ser.is_open:
            print('connection is opened successful')

    def setAccellOffset(self, value):
        if self.lastInput == None:
            print('There is no input generated at all by the sensor... Exiting')
            return

        gForceZ = 0.0
        rotY = 0.0
        try:
            gForceZ = float(self.lastInput[0])
            rotY = float(self.lastInput[1][:-3])
        except:
            return

        self.accellOffset = gForceZ;
        print(self.accellOffset)

    def updateState(self):
        if not self.enabled or not hasattr(self, 'ser') or self.ser is None:
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

        # if rotY > self.rotationSensitivity and self.state == 2:
        #     self.state = 0
        #     print("Q")
        #
        # if rotY < - self.rotationSensitivity and self.state == 2:
        #     self.state = 1
        #     print("E")
        #
        # if abs(gForceZ - self.accellOffset) < self.thrA / 2 and self.state != 2:
        #     self.state = 2
        #     win32api.keybd_event(0x51, 0, win32con.KEYEVENTF_KEYUP, 0)
        #     win32api.keybd_event(0x45, 0, win32con.KEYEVENTF_KEYUP, 0)
        #     print("N")

        if gForceZ < self.thrA and rotY > self.rotationSensitivity:
            self.state = 0
            print("Q")

        if gForceZ > self.thrA and rotY < -self.rotationSensitivity:
            self.state = 1;
            print("E")

        if (gForceZ < self.thrA and rotY < -self.rotationSensitivity * self.rotationSensitivityFactor) or (gForceZ > self.thrA and rotY > self.rotationSensitivity / 2 ):
            self.state = 2
            win32api.keybd_event(self.leftKey, 0, win32con.KEYEVENTF_KEYUP, 0)
            win32api.keybd_event(self.rightKey, 0, win32con.KEYEVENTF_KEYUP, 0)
            print("N")


    def startLoop(self):
        time.sleep(3)

        while 1:
            if self.state is 0:
                win32api.keybd_event(self.leftKey, 0, 0, 0)
            if self.state is 1:
                win32api.keybd_event(self.rightKey, 0, 0, 0)
            self.updateState()

    def updateSensitivity(self, value):
        self.rotationSensitivity = value

    def updateSensitivityFactor(self, value):
        self.rotationSensitivityFactor = value

    def remapButton(self, direction, value):
        if direction == 'left':
            self.leftKey = value
        else:
            self.rightKey = value

    def toggleEnabledButton(self):
        self.enabled = not self.enabled
        win32api.keybd_event(self.leftKey, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(self.rightKey, 0, win32con.KEYEVENTF_KEYUP, 0)
        self.state = 2
        self.updateState()
        print(self.enabled)


class SerialSnooperApp(App):
    def build(self):
        return MainScreen()

if __name__ == '__main__':
    SerialSnooperApp().run()