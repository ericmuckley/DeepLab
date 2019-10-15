import glob
import serial
import sys
import numpy as np
import pandas as pd
from scipy.interpolate import splrep
from scipy.interpolate import splev
import numpy.polynomial.polynomial as poly

from bokeh.plotting import figure

def multiline_plot(df, title='Title', xlabel='X', ylabel='Y'):
	''' Create bokeh line plot with multiple features from a
		pandas dataframe.'''
	# set up plot
	colors = ['red', 'blue', 'green', 'orange', 'black',
				'grey', 'yellow']*100
	p = figure(width=500, height=300, title=title, x_axis_label=xlabel,
				y_axis_label=ylabel, tools="box_zoom,reset")
	p.toolbar.logo = None
	p.title.text_font_size = '9pt'
	p.xaxis.axis_label_text_font_size = "9pt"
	p.yaxis.axis_label_text_font_size = "9pt"
	p.xaxis.major_label_text_font_size = "9pt"
	p.yaxis.major_label_text_font_size = "9pt"
	p.xaxis.axis_label_text_font_style = "normal"
	p.yaxis.axis_label_text_font_style = "normal"
	if len(df.columns) > 1:
		# loop over each column in the dataframe and add to plot
		for col in range(1, len(df.columns)):
			p.line(df.iloc[:, 0], df.iloc[:, col], line_color=colors[col],
					line_width=3, legend=df.columns[col], alpha=0.8,
					muted_color=colors[col], muted_alpha=0.1)
	if len(df.columns) == 1:
		# if only 1 column, plot that column
		p.line(np.arange(len(df)), df.iloc[:, 0], line_color='blue',
			line_width=3, legend=df.columns[0], alpha=0.8,
				muted_color='blue', muted_alpha=0.1)

	#p.legend.location = "bottom_left"
	p.legend.click_policy = "mute"
	p.toolbar.active_drag = None
	return p



def list_serialports():
	''' List serial port names using PySerial. Raises EnvironmentError on
		unsupported or unknown platforms. Returns a list of the serial
		ports available on the system.'''
	if sys.platform.startswith('win'):
		ports = ['COM%s' % (i + 1) for i in range(256)]
	elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
		# this excludes your current terminal "/dev/tty"
		ports = glob.glob('/dev/tty[A-Za-z]*')
	elif sys.platform.startswith('darwin'):
		ports = glob.glob('/dev/tty.*')
	else:
		raise EnvironmentError('Unsupported platform')
	result = []
	for port in ports:
		try:
			s = serial.Serial(port)
			s.close()
			result.append(port)
		except (OSError, serial.SerialException):
			pass
	return result





def resample_array(arr, new_len=100,
		new_xlims=None, vec_scale='lin', k=3, s=0):
    '''
    Resamples (stetches/compresses) a 2D array by using a spline fit.
    Array should be shape [[x1, y1, ...ym], ...[xn, yn, ...yn]] where the
    # first column in array is x-values and following next columns are
    y values. If no x values exist, insert column np.arange(len(arr))
    as x values.
    Accepts linear or log x-values, and new x_limits.
    k and s are degree and smoothing factor of the interpolation spline.
    '''
    # first, check whether array should be resampled using
    # a linear or log scale:
    if vec_scale == 'lin':
        new_scale = np.linspace
    if vec_scale == 'log':
        new_scale = np.geomspace
    # get new x-limits for the resampled array
    if new_xlims is None:
        new_x1, new_x2 = arr[0, 0], arr[-1, 0]
    else:
        new_x1, new_x2 = new_xlims[0], new_xlims[1]
    # create new x values
    arrx = new_scale(new_x1, new_x2, new_len)
    # create new empty array to hold resampled values
    stretched_array = np.zeros((new_len, len(arr[0])))
    stretched_array[:, 0] = arrx 
    # for each y-column, calculate parameters of degree-3 spline fit
    for col in range(1, len(arr[0])):
        spline_params = splrep(arr[:, 0], arr[:, col], k=int(k), s=s)
        # calculate spline at new x values
        arry = splev(arrx, spline_params)
        # populate stretched data into resampled array
        stretched_array[:, col] = arry
    return stretched_array









def compare_polyfits(
    x, y, x_new=None, fits=['poly1', 'poly2', 'poly3', 'spline'], s=0):
    '''
    Compares least squares fits to x and y ordered pairs.
    Performs fits at x_new points. The fits argument is a
    list of strings which indicate which fits to compare.
    fits = [
        'poly1' = degree 1 polynomial (linear) fit 
        'poly2' = degree 2 polynomial (quadratic) fit
        'poly3' = degree 3 polynomial fit
        'spline' = B-spline fit
            ]
    s = smoothing factor for the spline fit
    '''
    # if new x values are not passed, use original x values
    if x_new is None:
        x_new = x
    # create dictionary to hold fits
    fit_dic = {}
    # perform fits
    if 'poly1' in fits:
        poly1coefs = poly.polyfit(x, y, 1)
        poly1fit = poly.polyval(x_new, poly1coefs)
        fit_dic['poly1'] = poly1fit
    if 'poly2' in fits:
        poly2coefs = poly.polyfit(x, y, 2)
        poly2fit = poly.polyval(x_new, poly2coefs)
        fit_dic['poly2'] = poly2fit
    if 'poly3' in fits:
        poly3coefs = poly.polyfit(x, y, 3)
        poly3fit = poly.polyval(x_new, poly3coefs)
        fit_dic['poly3'] = poly3fit
    if 'spline' in fits:
        spline_params = splrep(x, y, s=s, k=3)
        splinefit = splev(x_new, spline_params)
        fit_dic['spline'] = splinefit
    return fit_dic
