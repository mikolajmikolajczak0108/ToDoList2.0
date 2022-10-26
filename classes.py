from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.pagelayout import PageLayout
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.label import MDLabel
import Functions
from kivy.uix.popup import Popup
from KivyCalendarForPyt3 import DatePicker, CalendarWidget
from kivy.core.audio import SoundLoader

##########################################ADDITIONAL CLASSES
class CustomDatePicker(DatePicker):

    def update_value(self, inst):
        """ Update textinput value on popup close """

        self.text = "%s.%s.%s" % tuple(self.cal.active_date)
        self.focus = False
        App.get_running_app().root.ids.ti.text = self.text
##########################################WINDOWS
class MainWindow(Screen):
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        self.isLogged = 0
        print("I work")
        self.data_base = None
        self.currentuser = ''
        self.normaltasks = [] #lists to hold the task that are always loaded from JSON File
        self.VIPtasks = []
        self.isoptionsmade = 0
        self.sounds = []
        self.sound1 = SoundLoader.load('music/Jazz.mp3') ##Preloading music themes
        self.sound2 = SoundLoader.load('music/RnB.mp3')
        self.sounds.append(self.sound1)
        self.sounds.append(self.sound2)
        Functions.maketaskdatabase() #Loads tasks from JSON File
    def on_login_click(self):
        if self.isLogged == 0:
            self.parent.current = "login"
        else:
            self.parent.current = 'ListOptionsWindow'
    def on_signin_click(self):
        if self.isLogged == 0:
            self.parent.current = "signin"
        else:
            self.parent.current = 'ListOptionsWindow'

    def on_options_click(self):
        self.parent.current = 'options_window'
        if not self.isoptionsmade:
            self.parent.get_screen('options_window').show_musics()
            self.parent.get_screen('options_window').show_graphics()
            self.isoptionsmade = 1 #To avoid endless spawn of widgets

    def on_quit_click(self):
        quit()

class LoginWindow(Screen):
    def logger(self):
        pass

    def clear(self):
        self.ids.user.text = ""
        self.ids.passw.text = ""

    def login(self):
        if Functions.LoginFunction(self) == 1:
            self.parent.get_screen('main').isLogged = 1
            self.parent.current = "ListOptionsWindow"
        else:
            self.parent.isLogged = 0

class SignInWindow(Screen):

    def signin(self):
        if Functions.SigninFunction(self) == 1:
            print("Signed in!")
            self.parent.get_screen('main').isLogged = 1
            self.parent.current = "ListOptionsWindow"
        else:
            self.parent.isLogged = 0

    def clear(self):
        self.ids.name.text = ""
        self.ids.tel.text = ""
        self.ids.email.text = ""
        self.ids.user.text = ""
        self.ids.passw.text = ""
        self.ids.passw2.text = ""

class AboutWindow(Screen):
    pass

class ListOptionsWindow(Screen):

    def back(self):
        self.parent.current = "main"

    def logout(self):
        self.parent.get_screen('main').ids.loginbutton.text = "login"
        self.parent.get_screen('main').isLogged = 0
        self.parent.current = 'main'

    def add_task(self):
        self.parent.current = 'AddTask'

    def show_task(self):
        self.parent.current = 'show_tasks'
        if not self.parent.get_screen('main').normaltasks and not self.parent.get_screen('main').VIPtasks: #To never load tasks when they are.. already loaded automatically in other functions
            Functions.load_tasks(self.parent.get_screen('show_tasks'))
    def show_delete_task(self):
        self.parent.current = 'delete_task'
        Functions.load_delete_tasks(self.parent.get_screen('delete_task'), self.parent.get_screen('delete_task').inDeleteState, self.parent.get_screen('delete_task').tasksLoaded, self.parent.get_screen('delete_task').addingWidget)
        self.parent.get_screen('delete_task').tasksLoaded = 1
    def show_calendar(self):
        calendar = CalendarWidget(self.parent, 0, 0)
        #THIS IS NOT KIVYCALENDAR FOR PYTHON 2.7, THIS IS FIX FOR PYTHON 3.X, ONLY WORKS IMPORTED FROM MODULE ATTACHED WITH PROJECT -> I made several changes also in it's front-end and
        # it implements working with tasks so it only works along with this app
        self.parent.get_screen('calendar').ids.calendarlayout.add_widget(calendar)

        self.parent.current = 'calendar'

    def show_finished_tasks(self):
        self.parent.current = 'finish_task'
        Functions.load_finished_tasks(self.parent.get_screen('finish_task'))
class AddingTask(Screen):
    def make_task(self):
        Functions.adding_task(self)

class TaskShow(Screen):
    pass
class DeleteTask(Screen):
    def __init__(self, **kwargs):
        super(DeleteTask, self).__init__(**kwargs)
        self.tasksLoaded = 0
        self.inDeleteState = 0 #Logical states that are used to manage task-reloading
        self.addingWidget = 0
    def deletecurrent(self, task):
        Functions.delete_task(self, task)
