# -*- coding: utf-8 -*-

import sys, os, textwrap
#from time import time, sleep

try:
  import Tkinter              # Python 2
  import ttk
  from Tkinter import *
except ImportError:
  import tkinter as Tkinter   # Python 3
  from tkinter import *
  import tkinter.ttk as ttk

#path="\\".join(sys.argv[0].split("\\")[:-1])+"\\"
path = ""

window=None

class widgets:pass
class widgets2:pass
class nav_widgets:pass
class widgets_master:pass

class question_widgets:pass
class question_widgets_master:pass
question_widgets_master.widgets_lists = dict()

DEFAULTENCODING = "utf-8"

def u(s):
	return unicode(s)
	
def readFile(path):
	s = ""
	try:
		s = open(path, "rb").read().decode(DEFAULTENCODING)
	except:
		print("readFile: %s" % (sys.exc_info()[1]))
		
	return u(s)

env = dict(os.environ)
env["PYTHONIOENCODING"] = DEFAULTENCODING
_CURRENT_QUESTION = 0
_QUESTION_NUMBER = 2

#TEST_LABEL = open("res/lab1.txt", "rb").read().decode("u8")
#TEST_LABEL2 = open("res/lab1.txt", "rb").read().decode("u8")
TEST_LABEL = readFile("res/lab1.txt")
TEST_LABEL2 = readFile("res/lab2.txt")
TEST_LABEL3 = readFile("res/lab3.txt")

class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master=master
        pad=3
        self._geom='200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.bind('<Escape>',self.toggle_geom)            
    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom

class FullScreenWidthApp(object):
    def __init__(self, master, **kwargs):
        self.master=master
        pad=3
        self._geom='200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            int(window.winfo_screenwidth()*0.9)-pad, master.screenheight))
        master.bind('<Escape>',self.toggle_geom)            
    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom
		
def pack_widgets(object):
	try:
		for obj in iter(object):
			[getattr(getattr(obj,i),"pack")() for i in dir(obj) if hasattr(getattr(obj, i), "pack")]
	except TypeError, te:
		[getattr(getattr(object,i),"pack")() for i in dir(object) if hasattr(getattr(object, i), "pack")]

def pack_forget_widgets(object):
	[getattr(getattr(object,i),"pack_forget")() for i in dir(object) if hasattr(getattr(object, i), "pack_forget")]

def grid_widgets(object):
	try:
		for obj in iter(object):
			count = 0
			for i in dir(obj):
				if hasattr(getattr(obj, i), "grid"):
					getattr(getattr(obj,i),"grid")(row=count, column=0, sticky="W")
				count += 1
	except TypeError, te:
		count = 0
		for i in dir(obj):
			if hasattr(getattr(obj, i), "grid"):
				getattr(getattr(obj,i),"grid")(row=count, column=0, sticky="W")
			count += 1

def grid_forget_widgets(object):
	[getattr(getattr(object,i),"grid_forget")() for i in dir(object) if hasattr(getattr(object, i), "grid_forget")]


def process_question(current_question, prev_question = -1):
	if prev_question != -1: # if has previous question
		question_widgets_master.widgets_lists[prev_question].w_main_lab.pack_forget()
		question_widgets_master.widgets_lists[prev_question].w_main_frame.pack_forget()
		
	if current_question in question_widgets_master.widgets_lists.keys():
		print("%d is in question_widgets_master.widgets_lists.keys()  = %s, loading the main frame..." 
			% (current_question, str(question_widgets_master.widgets_lists.keys())))
		question_widgets_master.widgets_lists[current_question].w_main_lab.pack()
		question_widgets_master.widgets_lists[current_question].w_main_frame.pack()
		return
	
	path = "res/q%d.txt" % (current_question + 1)	
	if not os.path.exists(path):
		print("%s doesn't exist, bailing away..." % (path))
		return
		
	Q = readFile(path)
	count, label_count = 0, 0
	question_frame = Frame()
	question_widgets.w_main_frame = question_frame
	question_widgets.w_main_lab=Tkinter.Label(window, 
		text=TEST_LABEL3, wraplength=(window.winfo_screenwidth()*0.8-3), justify = CENTER)
			
	question_widgets.w_main_lab.pack(side = TOP)
	for line in Q.split("\n"):
		line = line.replace("\r", "")
		if (count > 0):
			try:
				question, answer_form = line[:-1], line[-1]
			except:
				print("%s: unexpected empty line, skipping" % (path))
				continue
		else:
			question = line

		text_lines_count = 0

		# title
		if count == 0:
			label = Tkinter.Label(question_frame, text = question)
			setattr(question_widgets, "w_first_label", label)
			label.grid(row=label_count, column=0, sticky="W")
			label_count += 1
		else:
			for text_line in textwrap.wrap(question, width=int(window.winfo_screenwidth()/12)):
				if (text_lines_count > 0):
					text_line = "     " + text_line
				label = Tkinter.Label(question_frame, text=text_line)
				setattr(question_widgets, "w%s_%d_label" % (str(count).zfill(3), text_lines_count), label)
				label.grid(row=label_count, column=0, sticky="W")

				# if first question line
				if (text_lines_count == 0):
					entry = Entry(question_frame, width=1, bd=1)
					setattr(question_widgets, "w%s_entry" % (str(count).zfill(3)), entry)
					entry.grid(row = label_count, column=1)
				text_lines_count += 1
				label_count += 1
		count += 1
	question_widgets_master.widgets_lists[current_question]=question_widgets
	question_widgets_master.widgets_lists[current_question].w_main_frame.pack()

