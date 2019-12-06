
# -*- coding: utf-8 -*-

import os
import sqlite3
from kivy.app import App
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
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
		self.insertDataWid = BoxLayout()
		
		wid = Screen(name='start')
		wid.add_widget(self.startWid)
		self.add_widget(wid)
		
		wid = Screen(name='database')
		wid.add_widget(self.dataBaseWid)
		self.add_widget(wid)
		
		wid = Screen(name='insertdata')
		wid.add_widget(self.insertDataWid)
		self.add_widget(wid)

		self.start()

	def start(self):
		self.current = 'start'

	def dataBase(self):
		self.dataBaseWid.check_mem()
		self.current = 'database'
	
	def insert_data(self):
		self.insertDataWid.clear_widgets()
		wid = InsertDataWid(self)
		self.insertDataWid.add_widget(wid)
		self.current = 'insertdata'


class StartWid(BoxLayout):
	
	def __init__(self, mainwid, **kwargs):
		super().__init__(**kwargs)
		self.mainwid = mainwid

	def create_db(self):
		connect_db(self.mainwid.BD_PATH)
		self.mainwid.dataBase()


class DataBaseWid(BoxLayout):

	def __init__(self, mainwid, **kwargs):
		super().__init__(**kwargs)
		self.mainwid = mainwid

	def check_mem(self):
		self.ids.container.clear_widgets()
		wid = NewButton(self.mainwid)
		self.ids.container.add_widget(wid)


class InsertDataWid(BoxLayout):

	def __init__(self, mainwid, **kwargs):
		super().__init__(**kwargs)
		self.mainwid = mainwid

	def save(self):
		con = sqlite3.connect(self.mainwid.BD_PATH)
		cursor = con.cursor()
		id = self.ids.input_id.text
		nome = self.ids.input_nome.text
		marca = self.ids.input_marca.text
		valor = self.ids.input_valor.text
		sql = """
			INSERT INTO product(
					id, nome, marca, valor
				) VALUES (
					%s, '%s', '%s', %s
				)
		""" % (id, nome, marca, valor)
		try:
			cursor.execute(sql)
			con.commit()
		except Exception as e:
			print(e)
		finally:
			con.close()
	
	def back(self):
		print('236476587')
		self.mainwid.dataBase()


class NewButton(Button):

	def __init__(self, mainwid, **kwargs):
		super().__init__(**kwargs)
		self.mainwid = mainwid

	def create_product(self):
		self.mainwid.insert_data()


class MainApp(App):
	title = 'Inventário'
	
	def build(self):
		return MainWid()


if __name__ == '__main__':
	win = MainApp()
	win.run()


