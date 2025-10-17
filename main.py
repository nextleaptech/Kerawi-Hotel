from flask import Flask,render_template,redirect,url_for,request,flash
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,TextAreaField,SelectField
from wtforms.validators import DataRequired, Email,Length,Regexp
import smtplib
from dotenv import load_dotenv
import os


app = Flask(__name__)

load_dotenv()

"""Refer to the .env.example to create your own '.env' file"""
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
bootstrap = Bootstrap5(app)

email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')



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


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact",methods=["GET","POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        try:
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user=email,password=password)
                connection.sendmail(from_addr=email,
                                    to_addrs="sofi123man@gmail.com",
                                    msg=f"Subject:Contact form submission\n\n"
                                        f"From: {email}\n\nName:{form.name.data}\nEmail:{form.email.data}\nPhone:{form.phone.data}\nMessage:{form.message.data}")
            return redirect(url_for("contact",msg_sent="1"))
        except Exception:
            return redirect(url_for("contact",msg_sent="2"))
    msg_sent = request.args.get("msg_sent")
    return render_template("contact.html",form=form,msg_sent=msg_sent)

@app.route("/gallery")
def gallery():
    return render_template("gallery.html")

@app.route("/service")
def service():
    return render_template("service.html")

@app.route("/room")
def room():
    return render_template("room.html")

@app.route("/booking",methods=["GET","POST"])
def booking():
    form = BookingForm()
    if form.validate_on_submit():
        try:
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user=email, password=password)
                connection.sendmail(from_addr=email,
                                    to_addrs="sofi123man@gmail.com",
                                    msg=f"Subject: New Booking\n\n"
                                        f"Name: {form.name.data}\n"
                                        f"Email: {form.email.data}\n"
                                        f"Phone Number:{form.phone.data}\n"
                                        f"Check In: {form.checkin.data}\n"
                                        f"Check Out: {form.checkout.data}\n"
                                        f"Adults: {form.adults.data}\n"
                                        f"Children: {form.children.data}\n"
                                        f"Room: {form.room.data}\n"
                                        f"Special Request: {form.special_request.data}")
            return redirect(url_for("booking", msg_sent="1"))
        except Exception:
            return redirect(url_for("booking", msg_sent="2"))
    msg_sent = request.args.get("msg_sent")
    return render_template("booking.html", form=form, msg_sent=msg_sent)


@app.route("/newsletter",methods=["POST"])
def newsletter():
    if "newsletter_email" in request.form:
        referrer = request.referrer or url_for('home')
        try:
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user=email, password=password)
                connection.sendmail(from_addr=email,
                                    to_addrs="sofi123man@gmail.com",
                                    msg=f"Subject:Newsletter subscription\n\n"
                                        f"From: {email}\n\n{request.form["newsletter_email"]} has subscribed to the newsletter.\n\n")
            return redirect(f"{referrer}?newsletter_success=1")
        except Exception:
            return redirect(f"{referrer}?newsletter_success=2")
    return redirect(request.referrer or url_for('home'))





if __name__ == "__main__":
    app.run(debug=True)





