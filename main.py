
# -*- coding: utf-8 -*-

import os
import sqlite3
from kivy.app import App
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager

Config.set('graphics', 'width', '340')
Config.set('graphics', 'height', '640')


def connect_db(path):
	try:
		con = sqlite3.connect(path)
		cursor = con.cursor()
		create_table_product(cursor)
		con.commit()
	except Exception as e:
		print(e)
	finally:
		con.close()


def create_table_product(cursor):
	cursor.execute(
		"""
		CREATE TABLE product(
			id INT PRIMARY KEY NOT NULL,
			nome TEXT NOT NULL,
			marca TEXT NOT NULL,
			valor FLOAT NOT NULL
		)"""
	)
	

class MainWid(ScreenManager):
	
	def __init__(self, *args, **kwargs):
		super().__init__(**kwargs)
		self.APP_PATH = os.getcwd()
		self.BD_PATH = self.APP_PATH + '/db_sqlite3.db'
		self.startWid = StartWid(self)
		self.dataBaseWid = DataBaseWid(self)
		
		wid = Screen(name='start')
		wid.add_widget(self.startWid)
		self.add_widget(wid)
		
		wid = Screen(name='database')
		wid.add_widget(self.dataBaseWid)
		self.add_widget(wid)

		self.start()

	def start(self):
		self.current = 'start'

	def dataBase(self):
		self.current = 'database'
		

class StartWid(BoxLayout):
	
	def __init__(self, mainwid, **kwargs):
		super().__init__(**kwargs)
		self.mainwid = mainwid

	def create_db(self):
		connect_db(self.mainwid.BD_PATH)
		self.mainwid.dataBase()


class DataBaseWid(BoxLayout):

	def __init__(self, mainwid, **kwargs):
		super(DataBaseWid, self).__init__(**kwargs)
		self.mainwid = mainwid


class MainApp(App):
	title = 'Inventário'
	
	def build(self):
		return MainWid()


if __name__ == '__main__':
	win = MainApp()
	win.run()


