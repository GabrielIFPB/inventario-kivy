
# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager

Config.set('graphics', 'width', '340')
Config.set('graphics', 'height', '640')


class MainWid(ScreenManager):
	
	def __init__(self, *args, **kwargs):
		super().__init__(**kwargs)
		self.startWid = StartWid()
		
		wid = Screen(name='start')
		wid.add_widget(self.startWid)
		self.add_widget(wid)


class StartWid(BoxLayout):
	pass


class MainApp(App):
	title = 'Inventário'
	
	def build(self):
		return MainWid()


if __name__ == '__main__':
	win = MainApp()
	win.run()


