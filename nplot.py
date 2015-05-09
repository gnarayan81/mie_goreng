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

import noodle_ui as nui
import signal_plot as sp

#***********************************************************************
# numpy and matplotlib tester.
if __name__ == '__main__':
	# the sample index.
	sample_index = np.arange(-45, 44, 1)
	# the sampling frequency.
	Fs = 1e4
	# the frequency.
	f = 1e2
	# the signal. 
	sine_signal = np.sin(2 * np.pi * (f/Fs) * sample_index)
	# Create a signals object and pass in the time-base
	sig = sp.Signals(sine_signal, sample_index)
	# Call plot on it.
	#sig.Plot()

	cosine_signal = np.cos(2 * np.pi * (f/Fs) * sample_index)

	nmw = nui.NoodleModeGUI("NMUI")
	nmw.AddRegisterToList("VarGain")
	nmw.AddRegisterToList("FixedGain")


	# Add a plot
	nmw.AddPlot(sample_index, sine_signal)
	nmw.RegisterUpdatePlot(sample_index, cosine_signal)

	nmw.Deploy()


