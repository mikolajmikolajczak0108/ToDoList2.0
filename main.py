from kivy import Config
Config.set('graphics', 'fullscreen', 'auto')
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
Window.maximize()

import classes


class ToDoListApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = "DeepPurple"
        return Builder.load_file('ToDoList.kv')



ToDoListApp().run()


