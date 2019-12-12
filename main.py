
# -*- coding: utf-8 -*-

import os
import sqlite3
from kivy.app import App
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
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


class MessagePopup(Popup):
	pass
	

class MainWid(ScreenManager):
	
	def __init__(self, *args, **kwargs):
		super().__init__(**kwargs)
		self.APP_PATH = os.getcwd()
		self.DB_PATH = self.APP_PATH + '/db_sqlite3.db'
		self.startWid = StartWid(self)
		self.dataBaseWid = DataBaseWid(self)
		self.insertDataWid = InsertDataWid(self)    # BoxLayout()
		self.updateDataWid = BoxLayout()
		self.popup = MessagePopup()
		
		wid = Screen(name='start')
		wid.add_widget(self.startWid)
		self.add_widget(wid)
		
		wid = Screen(name='database')
		wid.add_widget(self.dataBaseWid)
		self.add_widget(wid)
		
		wid = Screen(name='insertdata')
		wid.add_widget(self.insertDataWid)
		self.add_widget(wid)
		
		wid = Screen(name='updatedata')
		wid.add_widget(self.updateDataWid)
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
	
	def update_data(self, data_id):
		self.updateDataWid.clear_widgets()
		wid = UpdateDataWid(self, data_id)
		self.updateDataWid.add_widget(wid)
		self.current = 'updatedata'


class StartWid(BoxLayout):
	
	def __init__(self, mainwid, **kwargs):
		super().__init__(**kwargs)
		self.mainwid = mainwid

	def create_db(self):
		connect_db(self.mainwid.DB_PATH)
		self.mainwid.dataBase()


class DataBaseWid(BoxLayout):

	def __init__(self, mainwid, **kwargs):
		super().__init__(**kwargs)
		self.mainwid = mainwid

	def check_mem(self):
		self.ids.container.clear_widgets()

		sql = """
				SELECT
					id, nome, marca, valor
				FROM
					product;
			"""
		try:
			con = sqlite3.connect(self.mainwid.DB_PATH)
			cursor = con.cursor()
			cursor.execute(sql)
			for i in cursor:
				win = DataWid(self.mainwid)
				row = 'ID: ' + str(100000000+i[0])[1:9] + '\n'
				row2 = i[1] + ', ' + i[2] + '\n'
				row3 = 'Preço por unidade: ' + str(i[3])
				win.data_id = str(i[0])
				win.data = row + row2 + row3
				self.ids.container.add_widget(win)
		except Exception as e:
			print(e)
		finally:
			con.close()
		
		wid = NewButton(self.mainwid)
		self.ids.container.add_widget(wid)


class UpdateDataWid(BoxLayout):

	def __init__(self, mainwid, data_id, **kwargs):
		super().__init__(**kwargs)
		self.mainwid = mainwid
		self.data_id = data_id
		self.check_mam()

	def check_mam(self):
		sql = """
				SELECT
					nome, marca, valor
				FROM
					product
				WHERE id = %s;
			""" % self.data_id
		try:
			con = sqlite3.connect(self.mainwid.DB_PATH)
			cursor = con.cursor()
			cursor.execute(sql)
			for i in cursor:
				self.ids.input_nome.text = i[0]
				self.ids.input_marca.text = i[1]
				self.ids.input_valor.text = str(i[2])
		except Exception as e:
			print(e)
		finally:
			con.close()

	def update(self):
		con = sqlite3.connect(self.mainwid.DB_PATH)
		cursor = con.cursor()
		nome = self.ids.input_nome.text
		marca = self.ids.input_marca.text
		valor = self.ids.input_valor.text
		data = (nome, marca, valor, self.data_id)
		sql = """
				UPDATE product
					SET	nome='%s', marca='%s', valor=%s
				WHERE id = %s
			""" % data
		if '' in data:
			message = self.mainwid.popup.ids.msg
			self.mainwid.popup.open()
			self.mainwid.popup.title = 'Database error'
			message.text = 'Um ou mais campos vazios'
		else:
			try:
				cursor.execute(sql)
				con.commit()
				self.mainwid.dataBase()
			except Exception as e:
				message = self.mainwid.popup.ids.msg
				self.mainwid.popup.open()
				self.mainwid.popup.title = 'Database error'
				message.text = str(e)
			finally:
				con.close()

	def deletar(self):
		con = sqlite3.connect(self.mainwid.DB_PATH)
		cursor = con.cursor()
		sql = """
			DELETE FROM product WHERE id=%s
		""" % self.data_id
		try:
			cursor.execute(sql)
			con.commit()
			self.mainwid.dataBase()
		except Exception as e:
			message = self.mainwid.popup.ids.msg
			self.mainwid.popup.open()
			self.mainwid.popup.title = 'Database error'
			message.text = str(e)
		finally:
			con.close()

	def close(self):
		self.mainwid.dataBase()


class InsertDataWid(BoxLayout):

	def __init__(self, mainwid, **kwargs):
		super().__init__(**kwargs)
		self.mainwid = mainwid

	def save(self):
		con = sqlite3.connect(self.mainwid.DB_PATH)
		cursor = con.cursor()
		id = self.ids.input_id.text
		nome = self.ids.input_nome.text
		marca = self.ids.input_marca.text
		valor = self.ids.input_valor.text
		data = (id, nome, marca, valor)
		sql = """
			INSERT INTO product(
					id, nome, marca, valor
				) VALUES (
					%s, '%s', '%s', %s
				)
		""" % data
		if '' in data:
			message = self.mainwid.popup.ids.msg
			self.mainwid.popup.open()
			self.mainwid.popup.title = 'Database error'
			message.text = 'Um ou mais campos vazios'
		else:
			try:
				cursor.execute(sql)
				con.commit()
				self.mainwid.dataBase()
			except Exception as e:
				message = self.mainwid.popup.ids.msg
				self.mainwid.popup.open()
				self.mainwid.popup.title = 'Database error'
				message.text = str(e)
			finally:
				con.close()
	
	def back(self):
		self.mainwid.dataBase()


class DataWid(BoxLayout):
	
	def __init__(self, mainwid, **kwargs):
		super().__init__(**kwargs)
		self.mainwid = mainwid

	def update(self, data_id):
		self.mainwid.update_data(data_id)


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


