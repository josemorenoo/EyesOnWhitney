import smtplib, ssl

sender_email = "jmorenodev1@gmail.com"
receiver_email = "josemoreno181818@gmail.com"
message = """\
Subject: Hi there

This message is sent from Python. Cool."""

password = input("Type your password and press enter: ")

smtp_server = "smtp.gmail.com"
context = ssl.create_default_context()
with smtplib.SMTP(smtp_server, port = 587) as server:
    server.ehlo()  # Can be omitted
    server.starttls(context=context)
    server.ehlo()  # Can be omitted
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)