
import kivy
kivy.require('1.0.6') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy.uix.button import Button

from SerialSnooper import DataReader

class MainScreen(GridLayout):

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.dataReader = DataReader()

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

        self.add_widget(Label(text='Test Area:'))
        self.testArea = TextInput(multiline=False)
        self.add_widget(self.testArea)

        def setZeroPoint(instance):
            self.dataReader.setAccellOffset(self)

        def toggleSensor(instance):
            self.dataReader.toggleEnabledButton()
            self.enableButton.text = 'Click here to stop the sensor' if self.dataReader.enabled else 'Click here to start the sensor'
            self.enableButton.background_color = (255,0,0, .3) if self.dataReader.enabled else (0, 255, 0, 0.3)

        def OnSliderValueChange(instance, value):
            sensitivityLabel.text = "Sensitivity (now: " + str(value) + ")"
            self.dataReader.updateSensitivity(value);

        self.sensitivitySlider.bind(value=OnSliderValueChange)
        self.button.bind(on_press=setZeroPoint)
        self.enableButton.bind(on_press=toggleSensor)


class SerialSnooperApp(App):
    def build(self):
        return MainScreen()

if __name__ == '__main__':
    SerialSnooperApp().run()