class FinishTask(Screen):
    def __init__(self, **kwargs):
        super(FinishTask, self).__init__(**kwargs)
    def back(self):
        self.parent.current = 'ListOptionsWindow'
        self.ids.FinishedTasks.clear_widgets()

class CalendarWindow(Screen):

    def back(self):
        self.ids.calendarlayout.clear_widgets()
        self.parent.current = 'ListOptionsWindow'

class CustomDropDown(DropDown): #From Kivy site, implementation of Drop-Down List, I did override it's basic on_select method to make it useful for the app
    def __init__(self, scr, **kwargs):
        super(CustomDropDown, self).__init__(**kwargs)
        self.scr=scr
    def on_select(self, data):
        if data == 'Jazz.mp3':
            self.scr.get_screen('main').sounds[1].stop()
            self.scr.get_screen('main').sounds[0].play()
        elif data == "RnB.mp3":
            self.scr.get_screen('main').sounds[0].stop()
            self.scr.get_screen('main').sounds[1].play()
        elif data == "None":
            self.scr.get_screen('main').sounds[0].stop()
            self.scr.get_screen('main').sounds[1].stop()
        elif data == "Dark":
            print("dark") #I plan to change the graphics theme in here (which is set in main.py automatically to dark)
        elif data == "Light":
            print("light")
        else:
            pass

class OptionsWindow(Screen):
    def __init__(self, **kwargs):
        super(OptionsWindow, self).__init__(**kwargs)
        self.mute=0
    def show_musics(self): #Drop-Down list for soundtrack options
        dropdown = CustomDropDown(self.parent)
        dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))
        mainbutton = MDRectangleFlatButton(text='Choose Sound', size_hint=(None, None))
        mainbutton.font_name = 'fonts/unispace.ttf'
        mainbutton.font_size = 25
        mainbutton.size_hint = 1, 0.3
        mainbutton.bind(on_release=dropdown.open)
        jazzbutton = MDRectangleFlatButton(text='Jazz.mp3', size_hint=(None, None))
        jazzbutton.font_name = 'fonts/unispace.ttf'
        jazzbutton.font_size = 25
        jazzbutton.size_hint = 1, 0.3
        jazzbutton.bind(on_release=lambda jazzbutton: dropdown.select(jazzbutton.text))
        dropdown.add_widget(jazzbutton)
        rnbbutton = MDRectangleFlatButton(text='RnB.mp3', size_hint=(None, None))
        rnbbutton.font_name = 'fonts/unispace.ttf'
        rnbbutton.font_size = 25
        rnbbutton.size_hint = 1, 0.3
        rnbbutton.bind(on_release=lambda rnbbutton: dropdown.select(rnbbutton.text))
        dropdown.add_widget(rnbbutton)
        nonebutton = MDRectangleFlatButton(text='None', size_hint=(None, None))
        nonebutton.font_name = 'fonts/unispace.ttf'
        nonebutton.font_size = 25
        nonebutton.size_hint = 1, 0.3
        nonebutton.bind(on_release=lambda nonebutton: dropdown.select(nonebutton.text))
        dropdown.add_widget(nonebutton)
        self.ids.music_chooser.add_widget(mainbutton)

    def on_mute_active(self, isActive):
        if not self.mute:
            self.parent.get_screen('main').sounds[0].volume = 0
            self.parent.get_screen('main').sounds[1].volume = 0
            self.mute = 1
        else:
            self.parent.get_screen('main').sounds[0].volume = self.ids.volume_slider.value_normalized
            self.parent.get_screen('main').sounds[1].volume = self.ids.volume_slider.value_normalized
            self.mute = 0

    def change_volume(self): #volume is set by slider widget added in .kv file
        self.parent.get_screen('main').sounds[0].volume = self.ids.volume_slider.value_normalized
        self.parent.get_screen('main').sounds[1].volume = self.ids.volume_slider.value_normalized

    def show_graphics(self):
        dropdown = CustomDropDown(self.parent)
        dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))
        mainbutton = MDRectangleFlatButton(text='Dark', size_hint=(None, None))
        mainbutton.font_name = 'fonts/unispace.ttf'
        mainbutton.font_size = 25
        mainbutton.size_hint = 1, 0.3
        mainbutton.bind(on_release=dropdown.open)
        darkbutton = MDRectangleFlatButton(text='Dark', size_hint=(None, None))
        darkbutton.font_name = 'fonts/unispace.ttf'
        darkbutton.font_size = 25
        darkbutton.size_hint = 1, 0.3
        darkbutton.bind(on_release=lambda darkbutton: dropdown.select(darkbutton.text))
        dropdown.add_widget(darkbutton)
        lightbutton = MDRectangleFlatButton(text='Light', size_hint=(None, None))
        lightbutton.font_name = 'fonts/unispace.ttf'
        lightbutton.font_size = 25
        lightbutton.size_hint = 1, 0.3
        lightbutton.bind(on_release=lambda lightbutton: dropdown.select(lightbutton.text))
        dropdown.add_widget(lightbutton)
        self.ids.graphics_set_chooser.add_widget(mainbutton)

class WindowManager(ScreenManager):
    pass


