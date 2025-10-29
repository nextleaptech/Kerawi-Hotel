from flask import Flask, render_template, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length, Regexp
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os
import traceback

app = Flask(__name__)
load_dotenv()

"""Refer to the .env.example to create your own '.env' file"""
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
bootstrap = Bootstrap5(app)

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('EMAIL')
app.config['MAIL_PASSWORD'] = os.getenv('PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('EMAIL')

mail = Mail(app)

email = os.getenv('EMAIL')

class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone = StringField("Phone Number", validators=[DataRequired(), Length(min=10, max=15)])
    message = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField("Send")

class BookingForm(FlaskForm):
    name = StringField("Your Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone = StringField("Phone Number", validators=[
        DataRequired(),
        Length(min=10, max=15),
        Regexp(r'^\+?\d+$', message="Enter a valid phone number")
    ])
    checkin = StringField("Check In", validators=[DataRequired()])
    checkout = StringField("Check Out", validators=[DataRequired()])
    adults = SelectField("Adults", choices=[("1", "1"), ("2", "2"), ("3", "3")], validators=[DataRequired()])
    children = SelectField("Children", choices=[("0", "0"), ("1", "1"), ("2", "2")])
    room = SelectField("Room", choices=[("1", "Room 1"), ("2", "Room 2"), ("3", "Room 3")], validators=[DataRequired()])
    special_request = TextAreaField("Special Request", validators=[Length(max=200)])
    submit = SubmitField("Book Now")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/menu")
def menu():
    return render_template("menu.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET","POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        try:
            msg = Message(
                "Contact form submission",
                recipients=["sofi123man@gmail.com"]
            )
            msg.body = f"From: {email}\n\nName: {form.name.data}\nEmail: {form.email.data}\nPhone:{form.phone.data}\nMessage:{form.message.data}"
            mail.send(msg)
            return redirect(url_for("contact", msg_sent="1"))
        except Exception:
            print(traceback.format_exc())
            return redirect(url_for("contact", msg_sent="2"))
    msg_sent = request.args.get("msg_sent")
    return render_template("contact.html", form=form, msg_sent=msg_sent)

@app.route("/gallery")
def gallery():
    return render_template("gallery.html")

@app.route("/service")
def service():
    return render_template("service.html")

@app.route("/room")
def room():
    return render_template("room.html")

@app.route("/booking", methods=["GET","POST"])
def booking():
    form = BookingForm()
    if form.validate_on_submit():
        try:
            msg = Message(
                "New Booking",
                recipients=["sofi123man@gmail.com"]
            )
            msg.body = f"Name: {form.name.data}\nEmail: {form.email.data}\nPhone Number:{form.phone.data}\nCheck In: {form.checkin.data}\nCheck Out: {form.checkout.data}\nAdults: {form.adults.data}\nChildren: {form.children.data}\nRoom: {form.room.data}\nSpecial Request: {form.special_request.data}"
            mail.send(msg)
            return redirect(url_for("booking", msg_sent="1"))
        except Exception:
            return redirect(url_for("booking", msg_sent="2"))
    msg_sent = request.args.get("msg_sent")
    return render_template("booking.html", form=form, msg_sent=msg_sent)

@app.route("/newsletter", methods=["POST"])
def newsletter():
    if "newsletter_email" in request.form:
        referrer = request.referrer or url_for('home')
        try:
            msg = Message(
                "Newsletter subscription",
                recipients=["sofi123man@gmail.com"]
            )
            msg.body = f"From: {email}\n\n{request.form['newsletter_email']} has subscribed to the newsletter."
            mail.send(msg)
            return redirect(f"{referrer}?newsletter_success=1")
        except Exception:
            return redirect(f"{referrer}?newsletter_success=2")
    return redirect(request.referrer or url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
