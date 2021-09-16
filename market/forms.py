from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User


class RegisterForm(FlaskForm):

    def validate_email_address(self, email_address_to_check: str):
        check_email = User.query.filter_by(email_address=email_address_to_check.data).first()
        if check_email:
            raise ValidationError('This email already exists')

    def validate_username(self, username_to_check: str):
        check_user = User.query.filter_by(username=username_to_check.data).first()
        if check_user:
            raise ValidationError('This username already exists')

    username = StringField(label='Username', validators=[Length(min=2, max=20), DataRequired()])
    email_address = StringField(label='Email', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password', validators=[Length(min=3), DataRequired()])
    password2 = PasswordField(label='Confirm Password', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')