def next_question(event):
	global _CURRENT_QUESTION
	
	if (_CURRENT_QUESTION < _QUESTION_NUMBER - 1):
		_CURRENT_QUESTION += 1
		process_question(_CURRENT_QUESTION, _CURRENT_QUESTION - 1)
		nav_widgets.forward.bind('<Button-1>', next_question)
	else:
		nav_widgets.forward.config(state = "disabled")
		nav_widgets.forward.unbind('<Button-1>')

def prev_question(event):
	global _CURRENT_QUESTION
	
	if (_CURRENT_QUESTION > 0):
		_CURRENT_QUESTION -= 1
		if (nav_widgets.forward.cget("state") != "normal" and _QUESTION_NUMBER > 1):
			nav_widgets.forward.config(state = "normal")
			nav_widgets.forward.bind('<Button-1>', next_question)
	else:
		nav_widgets.backward.bind('<Button-1>', start_app)
	
	process_question(_CURRENT_QUESTION, _CURRENT_QUESTION - 1)
	
def second_window(event):
	global window

	pack_forget_widgets(widgets)
	nav_widgets.backward.config(state = "normal")
	nav_widgets.backward.bind('<Button-1>', start_app)
	nav_widgets.forward.bind('<Button-1>', next_question)

	process_question(_CURRENT_QUESTION)
	
def start_app(event):
	global window
	
	print("current path: %s" % path)
	if (window == None):
		widgets_master.widgets_lists = [widgets]
		
		window=Tkinter.Tk()
		window.screenheight = int(window.winfo_screenheight()*0.7)
		FullScreenWidthApp(window)
	
		widgets.w00_main_frame = Frame(window, borderwidth = 2)
		widgets.w01_lab=Tkinter.Label(widgets.w00_main_frame, 
			text=TEST_LABEL, wraplength=(window.winfo_screenwidth()*0.85-3), justify = CENTER)
		
		widgets.w02_lab=Tkinter.Label(widgets.w00_main_frame, 
			text=TEST_LABEL2, wraplength=(window.winfo_screenwidth()*0.85-3), justify = LEFT)
		#widgets.w02_ent=Tkinter.Entry(window, width=20,bd=3)
		#widgets.w02_ent.insert(END, user_name)
	
		nav_widgets.nav_frame = Frame(window, borderwidth = 2)
		nav_widgets.nav_frame.pack(side = BOTTOM)
		
		nav_widgets.backward=Tkinter.Button(nav_widgets.nav_frame, text="Назад", state = "disabled", width=20, height=1, bg="grey", fg="black")
		nav_widgets.forward=Tkinter.Button(nav_widgets.nav_frame, text="Вперед", width=20, height=1, bg="grey", fg="black")
		nav_widgets.forward.bind('<Button-1>', second_window)
		nav_widgets.backward.pack(side = LEFT)
		nav_widgets.forward.pack(side = RIGHT)
	
		pack_widgets(widgets)
		#show_widgets()
		#window.geometry('x400+0+0')
		#widgets.w01_lab.config()
	
		window.mainloop()
	else:
		question_widgets_master.widgets_lists[_CURRENT_QUESTION].w_main_frame.pack_forget()
		question_widgets_master.widgets_lists[_CURRENT_QUESTION].w_main_lab.pack_forget()
		pack_widgets(widgets)
		nav_widgets.backward.unbind('<Button-1>')
		nav_widgets.backward.config(state = "disabled")
		
start_app(None)