from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ECE444_F2023'
bootstrap = Bootstrap(app)

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = StringField('What is your UofT email address?', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    email_utoronto = False  # Initialize as False initially
    form = NameForm()

    if form.validate_on_submit():
        old_name = session.get('name')
        old_email = session.get('email')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        if old_email is not None and old_email != form.email.data:
            flash('Looks like you have changed your email!')
        # Check if the email contains "utoronto"
        if "utoronto" in form.email.data:
            email_utoronto = True
        
        session['name'] = form.name.data
        session['email'] = form.email.data  

        #return redirect(url_for('index'))
    return render_template('index.html', name=session.get('name'), email = session.get('email'), email_utoronto=email_utoronto, form=form)

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.route('/clear_session')
def clear_session():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)



