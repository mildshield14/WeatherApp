class EmailSending:
    def __init__(self, data):
        self.data = data

    def sending(self, recipient_email):
        import smtplib
        import configparser

        # use of ini file for security reasons
        config = configparser.ConfigParser()
        config.read('cred.ini')

        # SMTP configuration
        smtp_server = config.get('EmailSettings', 'SMTP_SERVER')
        port = config.get('EmailSettings', 'SMTP_PORT')

        sender_email = config.get('EmailSettings', 'sender_email')
        password = config.get('EmailSettings', 'password')

        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(sender_email, password)

        # Send email
        subject = 'Weather Alert'
        body = 'Testing new configuration!'

        import email.message

        message = email.message.Message()
        message['From'] = sender_email
        message['To'] = recipient_email
        message['Subject'] = subject
        message.set_payload(self.data)

        response = server.sendmail(sender_email, recipient_email, message.as_string())
        if response == {}:
            print('Email sent successfully')
        else:
            print(f'Email failed to send. Response: {response}')
        # Close server connection
        server.quit()

