
# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager


class MainWid(ScreenManager):
	pass


class MainApp(App):
	title = 'Inventário'
	
	def build(self):
		return MainWid()


if __name__ == '__main__':
	win = MainApp()
	win.run()


