from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html', title='Welcome to Deeplab')

@app.route('/allsamples')
def allsamples():
	samples = ['a', 'b', 'c', 'd']
	return render_template('allsamples.html', title='All samples',
		samples=samples)
