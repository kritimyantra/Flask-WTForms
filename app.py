from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class FormData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()


class MyForm(FlaskForm):
    name=StringField('Name', validators=[DataRequired()])
    email=StringField('Email', validators=[DataRequired(),Email()])

    def validate_email(self,field):
        existing_email = FormData.query.filter_by(email=field.data).first()
        if existing_email:
            raise ValidationError('Email already taken.')

    submit = SubmitField('Submit')

@app.route('/',methods=['GET','POST'])
def index():
    form = MyForm()
    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        # save into database
        form_data = FormData(name=name,email=email)
        db.session.add(form_data)
        db.session.commit()

        return 'Success'

    return render_template('index.html',form=form)

if __name__ == '__main__':
    app.run(debug=True)