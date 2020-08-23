#!/usr/bin/python3

import os
import sys
import tkinter as tk
from tkinter import filedialog

if sys.version_info[0] < 3:
	raise Exception("Must be using Python 3")

import tkinter as tk

class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		self.pack()
		self.create_widgets()

	def create_widgets(self):
		self.dir_path_text = tk.Text(self, height=2, width=30)
		self.dir_path_text.pack()
		self.dir_select_button = tk.Button(self)
		self.dir_select_button["text"] = "..."
		self.dir_select_button["command"] = self.select_dir
		self.dir_select_button.pack(side="top")

		self.quit = tk.Button(self, text="QUIT", fg="red",
							  command=self.master.destroy)
		self.quit.pack(side="bottom")

	def select_dir(self):
		self.dir_path = filedialog.askdirectory()
		self.dir_path_text.insert(tk.END, self.dir_path)
		

root = tk.Tk()
app = Application(master=root)
app.mainloop()