from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length, Regexp
from dotenv import load_dotenv
import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

app = Flask(__name__)
load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
bootstrap = Bootstrap5(app)

# Brevo API setup
brevo_api_key = os.getenv('BREVO_API_KEY')
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = brevo_api_key
api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

# Hotel/admin email
ADMIN_EMAIL = "sofi123man@gmail.com"
SENDER_EMAIL = {"email": "merkebtech@gmail.com", "name": "Kerawi Hotel"}


# Forms
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


# Helper function to send user confirmation emails
def send_user_confirmation(user_name, user_email, subject_text, body_html):
    to = [{"email": user_email, "name": user_name}]
    send_email = sib_api_v3_sdk.SendSmtpEmail(
        to=to,
        sender=SENDER_EMAIL,
        subject=subject_text,
        html_content=body_html
    )
    try:
        api_instance.send_transac_email(send_email)
        print(f"✅ Confirmation email sent to {user_email}")
    except ApiException as e:
        print(f"Error sending user confirmation: {e}")


# Routes
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/menu")
def menu():
    return render_template("menu.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        subject = "Contact Form Submission"
        html_content_admin = f"""
        <h3>New Contact Message</h3>
        <p><strong>Name:</strong> {form.name.data}</p>
        <p><strong>Email:</strong> {form.email.data}</p>
        <p><strong>Phone:</strong> {form.phone.data}</p>
        <p><strong>Message:</strong> {form.message.data}</p>
        """
        send_email_admin = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": ADMIN_EMAIL}],
            sender=SENDER_EMAIL,
            subject=subject,
            html_content=html_content_admin
        )
        try:
            api_instance.send_transac_email(send_email_admin)

            # Send confirmation to user
            subject_user = "We Received Your Message!"
            html_user = f"""
            <p>Hi {form.name.data},</p>
            <p>Thank you for contacting Kerawi Hotel! We have received your message and will get back to you shortly.</p>
            <p>Warm regards,<br>Kerawi Hotel Team</p>
            """
            send_user_confirmation(form.name.data, form.email.data, subject_user, html_user)

            return redirect(url_for("contact", msg_sent="1"))
        except ApiException as e:
            print(f"Error sending Brevo email: {e}")
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


@app.route("/booking", methods=["GET", "POST"])
def booking():
    form = BookingForm()
    if form.validate_on_submit():
        subject = "New Booking Request"
        html_content_admin = f"""
        <h3>New Booking</h3>
        <p><strong>Name:</strong> {form.name.data}</p>
        <p><strong>Email:</strong> {form.email.data}</p>
        <p><strong>Phone:</strong> {form.phone.data}</p>
        <p><strong>Check In:</strong> {form.checkin.data}</p>
        <p><strong>Check Out:</strong> {form.checkout.data}</p>
        <p><strong>Adults:</strong> {form.adults.data}</p>
        <p><strong>Children:</strong> {form.children.data}</p>
        <p><strong>Room:</strong> {form.room.data}</p>
        <p><strong>Special Request:</strong> {form.special_request.data}</p>
        """
        send_email_admin = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": ADMIN_EMAIL}],
            sender=SENDER_EMAIL,
            subject=subject,
            html_content=html_content_admin
        )
        try:
            api_instance.send_transac_email(send_email_admin)

            # Send confirmation to user
            subject_user = "We Received Your Booking!"
            html_user = f"""
            <p>Hi {form.name.data},</p>
            <p>Thank you for booking with Kerawi Hotel! We have received your request and will contact you shortly to confirm your booking.</p>
            <p>Warm regards,<br>Kerawi Hotel Team</p>
            """
            send_user_confirmation(form.name.data, form.email.data, subject_user, html_user)

            return redirect(url_for("booking", msg_sent="1"))
        except ApiException as e:
            print(f"Error sending Brevo email: {e}")
            return redirect(url_for("booking", msg_sent="2"))

    msg_sent = request.args.get("msg_sent")
    return render_template("booking.html", form=form, msg_sent=msg_sent)


@app.route("/newsletter", methods=["POST"])
def newsletter():
    if "newsletter_email" in request.form:
        referrer = request.referrer or url_for("home")
        html_content_admin = f"<p>New subscription: <strong>{request.form['newsletter_email']}</strong></p>"
        send_email_admin = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": ADMIN_EMAIL}],
            sender=SENDER_EMAIL,
            subject="New Newsletter Subscription",
            html_content=html_content_admin
        )
        try:
            api_instance.send_transac_email(send_email_admin)

            # Confirmation to subscriber
            subject_user = "Thank You for Subscribing!"
            html_user = f"""
            <p>Hi,</p>
            <p>Thank you for subscribing to Kerawi Hotel newsletter! You will receive our latest updates and offers soon.</p>
            <p>Warm regards,<br>Kerawi Hotel Team</p>
            """
            send_user_confirmation(request.form['newsletter_email'], request.form['newsletter_email'], subject_user, html_user)

            return redirect(f"{referrer}?newsletter_success=1")
        except ApiException as e:
            print(f"Error sending newsletter email: {e}")
            return redirect(f"{referrer}?newsletter_success=2")

    return redirect(request.referrer or url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
