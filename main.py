# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.properties import DictProperty
from kivy.uix.image import Image
# from kivy.uix.widget import Widget
from kivy.clock import Clock, mainthread
# from kivy.garden.cefpython import CefBrowser, cefpython

from kivymd.bottomsheet import MDListBottomSheet, MDGridBottomSheet
from kivymd.button import MDIconButton
from kivymd.date_picker import MDDatePicker
from kivymd.dialog import MDDialog
from kivymd.label import MDLabel
from kivymd.list import ILeftBody, ILeftBodyTouch, IRightBodyTouch, BaseListItem
from kivymd.material_resources import DEVICE_TYPE
from kivymd.navigationdrawer import MDNavigationDrawer, NavigationDrawerHeaderBase
from kivymd.selectioncontrols import MDCheckbox
from kivymd.snackbar import Snackbar
from kivymd.theming import ThemeManager
from kivymd.time_picker import MDTimePicker

from jnius import autoclass
from os.path import join, dirname, realpath

from plyer import notification
from plyer.utils import platform
from plyer.compat import PY2
from plyer import vibrator

#from android.runnable import run_on_ui_thread
#WebView = autoclass('android.webkit.WebView')
#WebViewClient = autoclass('android.webkit.WebViewClient')
#activity = autoclass('org.renpy.android.PythonActivity').mActivity

import requests
import json
import webbrowser

baseURL = 'https://api.thingspeak.com/talkbacks/31641/commands'
baseURL_Room1_Condition = 'https://api.thingspeak.com/channels/723513/feeds.json?api_key=1M45KUAM480PFZWX&results=50'
baseURL_temperature_setting_room1_get = 'https://api.thingspeak.com/channels/741927/feeds.json?api_key=QZQ9FM7V1MM215R0&results=2'
baseURL_temperature_setting_room1_update = 'https://api.thingspeak.com/update?api_key=LWV7LOPF9QN79QG4&field1=0'
baseURL_energy_running_get = 'https://api.thingspeak.com/channels/751981/fields/3.json?api_key=G17BAT3422YXJ5JH&results=20'
baseURL_energy_off_get = 'https://api.thingspeak.com/channels/751981/fields/4.json?api_key=G17BAT3422YXJ5JH&results=20'
baseURL_energy = 'https://api.thingspeak.com/channels/751981/feeds.json?api_key=G17BAT3422YXJ5JH&results=50'

BROWN = [153/255, 0, 0, 0.8]
RED = [255/255, 0, 0, 0.8]
ORANGE = [255/255, 128/255, 0, 0.8]
YELLOW = [255/255, 255/255, 0, 0.8]
LIME = [191/255, 255/255, 0, 0.8]
GREEN = [0, 255/255, 0, 0.8]


def post_command(command_string, position):
    instruction = {'api_key': 'NU6M3B6JB1Q3IR76', 'command_string': command_string, 'position': position}
    print("Uploading...")
    thingspeak = requests.post(baseURL, data=instruction)
    print(thingspeak.status_code, thingspeak.reason)
    print("Upload finish")


class HackedDemoNavDrawer(MDNavigationDrawer):
    # DO NOT USE
    def add_widget(self, widget, index=0):
        if issubclass(widget.__class__, BaseListItem):
            self._list.add_widget(widget, index)
            if len(self._list.children) == 1:
                widget._active = True
                self.active_item = widget
            widget.bind(on_release=lambda x: x._set_active(True, list=self))
        elif issubclass(widget.__class__, NavigationDrawerHeaderBase):
            self._header_container.add_widget(widget)
        else:
            super(MDNavigationDrawer, self).add_widget(widget, index)


