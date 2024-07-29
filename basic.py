from flask import Flask, redirect , url_for, render_template, request
from flask_wtf import FlaskForm # type: ignore
from wtforms import StringField,SubmitField # type: ignore

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretflask'

class InfoForm(FlaskForm):
    breed = StringField("What breed are you?")
    submit = SubmitField('Submit')


@app.route("/", methods=['GET','POST'])
def home():
    
    breed = False
    form = InfoForm()
    if form.validate_on_submit():
        breed = form.breed.data
        form.breed.data = ''
    return render_template('formindex.html',form=form,breed=breed)

if __name__ == '__main__':
    app.run(debug= True)