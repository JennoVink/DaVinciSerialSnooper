import copy
import kivy
kivy.require('1.0.6') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput

import math

import serial
import serial.tools.list_ports

import win32api
import win32con
import time
import threading




class MainScreen(GridLayout):

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.dataReader = DataReader()

        self.VK_CODE = {'q': 0x51,'e': 0x45,'backspace': 0x08,'tab': 0x09,'clear': 0x0C,'enter': 0x0D,'shift': 0x10,'ctrl': 0x11,'alt': 0x12,'pause': 0x13,'caps_lock': 0x14,'esc': 0x1B,'spacebar': 0x20,'page_up': 0x21,'page_down': 0x22,'end': 0x23,'home': 0x24,'left_arrow': 0x25,'up_arrow': 0x26,'right_arrow': 0x27,'down_arrow': 0x28,'select': 0x29,'print': 0x2A,
                   'execute': 0x2B,'print_screen': 0x2C,'ins': 0x2D,'del': 0x2E,'help': 0x2F,'0': 0x30,'1': 0x31,'2': 0x32,'3': 0x33,'4': 0x34,'5': 0x35,'6': 0x36,'7': 0x37,'8': 0x38,'9': 0x39,'a': 0x41,'b': 0x42,'c': 0x43,'d': 0x44,
                   'f': 0x46,'g': 0x47,'h': 0x48,'i': 0x49,'j': 0x4A,'k': 0x4B,'l': 0x4C,'m': 0x4D,'n': 0x4E,'o': 0x4F,'p': 0x50,'r': 0x52,'s': 0x53,'t': 0x54,'u': 0x55,'v': 0x56,'w': 0x57,'x': 0x58,'y': 0x59,'z': 0x5A,'numpad_0': 0x60,'numpad_1': 0x61,'numpad_2': 0x62,'numpad_3': 0x63,'numpad_4': 0x64,'numpad_5': 0x65,'numpad_6': 0x66,'numpad_7': 0x67,'numpad_8': 0x68,'numpad_9': 0x69,'multiply_key': 0x6A,'add_key': 0x6B,'separator_key': 0x6C,'subtract_key': 0x6D,'decimal_key': 0x6E,'divide_key': 0x6F,'F1': 0x70,'F2': 0x71,'F3': 0x72,'F4': 0x73,'F5': 0x74,'F6': 0x75,'F7': 0x76,'F8': 0x77,'F9': 0x78,'F10': 0x79,'F11': 0x7A,'F12': 0x7B,'F13': 0x7C,'F14': 0x7D,'F15': 0x7E,'F16': 0x7F,'F17': 0x80,'F18': 0x81,'F19': 0x82,'F20': 0x83,'F21': 0x84,'F22': 0x85,'F23': 0x86,'F24': 0x87,'num_lock': 0x90,'scroll_lock': 0x91,'left_shift': 0xA0,'right_shift ': 0xA1,'left_control': 0xA2,'right_control': 0xA3,'left_menu': 0xA4,'right_menu': 0xA5,'browser_back': 0xA6,'browser_forward': 0xA7,'browser_refresh': 0xA8,'browser_stop': 0xA9,'browser_search': 0xAA,
                   'browser_favorites': 0xAB,'browser_start_and_home': 0xAC,'volume_mute': 0xAD,'volume_Down': 0xAE,'volume_up': 0xAF,'next_track': 0xB0,'previous_track': 0xB1,'stop_media': 0xB2,'play/pause_media': 0xB3,'start_mail': 0xB4,'select_media': 0xB5,'start_application_1': 0xB6,'start_application_2': 0xB7,'attn_key': 0xF6,'crsel_key': 0xF7,'exsel_key': 0xF8,'play_key': 0xFA,'zoom_key': 0xFB,'clear_key': 0xFE,'+': 0xBB,',': 0xBC,'-': 0xBD,'.': 0xBE,'/': 0xBF,'`': 0xC0,';': 0xBA,'[': 0xDB,'\\': 0xDC,']': 0xDD,"'": 0xDE,'`': 0xC0}

        self.cols = 2

        self.recordButton = Button(text='Click here to record a new gesture.', font_size=14)
        self.add_widget(self.recordButton)

        self.enableButton = Button(text='Click here to stop the sensor', font_size=14)
        self.enableButton.background_color = (255,0,0, .3)
        self.add_widget(self.enableButton)

        # self.cols = 2
        inputBoxName = TextInput(text='Name for the new gesture')
        self.add_widget(inputBoxName)
        self.recognizeButton = Button(text='Recognize!')
        self.add_widget(self.recognizeButton)

        sensetivityLabel = Label(text='sensetivity')
        self.add_widget(sensetivityLabel)
        self.sensitivitySlider = Slider(value_track=True, value=60, min=0.5, max=80, value_track_color=[1, 0, 0, 1])
        self.add_widget(self.sensitivitySlider)

        # create a dropdown with 10 buttons
        self.dropdown = DropDown()

        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            print(p)
            btn = Button(text='%s' % p, size_hint_y=None)

            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(btn)

        if len(ports) == 0:
            btn = Button(text='No comports found...' , size_hint_y=None, height=44)

            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(btn)

        # create select comp port button
        comPortLabel = Label(text='Select com port')
        self.add_widget(comPortLabel)

        self.mainbutton = Button(text='Select a COM port', size_hint=(0.1, None))
        self.add_widget(self.mainbutton)

        self.mainbutton.bind(on_release=self.dropdown.open)

        # keymapping:
        # left key:
        self.leftKeyDropdown = DropDown()
        self.rightKeyDropdown = DropDown()

        for key, keyCode in self.VK_CODE.items():
            btn = Button(text='%s' % key, size_hint_y=None, height=30)
            btn2 = Button(text='%s' % key, size_hint_y=None, height=30)

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


        def recordGesture(instance):
            self.dataReader.recordGesture(gestureName=inputBoxName.text)

        def recognizeGesture(instance):
            self.dataReader.recognizeGesture()

        def toggleSensor(instance):
            self.dataReader.toggleEnabledButton()
            self.enableButton.text = 'Click here to stop the sensor' if self.dataReader.enabled else 'Click here to start the sensor'
            self.enableButton.background_color = (255,0,0, .3) if self.dataReader.enabled else (0, 255, 0, 0.3)

        def OnSliderValueChange(instance, value):
            sensetivityLabel.text = "Sensitivity (now: " + str(value) + ")"
            self.dataReader.updateSensitivity(79.5 - value)

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
        self.recordButton.bind(on_press=recordGesture)
        self.recognizeButton.bind(on_press=recognizeGesture)
        self.enableButton.bind(on_press=toggleSensor)
        self.dropdown.bind(on_select=comPortChanged)
        self.leftKeyDropdown.bind(on_select=leftButtonChanged)
        self.rightKeyDropdown.bind(on_select=rightButtonChanged)