class KitchenSink(App):
    theme_cls = ThemeManager()
    previous_date = ObjectProperty()
    title = "GMDP Team2 Smart Room"

    Room_1_Temp = ObjectProperty()
    Room_1_Current_Setting = ObjectProperty()
    Room_1_Light = ObjectProperty()
    Room_1_AC_Status = ObjectProperty()
    Room_1_Running_Time = ObjectProperty()
    Room_1_Energy_Saving = ObjectProperty()

    Room_1_PIR_Triggering_Times = ObjectProperty()
    Room_1_Occupancy_Status = ObjectProperty()
    Room_1_Occupancy_Color = ObjectProperty()

    Room_2_Temp = ObjectProperty()
    Room_2_Current_Setting = ObjectProperty()
    Room_2_Light = ObjectProperty()
    Room_2_AC_Status = ObjectProperty()
    Room_2_Running_Time = ObjectProperty()
    Room_2_Energy_Saving = ObjectProperty()

    User_1_Configuration = ObjectProperty()

    def build(self):
        self.var_init()
        main_widget = Builder.load_file('main.kv')
        # self.theme_cls.theme_style = 'Dark'
        return main_widget

    def var_init(self):
        self.get_temperature()
        self.get_occupancy_info()
        self.get_energy_info()
        # self.get_temperature_setting_room1()
        self.Room_1_Light = 0
        self.Room_2_Light = 0
        self.Room_1_AC_Status = 0
        self.Room_2_AC_Status = 0
        self.Room_1_Current_Setting = "Off"
        # self.read_user1_configuration()

    def read_user1_configuration(self):
        with open('data/user_1.json', 'r') as read_file:
            self.User_1_Configuration = json.load(read_file)
            self.Room_1_Current_Setting = self.User_1_Configuration['room1']['current_temperature_setting']

    def write_user1_configuration(self):
        with open('data/user_1.json', 'w') as write_file:
            json.dump(self.User_1_Configuration, write_file)

    def get_temperature(self):
        r = requests.get(baseURL_Room1_Condition)
        data = json.loads(r.text)
        self.Room_1_Temp = round(self.read_valid_data(data, 'field1'))

    def get_occupancy_info(self):
        r = requests.get(baseURL_Room1_Condition)
        data = json.loads(r.text)
        self.Room_1_PIR_Triggering_Times = (self.read_valid_data(data, 'field4'))
        if self.Room_1_PIR_Triggering_Times <= 10:
            self.Room_1_Occupancy_Status = 'Empty Room'
            self.Room_1_Occupancy_Color = GREEN
        elif 10 <= self.Room_1_PIR_Triggering_Times < 100:
            self.Room_1_Occupancy_Status = 'One or two people are here'
            self.Room_1_Occupancy_Color = LIME
        elif 100 <= self.Room_1_PIR_Triggering_Times < 200:
            self.Room_1_Occupancy_Status = 'Several people are here'
            self.Room_1_Occupancy_Color = YELLOW
        elif 200 <= self.Room_1_PIR_Triggering_Times < 300:
            self.Room_1_Occupancy_Status = 'Many people are here'
            self.Room_1_Occupancy_Color = ORANGE
        elif 300 <= self.Room_1_PIR_Triggering_Times < 400:
            self.Room_1_Occupancy_Status = 'The Room is Full !'
            self.Room_1_Occupancy_Color = RED
        elif 400 <= self.Room_1_PIR_Triggering_Times < 500:
            self.Room_1_Occupancy_Status = 'The Room is Full !!'
            self.Room_1_Occupancy_Color = BROWN
        elif self.Room_1_PIR_Triggering_Times >= 500:
            self.Room_1_Occupancy_Status = 'The Room is Full !!!'
            self.Room_1_Occupancy_Color = BROWN
        else:
            self.Room_1_Occupancy_Status = -1

    def get_energy_info(self):
        r = requests.get(baseURL_energy)
        data = json.loads(r.text)
        self.Room_1_Running_Time = round(self.read_valid_data(data, 'field3') / 60, 1)
        self.Room_1_Energy_Saving = round(self.read_valid_data(data, 'field4') * 50 / 3600, 3)

    def get_temperature_setting_room1(self):
        r = requests.get(baseURL_temperature_setting_room1_get)
        data = json.loads(r.text)
        self.Room_1_Current_Setting = int(data['feeds'][1]['field1'][1:])

    def switch_light(self):
        self.Room_1_Light = 1 - self.Room_1_Light
        post_command("00"+str(self.Room_1_Light), 1)
        if self.Room_1_Light == 0:
            self.do_notify('Turn off light #1 successfully!')
        elif self.Room_1_Light == 1:
            self.do_notify('Turn on light #1 successfully!')

    def switch_light_2(self):
        self.Room_2_Light = 1 - self.Room_2_Light
        post_command("01"+str(self.Room_2_Light), 1)
        if self.Room_2_Light == 0:
            self.do_notify('Turn off light #2 successfully!')
        elif self.Room_2_Light == 1:
            self.do_notify('Turn on light #2 successfully!')

    def on_off_room1_ac(self):
        self.Room_1_AC_Status = 1-self.Room_1_AC_Status
        if self.Room_1_AC_Status == 0:
            self.Room_1_Current_Setting = 'Off'
            post_command('1000', 1)
            self.write_user1_configuration()
        elif self.Room_1_AC_Status == 1:
            self.read_user1_configuration()
            post_command('1010', 1)
            post_command('11' + str(self.User_1_Configuration['room1']['current_temperature_setting']), 1)
            self.read_user1_configuration()

    def increase_temperature(self):
        if self.Room_1_Current_Setting != "Off":
            self.Room_1_Current_Setting += 1
            self.User_1_Configuration['room1']['current_temperature_setting'] += 1
            self.write_user1_configuration()
            post_command('11' + str(self.User_1_Configuration['room1']['current_temperature_setting']), 1)

    def decrease_temperature(self):
        if self.Room_1_Current_Setting != "Off":
            self.Room_1_Current_Setting -= 1
            self.User_1_Configuration['room1']['current_temperature_setting'] -= 1
            self.write_user1_configuration()
            post_command('11' + str(self.User_1_Configuration['room1']['current_temperature_setting']), 1)

    @staticmethod
    def get_temperature_plot():
        webbrowser.open(
            'https://thingspeak.com/channels' +
            '/723513/charts/1?bgcolor=%23ffffff&color=%23d62020' +
            '&dynamic=true&results=200&type=line&update=15'
        )

    @staticmethod
    def get_occupancy_plot():
        webbrowser.open(
            'https://thingspeak.com/channels/723513/charts/4?' +
            'bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=200&type=line&update=15'
        )

    @staticmethod
    def read_valid_data(data, field):
        i = 49
        latest_valid_data = data['feeds'][i][field]
        while i >= 0:
            while data['feeds'][i][field] is None:
                i -= 1
            latest_valid_data = data['feeds'][i][field]
            print('latest valid data is: ' + str(latest_valid_data))
            break
        return float(latest_valid_data)

    @staticmethod
    def do_notify(message):
        notification.notify(message=message, toast=True)

    # @staticmethod
    # def do_vibrate(self, time): # not work on Android Q
    #     print(vibrator.exists())
    #     vibrator.vibrate(time=2)

    def set_error_message(self, *args):
        if len(self.root.ids.text_field_error.text) == 2:
            self.root.ids.text_field_error.error = True
        else:
            self.root.ids.text_field_error.error = False

    def on_pause(self):
        return True

    def on_stop(self):
        pass


class AvatarSampleWidget(ILeftBody, Image):
    pass


class IconLeftSampleWidget(ILeftBodyTouch, MDIconButton):
    pass


class IconRightSampleWidget(IRightBodyTouch, MDCheckbox):
    pass


if __name__ == '__main__':
    KitchenSink().run()
