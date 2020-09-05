import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random

sender_email = "jmorenodev1@gmail.com"

def send_word_at_once(people: list, permits_available: str):
    smtp_server = "smtp.gmail.com"
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port = 587) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, 'eyesonwhitney')
        for receiver_email in people:
            message = create_email_message(permits_available, receiver_email)
            server.sendmail(sender_email, receiver_email, message)

def create_email_message(permits_available: str, receiver_email) -> str:
    message = MIMEMultipart("alternative")
    message["Subject"] = "WHITNEY ALERT! (TEST)"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = """\
    This is a Whitney Permit Alert! You're not tripping! Hurry!
    {}
    """.format(permits_available)

    html = """\
    <html>
    <body>
        <div>
            <b>This is a Whitney Permit Alert! You're not tripping! Hurry!</b>
            <p>The following dates are available:</p>
            <br><div style="white-space: pre">
                <p>{}</p>
            </div>
            <div style="text-align: left">
                <a href="https://www.recreation.gov/permits/233260" style="font-size: 30px">Click here to reserve on recreation.gov</a> 
            </div><br>
        </div>
    <img src="https://i.pinimg.com/originals/54/20/5c/54205c11d55a1a5d09085687982edff0.jpg" />
    <!-- this span ensures Gmail doesn't trim the email -->
    <span style="opacity: 0"> {} </span>
    </body>
    </html>
    """.format(permits_available, random.random())

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)
    return message.as_string()
