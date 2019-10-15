from app import app
from app import db
from app import corrspec, app_methods as am
from flask import render_template, flash, redirect, request, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length

from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Sample
from werkzeug.urls import url_parse
from bokeh.embed import components

from bokeh.io import output_file, show
from bokeh.models import BasicTicker, ColorBar, ColumnDataSource, LinearColorMapper, PrintfTickFormatter
from bokeh.plotting import figure
from bokeh.sampledata.unemployment1948 import data
from bokeh.transform import transform



from datetime import datetime
import pandas as pd

@app.before_request
def before_request():
    # get "last seen" time for a user when they sign in
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


class SampleForm(FlaskForm):
    # form for creating new samples
    name = TextAreaField('Sample name (required)',
            validators=[DataRequired(), Length(min=1, max=140)])
    composition = TextAreaField('Composition',
            validators=[Length(min=0, max=140)])
    fab_method = TextAreaField('Fabrication method',
            validators=[Length(min=0, max=140)])
    fab_date = TextAreaField('Fabrication date (YYYY-MM-DD) (required)',
            validators=[DataRequired(), Length(min=0, max=10)])
    notes = TextAreaField('Notes',
            validators=[Length(min=0, max=140)])
    experiments = TextAreaField('Experiments',
            validators=[Length(min=0, max=140)])
    ispublic = BooleanField('Visible to public')

    submit = SubmitField('Submit')


class ExperimentForm(FlaskForm):
    # form for creating new experiments
    exp_date = TextAreaField('Experiment date (YYYY-MM-DD) (required)',
            validators=[DataRequired(), Length(min=0, max=10)])
    experiment = TextAreaField('Experiment (required)',
            validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')


class EditProfileForm(FlaskForm):
    # form for editing the user profile
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('Information to display publicly',
                validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')


class RegistrationForm(FlaskForm):
    username = StringField('Publicly-displayed name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('8-digit pin', validators=[DataRequired()])
    password2 = PasswordField(

        'Repeat 8-digit pin', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('8-digit pin', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


'''
@app.route('/edit_sample', methods=['GET', 'POST'])
@login_required
def edit_sample():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)
'''



@app.route('/sample/<name>/add_experiment', methods=['GET', 'POST'])
@login_required
def add_experiment(name):
    form = ExperimentForm()
    sample = Sample.query.filter_by(name=name).first_or_404()
    if form.validate_on_submit():
        sample.experiment[str(form.exp_date.data)] = form.experiment.data
        db.session.commit()
        flash('Your experiment has been added.')
        return redirect(url_for('sample/<name>'))
    return render_template("samples.html", title='Add experiment',
        form=form)




@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@app.route('/analyze')
def analyze():
    return render_template('analyze.html', title='Data analysis')



@app.route('/corrspec')
def corrspec():
    return render_template('corrspec.html', script1='', div1='',
        title='Two-dimensional correlation spectroscopy')

@app.route('/upload_corrspec', methods=['GET', 'POST'])
def upload_corrspec():
    '''Page for uploading CSV files for 2D correlation spectroscopy.
    If the "Choose file" or "Upload"
    buttons are clicked on the HTML page, then 'request.method == 'POST'
    will run. This will check whether there is a valid CSV file uploaded
    and either plot it, or return an error message on the upload page.'''
    # default message for user trying to upload CSV file
    upload_info = {'message': ''}
    # if the upload form is submitted, try to read the CSV file

    if request.method == 'POST':
        try:
            file1 = request.files.get('file1')
            upload_info['file1'] = file1
            df1 = pd.read_csv(file1)
            
            '''
            if request.files.get('file2') == None:
                pass
            sy, asy, mean_df = corrspec(df1)
            '''
            print(df1)
            p = am.multiline_plot(df1, title=str(file1),
								xlabel='Point', ylabel='Values')
            #p = HeatMap(df1, title='My heatmap')
            print(p)
            script1, div1 = components(p)
            print(script1, div1)
            #script, div = '', ''
            #session['df'] = df
            # render the new uploaded_csv page which plots the CSV data
            return render_template('corrspec.html',
                              title='Data successfully uploaded',
                         upload_info=upload_info, script1=script1, div1=div1)

        # if there is an error with the CSV file, return to the upload page
        except:
            upload_info['message'] = 'Upload failed. Please choose valid CSV files and try again.'
            render_template('upload_corrspec.html', upload_info=upload_info,
                            title='Upload files for 2D correlation spectroscopy')


    return render_template('upload_corrspec.html',
                          title='Upload files for 2D correlation spectroscopy',
                           upload_info=upload_info)













@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    samples = user.samples
    return render_template('user.html', user=user, title=user.username, samples=samples)






@app.route('/users')
def users():
    userlist = User.query.all()
    return render_template('users.html', title='Users', userlist=userlist)

@app.route('/samples')
def samples():
	samples = Sample.query.all()
	return render_template('samples.html', title='Samples', samples=samples)


@app.route('/sample/<name>')
def sample(name):
    sample = Sample.query.filter_by(name=name).first_or_404()
    return render_template('sample.html', sample=sample, title=sample.name)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now registered.')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)



@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html', title='Welcome to Deeplab')




@app.route('/addsample', methods=['GET', 'POST'])
@login_required
def addsample():
    form = SampleForm()
    if form.validate_on_submit():
        sample = Sample(name=form.name.data,
                        composition=form.composition.data,
                        fab_method=form.fab_method.data,
                        fab_date=form.fab_date.data,
                        notes=form.notes.data,
                        experiments=form.experiments.data,
                        ispublic=form.ispublic.data,
                        author=current_user)
        db.session.add(sample)
        db.session.commit()
        flash('Your sample has been created.')
        return redirect(url_for('samples'))
    samples = Sample.query.all()
    return render_template("addsample.html", title='Home Page', form=form, samples=samples)

