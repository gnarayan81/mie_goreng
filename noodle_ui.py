#########################################################################
# The MIT License (MIT)

# Copyright (c) 2015 Gopal Narayanan

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#########################################################################

import numpy as np
import matplotlib.pyplot as plt

import Tkinter as tk

import matplotlib as mplb
mplb.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler

import time

#***********************************************************************
# GUI.
class NoodleModeGUI:
	root = None
	root_title = ""
	root_frame = None
	canvas = None
	
	# Register list.
	register_list = None
	register_index = 0
	register_select_cb = None
	# Plot
	plot_figure = None
	subplot_handle = None
	canvas_handle = None
	# Plot update on select
	update_signal = None
	update_timebase = None
	persistence_requested = False
	
	selected_register = None
	selected_reg_index = 0
	# Description window frame.
	description_window_frame = None
	desc_window_bits = None
	desc_window_read = None # Read button
	desc_rw_frame = None
	desc_bitfield_frame = None
	
	# select a register.
	selected_reg_label = None
	selected_reg_stringvar = None
	reg_value_entry = None
	description_text = None
		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	# Create a noodle-mode register description.
	def __GenRegisterDescriptionWindow(self):

		selected_reg_frame = tk.Frame(self.canvas, borderwidth=3)
		selected_reg_frame.place(y=520, x=10)
		label_reg = tk.Label(selected_reg_frame, text="Selected Register: ").grid(row=0,column=0)
		
		self.selected_reg_stringvar = tk.StringVar()
		self.selected_reg_label = tk.Label(selected_reg_frame, 
		textvariable=self.selected_reg_stringvar).grid(row=0,column=1)
		self.selected_reg_stringvar.set("<NONE>")
		# Now the value field.
		self.reg_value_entry = tk.Entry(selected_reg_frame)
		self.reg_value_entry.grid(row=0, column=2)
		self.reg_value_entry.insert(10, '0xDEADBEEF')
		
		self.desc_window_read = tk.Button(selected_reg_frame, text = "RD").grid(row=0, column=3)
		self.desc_window_read = tk.Button(selected_reg_frame, text = "WR").grid(row=0, column=4)
		
		## Now the description box.
		description_frame = tk.Frame(self.canvas, borderwidth=3)
		description_frame.place(x=600, y=520) 
		description_label = tk.Label(description_frame, text = "Description").grid(row=0, column=0)
		self.description_text = tk.Text(description_frame, height=5.5, width=58)
		self.description_text.grid(row=1, column=0)
		self.description_text.insert(tk.INSERT, "Fill this in whenever, from here... ")
		self.description_text.insert(tk.END, "\n\n... to here.")
		
		self.desc_bitfield_frame = tk.Frame(self.canvas, relief=tk.SUNKEN, borderwidth=3)
		self.desc_bitfield_frame.place(y=560, x=10)
		desc_bitfield_frame_bot = tk.Frame(self.canvas, relief=tk.SUNKEN, borderwidth=3)
		desc_bitfield_frame_bot.place(y=590, x=10)
		self.desc_window_bits = [tk.Button(self.desc_bitfield_frame, text = '0', height=1, width=1)]
		self.desc_window_bits[0].pack(side=tk.RIGHT, fill=tk.NONE, expand=tk.YES)
		for i in range(1, 16):
			self.desc_window_bits = \
			self.desc_window_bits + [tk.Button(self.desc_bitfield_frame, text = '0', height=1, width=1)]
			self.desc_window_bits[i].pack(side=tk.RIGHT, fill=tk.NONE, expand=tk.YES)
			
		for i in range(16, 32):
			self.desc_window_bits = \
			self.desc_window_bits + [tk.Button(desc_bitfield_frame_bot, text = '0', height=1, width=1)]
			self.desc_window_bits[i].pack(side=tk.RIGHT, fill=tk.NONE, expand=tk.YES)			
	
	
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	# Create the basic frame and primary widgets.
	def __init__(self, title = "YcNoodleMode GUI"):
		self.root = tk.Tk()
		self.root.wm_title(title)
		self.root.resizable(0,0)
		
		self.canvas = tk.Canvas(self.root, width=1024,height=650)
		self.canvas.pack(expand=tk.YES,fill=tk.BOTH)		
		self.root_frame = tk.Frame(self.canvas)
		self.root_frame.place(x=10,y=10)
		self.root_frame.pack_propagate(1)
		
		self.register_list = tk.Listbox(self.root_frame, relief=tk.SUNKEN, borderwidth=3, height=31, width=30)
		self.register_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)
		self.register_list.bind('<<ListboxSelect>>', self.__ListSelectionFunctional)
		self.__GenRegisterDescriptionWindow()
	
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	# Add a register to the list.
	def AddRegisterToList(self, register, at=-1):
		if at != -1:
			self.register_list.insert(at, register)
		else:
			self.register_index = self.register_index + 1
			self.register_list.insert(self.register_index, register)
			
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	# Private method: List selection callback.
	def __ListSelectionFunctional(self, event):
		w = event.widget
		index = int(w.curselection()[0])
		value = w.get(index)
		print 'Your selection was %s' % value
		
		self.selected_register = value
		self.selected_reg_index = index
		
		self.selected_reg_stringvar.set(value)
		
		if self.persistence_requested == False:
			self.subplot_handle.clear()
			self.subplot_handle.grid(True)
		self.subplot_handle.plot(self.update_timebase, self.update_signal)
		self.canvas_handle.show()	
					
			
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	# Register a list selection callback. This is a Tcl/Tk Virtual event. 
	# http://www.tcl.tk/man/tcl8.5/TkCmd/event.htm#M41]
	# http://stackoverflow.com/questions/6554805/getting-a-callback-when-a-tkinter-listbox-selection-is-changed
	def RegisterListSelectCB(self, cb):
		self.register_list.bind('<<ListboxSelect>>', cb)
	
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	# Add a plot.	
	def AddPlot(self, timebase, signal):
		self.plot_figure = plt.Figure(figsize=(7,4.5), dpi=100)
		self.subplot_handle = self.plot_figure.add_subplot(111)
		self.subplot_handle.plot(timebase, signal)
		self.subplot_handle.grid(True)
		
		plot_frame = tk.Frame(self.canvas, relief=tk.SUNKEN, borderwidth=3)
		plot_frame.place(x=300, y=10)
		self.canvas_handle = FigureCanvasTkAgg(self.plot_figure, master=plot_frame)
		self.canvas_handle.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=tk.YES)

		toolbar = NavigationToolbar2TkAgg(self.canvas_handle, plot_frame)
		toolbar.update()
		self.canvas_handle._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)		
		
		self.canvas_handle.show()
		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	# Update plot. 
	def RegisterUpdatePlot(self, timebase, signal, persistent=False):
		self.update_signal = signal
		self.update_timebase = timebase
		self.persistence_requested = persistent
				
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	# Deploy.
	def Deploy(self):
		self.root.mainloop()
