from flask_wtf import FlaskForm
from wtforms import FileField, StringField, HiddenField, PasswordField, SelectField, RadioField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, NumberRange, Email
from .models import Utilisateur

class LoginForm(FlaskForm):
    email = StringField('Adresse email')
    password = PasswordField('Mot de passe')
    password_incorrect = ""
    next = HiddenField()

    def get_authenticated_user(self):
        user = Utilisateur.query.filter_by(email_util=self.email.data).first()
        if user and user.mdp_util == self.password.data:
            return user
    
    def has_content(self):
        return self.password.data != "" or self.email.data != ""
    
    def show_password_incorrect(self):
        self.password_incorrect = "Email ou mot de passe incorrect"

class ModificationForm(FlaskForm):
    firstname = StringField('Prénom', validators=[DataRequired()])
    lastname = StringField('Nom', validators=[DataRequired()])
    email = StringField('Adresse mail', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe')

