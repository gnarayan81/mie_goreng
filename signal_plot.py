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

#***********************************************************************
class Signals:
	# establish a signal baseline.
	signal = np.array(np.arange(1, 5))
	time_axis = np.array([0])
	
	# construct some signal
	def __init__(self, signal, time_axis = np.array([0])):
		# Do some typecheck.
		if isinstance(signal, np.ndarray) == False:
			print "Wrong type! Signal should be a numpy.ndarray object!"
			exit(-1)
			
		if isinstance(time_axis, np.ndarray) == False:
			print "Wrong type! time_axis should be a numpy.ndarray object!"
			exit(-1)			
		# otherwise, copy the signal.
		self.signal = signal
		# ... and the axis
		self.time_axis = time_axis
	# plot
	def Plot(self, show_grid = True):
		# Call the matplotlib plotter.
		if self.time_axis.size <= 1:
			self.time_axis = np.arange(0, self.signal.size)
			
		plt.plot(self.time_axis, self.signal)
		# show grid if true
		if show_grid == True:
			plt.grid(True)
		plt.show()		