#note: pyinstaller was not happy inserting the dependency: (adding it in the .spec file as hidden import didn't work. Fix:
class DataReader:
    # config / callibration variables
    def __init__(self):
        self.state = 3
        self.lastInput = None
        self.enabled = True

        self.leftKey = 0x51
        self.rightKey = 0x45

        self.lastComport = None

        self.gestures = {}
        self.recordedData = []
        self.recording = True
        self.isRecognizing = False

        t = threading.Thread(target=self.startLoop)
        t.start()

    def initSerialPort(self, comport):
        if comport != None:
            self.lastComport = comport

        self.serialStream = None
        try:
            self.serialStream = serial.Serial(self.lastComport, baudrate=115200, timeout=0.01)
        except Exception as e:
            print( 'Something is wrong with the COM-port.')
            print(e)
            return

        if self.serialStream.is_open:
            print('connection is opened successfully')


    def recordGesture(self, gestureName):
        if not self.recording:
            self.recordedData.clear()
        else:
            # if the gesure is not already recognized
            if not len(self.gestures.get(gestureName, {})):
                self.gestures[gestureName] = {}

            self.gestures[gestureName][len(self.gestures[gestureName]) + 1] = self.processRecordedData(self.recordedData)

            print(self.gestures)
        self.recording = not self.recording

    def updateState(self):
        if not self.enabled or not hasattr(self, 'serialStream') or self.serialStream is None:
            return

        # here is self.ser not none
        if not self.serialStream.is_open:
            return

        if not self.recording and not self.isRecognizing:
            return

        data = self.serialStream.readline().decode('ascii').split('\t')

        if len(data) != 6:
            return

        # remove the \r\n
        data[-1] = data[-1][:-3]

        data = [float(sensorValue) for sensorValue in data]

        self.lastInput = data
        self.recordedData.append(data)

        if self.isRecognizing:
            gesturesCopy = copy.deepcopy(self.gestures)

            for gestureName, thresholds in gesturesCopy.items():
                i = 0;
                for key, thresholdDataSet in thresholds.items():
                    print(':::::thresholddataset:::::')
                    print(thresholdDataSet)
                    for key, thresholds in thresholdDataSet.items():
                        for threshold in thresholds:
                            print(threshold)

                            None
                            # if threshold[0] == '<':
                            #     if data[i] > threshold[1]:
                            #         # better remove from dict.
                            #         break
                            # else:
                            #     if data[i] < threshold[1]:
                            #         break

                i += 1


        # print(data)

    def startLoop(self):
        time.sleep(3)

        while 1:
            if self.state is -1:
                win32api.keybd_event(self.leftKey, 0, 0, 0)
            if self.state is 1:
                win32api.keybd_event(self.rightKey, 0, 0, 0)
            self.updateState()

    def updateSensitivity(self, value):
        self.rotationSensitivity = value

    def updateSensitivityFactor(self, value):
        self.rotationSensitivityFactor = value

    def updateZeroArea(self, value):
        self.neutralZoneDegrees = value

    def remapButton(self, direction, value):
        if direction == 'left':
            self.leftKey = value
        else:
            self.rightKey = value

    def toggleEnabledButton(self):
        self.enabled = not self.enabled
        win32api.keybd_event(self.leftKey, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(self.rightKey, 0, win32con.KEYEVENTF_KEYUP, 0)
        self.state = 0
        self.updateState()

        if self.enabled:
            self.initSerialPort(comport=None)
        elif self.serialStream.is_open and self.enabled == False:
            self.serialStream.close()
            print(self.enabled)

    # process the recorded data and
    def processRecordedData(self, recordedData):
        deviationFactor = 1
        thresholdValues = {}
        print('----------')
        print(recordedData[0])
        print(recordedData[-1])

        i = 0
        for recordedDatasetStart in recordedData[0]:
            limit = recordedData[-1][i] * deviationFactor
            if recordedDatasetStart >= recordedData[-1][i]:
                thresholdValues[i] = {}
                thresholdValues[i]['<'] = limit

            else:
                thresholdValues[i] = {}
                thresholdValues[i]['>'] = limit

            i += 1

        # print('---------- Thresholds from process recorded data -----')
        #
        # print(thresholdValues)
        # print('//////// Thresholds -----')

        return thresholdValues

    def recognizeGesture(self):
        self.isRecognizing = not self.isRecognizing


class SerialSnooperApp(App):
    def build(self):
        return MainScreen()

if __name__ == '__main__':
    SerialSnooperApp().run()