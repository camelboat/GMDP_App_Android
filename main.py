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

#from android.runnable import run_on_ui_thread
#WebView = autoclass('android.webkit.WebView')
#WebViewClient = autoclass('android.webkit.WebViewClient')
#activity = autoclass('org.renpy.android.PythonActivity').mActivity

import requests
import json
import webbrowser

baseURL = 'https://api.thingspeak.com/talkbacks/31641/commands'
baseURL_Channel_get = 'https://api.thingspeak.com/channels/723513/feeds.json?api_key=1M45KUAM480PFZWX&results=2'
baseURL_temperature_setting_room1_get = 'https://api.thingspeak.com/channels/741927/feeds.json?api_key=QZQ9FM7V1MM215R0&results=2'
baseURL_temperature_setting_room1_update = 'https://api.thingspeak.com/update?api_key=LWV7LOPF9QN79QG4&field1=0'


main_widget_kv = '''
#:import Toolbar kivymd.toolbar.Toolbar
#:import ThemeManager kivymd.theming.ThemeManager
#:import MDNavigationDrawer kivymd.navigationdrawer.MDNavigationDrawer
#:import NavigationLayout kivymd.navigationdrawer.NavigationLayout
#:import NavigationDrawerDivider kivymd.navigationdrawer.NavigationDrawerDivider
#:import NavigationDrawerToolbar kivymd.navigationdrawer.NavigationDrawerToolbar
#:import NavigationDrawerSubheader kivymd.navigationdrawer.NavigationDrawerSubheader
#:import MDCheckbox kivymd.selectioncontrols.MDCheckbox
#:import MDSwitch kivymd.selectioncontrols.MDSwitch
#:import MDList kivymd.list.MDList
#:import OneLineListItem kivymd.list.OneLineListItem
#:import TwoLineListItem kivymd.list.TwoLineListItem
#:import ThreeLineListItem kivymd.list.ThreeLineListItem
#:import OneLineAvatarListItem kivymd.list.OneLineAvatarListItem
#:import OneLineIconListItem kivymd.list.OneLineIconListItem
#:import OneLineAvatarIconListItem kivymd.list.OneLineAvatarIconListItem
#:import MDTextField kivymd.textfields.MDTextField
#:import MDSpinner kivymd.spinner.MDSpinner
#:import MDCard kivymd.card.MDCard
#:import MDSeparator kivymd.card.MDSeparator
#:import MDDropdownMenu kivymd.menu.MDDropdownMenu
#:import get_color_from_hex kivy.utils.get_color_from_hex
#:import colors kivymd.color_definitions.colors
#:import SmartTile kivymd.grid.SmartTile
#:import MDSlider kivymd.slider.MDSlider
#:import MDTabbedPanel kivymd.tabs.MDTabbedPanel
#:import MDTab kivymd.tabs.MDTab
#:import MDProgressBar kivymd.progressbar.MDProgressBar
#:import MDAccordion kivymd.accordion.MDAccordion
#:import MDAccordionItem kivymd.accordion.MDAccordionItem
#:import MDAccordionSubItem kivymd.accordion.MDAccordionSubItem
#:import MDThemePicker kivymd.theme_picker.MDThemePicker
#:import MDBottomNavigation kivymd.tabs.MDBottomNavigation
#:import MDBottomNavigationItem kivymd.tabs.MDBottomNavigationItem

NavigationLayout:
    id: nav_layout
    MDNavigationDrawer:
        id: nav_drawer
        NavigationDrawerToolbar:
            title: "CHOOSE YOUR FUNCTION"
        NavigationDrawerIconButton:
            icon: 'lightbulb'
            text: "Lighting System"
            on_release: app.root.ids.scr_mngr.current = 'light'
        NavigationDrawerIconButton:
            icon: 'temperature-celsius'
            text: "Temperature"
            on_release: app.root.ids.scr_mngr.current = 'get_temperature'
        NavigationDrawerIconButton:
            icon: 'nature-people'
            text: "Room Occupation"
            on_release: app.root.ids.scr_mngr.current = 'room_occupation'
        NavigationDrawerIconButton:
            icon: 'checkbox-blank-circle'
            text: "Account Setting"
            on_release: app.root.ids.scr_mngr.current = 'account_setting'
        
    BoxLayout:
        orientation: 'vertical'
        Toolbar:
            id: toolbar
            title: 'GMDP Team2 Smart Room'
            md_bg_color: app.theme_cls.primary_color
            background_palette: 'Primary'
            background_hue: '500'
            left_action_items: [['menu', lambda x: app.root.toggle_nav_drawer()]]
            right_action_items: [['dots-vertical', lambda x: app.root.toggle_nav_drawer()]]
        ScreenManager:
            id: scr_mngr
            Screen:
                name: 'light'
                ScrollView:
                    do_scroll_x: False
                    MDList:
                        id: ml
                        OneLineAvatarIconListItem:
                            text: "Light #1"
                            AvatarSampleWidget:
                                source: './assets/light_bulb.png'
                            MDSwitch:
                                size_hint:    None, None
                                size:        dp(36), dp(48)
                                pos_hint:    {'center_x': 0.92, 'center_y': 0.5}
                                _active:      True
                                on_active: app.show_example_snackbar('switch')

            Screen:
                name: 'get_temperature'
                MDCard:
                    size_hint: 0.45, 0.3
                    #size: dp(360), dp(100)
                    pos_hint: {'center_x': 0.25, 'center_y': 0.8}
                    BoxLayout:
                        orientation:'vertical'
                        padding: dp(8)
                        MDLabel:
                            text: 'Current Temperature ('+u'\N{DEGREE SIGN}'+'C)'
                            theme_text_color: 'Secondary'
                            font_style:"Body1"
                            size_hint_y: None
                            height: dp(36)
                            halign: 'center'
                            font_size: '6pt'
                        MDSeparator:
                            height: dp(1)
                        MDLabel:
                            text: str(app.Room_1_Temp)
                            theme_text_color: 'Secondary'
                            font_style:"Title"
                            halign: 'center'
                            font_size: '20pt'
                # MDCard:
                #     size_hint: 0.45, 0.3
                #     #size: dp(360), dp(100)
                #     pos_hint: {'center_x': 0.75, 'center_y': 0.8}
                #     BoxLayout:
                #         orientation:'vertical'
                #         padding: dp(8)
                #         MDLabel:
                #             text: 'People Number Condition'
                #             theme_text_color: 'Secondary'
                #             font_style:"Body1"
                #             size_hint_y: None
                #             height: dp(36)
                #             halign: 'center'
                #             font_size: '6pt'
                #         MDSeparator:
                #             height: dp(1)
                #         MDLabel:
                #             text: 'Not available now'
                #             theme_text_color: 'Secondary'
                #             font_style:"Title"
                #             halign: 'center'
                #             font_size: '10pt'
                MDCard:
                    size_hint: 0.45, 0.3
                    #size: dp(360), dp(100)
                    pos_hint: {'center_x': 0.75, 'center_y': 0.8}
                    BoxLayout:
                        orientation:'vertical'
                        padding: dp(8)
                        MDLabel:
                            text: 'Current Air-conditioner Temperature Setting ('+u'\N{DEGREE SIGN}'+'C)'
                            theme_text_color: 'Secondary'
                            font_style:"Body1"
                            size_hint_y: None
                            height: dp(36)
                            halign: 'center'
                            font_size: '6pt'
                        MDSeparator:
                            height: dp(1)
                        MDLabel:
                            text: str(app.Room_1_Current_Setting)
                            theme_text_color: 'Secondary'
                            font_style:"Title"
                            halign: 'center'
                            font_size: '20pt'
                MDRaisedButton:
                    text: "Get Latest Room Condition Info"
                    elevation_normal: 2
                    opposite_colors: True
                    size_hint: 0.95, 0.1
                    pos_hint: {'center_x': 0.5, 'center_y': 0.2}
                    on_release: app.get_temperature()
                MDRaisedButton:
                    text: "Check Plot for Temperature on ThingSpeak"
                    elevation_normal: 2
                    opposite_colors: True
                    size_hint: 0.95, 0.1
                    pos_hint: {'center_x': 0.5, 'center_y': 0.075}
                    on_release: app.get_temperature_plot()
                MDFloatingActionButton:
                    id: float_act_btn
                    icon: 'plus'
                    opposite_colors: True
                    elevation_normal: 8
                    size: dp(80), dp(80)                    
                    pos_hint: {'center_x': 0.25, 'center_y': 0.45}
                    on_release: app.increase_temperature()
                MDFloatingActionButton:
                    id: float_act_btn
                    icon: 'minus'
                    opposite_colors: True
                    elevation_normal: 8
                    size: dp(80), dp(80)
                    pos_hint: {'center_x': 0.75, 'center_y': 0.45}
                    on_release: app.decrease_temperature()
                MDFloatingActionButton:
                    id: float_act_btn
                    icon: 'power'
                    opposite_colors: True
                    elevation_normal: 8
                    size: dp(80), dp(80)
                    pos_hint: {'center_x': 0.5, 'center_y': 0.45}
                    on_release: app.on_off_room1_ac()
                # MDRaisedButton:
                #     text: "+"
                #     font_style: 'Title'
                #     elevation_normal: 2
                #     opposite_colors: True
                #     size_hint: 0.45, 0.1
                #     pos_hint: {'center_x': 0.75, 'center_y': 0.55}
                #     # font_size: '100pt'
                #     on_release: app.increase_temperature()
                # MDRaisedButton:
                #     text: "-"
                #     elevation_normal: 2
                #     opposite_colors: True
                #     size_hint: 0.45, 0.1
                #     pos_hint: {'center_x': 0.75, 'center_y': 0.35}
                #     font_size: '100pt'
                #     on_release: app.decrease_temperature()
            Screen:
                name: 'room_occupation'
                MDCard:
                    size_hint: 0.95, 0.3
                    #size: dp(360), dp(100)
                    pos_hint: {'center_x': 0.5, 'center_y': 0.8}
                    BoxLayout:
                        orientation:'vertical'
                        padding: dp(8)
                        MDLabel:
                            text: 'People Number Condition'
                            theme_text_color: 'Secondary'
                            font_style:"Body1"
                            size_hint_y: None
                            height: dp(36)
                            halign: 'center'
                            font_size: '6pt'
                        MDSeparator:
                            height: dp(1)
                        MDLabel:
                            text: 'Not available now'
                            theme_text_color: 'Secondary'
                            font_style:"Title"
                            halign: 'center'
                            font_size: '10pt'              
            Screen:
                name: 'account_setting'
                ScrollView:
                    do_scroll_x: False
                    MDList:
                        id: ml
                        OneLineListItem:
                            text: "One-line item"
                        TwoLineListItem:
                            text: "Two-line item"
                            secondary_text: "Secondary text here"
                        ThreeLineListItem:
                            text: "Three-line item"
                            secondary_text: "This is a multi-line label where you can fit more text than usual"
                        OneLineAvatarListItem:
                            text: "Single-line item with avatar"
                            AvatarSampleWidget:
                                source: './assets/avatar.png'
                        TwoLineAvatarListItem:
                            type: "two-line"
                            text: "Two-line item..."
                            secondary_text: "with avatar"
                            AvatarSampleWidget:
                                source: './assets/avatar.png'
                        ThreeLineAvatarListItem:
                            type: "three-line"
                            text: "Three-line item..."
                            secondary_text: "...with avatar..." + '\\n' + "and third line!"
                            AvatarSampleWidget:
                                source: './assets/avatar.png'
                        OneLineIconListItem:
                            text: "Single-line item with left icon"
                            IconLeftSampleWidget:
                                id: li_icon_1
                                icon: 'star-circle'
                        TwoLineIconListItem:
                            text: "Two-line item..."
                            secondary_text: "...with left icon"
                            IconLeftSampleWidget:
                                id: li_icon_2
                                icon: 'comment-text'
                        ThreeLineIconListItem:
                            text: "Three-line item..."
                            secondary_text: "...with left icon..." + '\\n' + "and third line!"
                            IconLeftSampleWidget:
                                id: li_icon_3
                                icon: 'sd'
                        OneLineAvatarIconListItem:
                            text: "Single-line + avatar&icon"
                            AvatarSampleWidget:
                                source: './assets/avatar.png'
                            IconRightSampleWidget:
                        TwoLineAvatarIconListItem:
                            text: "Two-line item..."
                            secondary_text: "...with avatar&icon"
                            AvatarSampleWidget:
                                source: './assets/avatar.png'
                            IconRightSampleWidget:
                        ThreeLineAvatarIconListItem:
                            text: "Three-line item..."
                            secondary_text: "...with avatar&icon..." + '\\n' + "and third line!"
                            AvatarSampleWidget:
                                source: './assets/avatar.png'
                            IconRightSampleWidget:
'''


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
            # widget.bind(on_release=lambda x: self.panel.toggle_state())
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

    Room_2_Temp = ObjectProperty()
    Room_2_Current_Setting = ObjectProperty()
    Room_2_Light = ObjectProperty()
    Room_2_AC_Status = ObjectProperty()

    User_1_Configuration = ObjectProperty()

    def build(self):
        main_widget = Builder.load_string(main_widget_kv)
        # self.theme_cls.theme_style = 'Dark'
        self.var_init()
        return main_widget

    def var_init(self):
        self.get_temperature()
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
        r = requests.get(baseURL_Channel_get)
        data = json.loads(r.text)
        self.Room_1_Temp = data['feeds'][1]['field1'][1:]

    def get_temperature_setting_room1(self):
        r = requests.get(baseURL_temperature_setting_room1_get)
        data = json.loads(r.text)
        self.Room_1_Current_Setting = int(data['feeds'][1]['field1'][1:])

    def show_example_snackbar(self, snack_type):
        if snack_type == 'on':
            post_command("001", 1)
            Snackbar(text="Turn on successfully!").show()
        elif snack_type == 'off':
            post_command("000", 1)
            Snackbar(text="Turn off successfully!").show()
        elif snack_type == 'switch':
            self.Room_1_Light = 1 - self.Room_1_Light
            post_command("00"+str(self.Room_1_Light), 1)
            if self.Room_1_Light == 0:
                Snackbar(text="Turn off successfully!").show()
            elif self.Room_1_Light == 1:
                Snackbar(text="Turn on successfully!").show()

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

    def get_temperature_plot(self):
        webbrowser.open('https://thingspeak.com/channels' +
                        '/723513/charts/1?bgcolor=%23ffffff&color=%23d62020' +
                        '&dynamic=true&results=200&type=line&update=15'
        )

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

