import imapclient
import smtplib


class ConnectionError(Exception):
    """Base class for other connection-related exceptions"""
    pass


class IMAPConnectionError(ConnectionError):
    """Raised when there is an error connecting to the IMAP server"""
    def __init__(self, message="IMAP Connection Error"):
        self.message = message
        super().__init__(self.message)


class SMTPConnectionError(ConnectionError):
    """Raised when there is an error connecting to the SMTP server"""
    def __init__(self, message="SMTP Connection Error"):
        self.message = message
        super().__init__(self.message)


class Connection:
    """Handles the connection to IMAP and SMTP servers for email access."""

    def __init__(self, email: str, password: str, imap_server: str = '', smtp_server: str = ''):
        self.imap_server = imap_server
        self.smtp_server = smtp_server
        self.email = email
        self._password = password
        self.imap_client = None
        self.smtp_client = None

    def connect_imap(self):
        """Connect to IMAP server"""
        try:
            self.imap_client = imapclient.IMAPClient(self.imap_server)
            self.imap_client.login(self.email, self._password)
        except imapclient.exceptions.LoginError:
            raise IMAPConnectionError("IMAP Authentication Error: Invalid email or password.")
        except Exception as e:
            raise IMAPConnectionError(f"IMAP Connection Error: {e}")

    def disconnect_imap(self):
        """Disconnect from IMAP server"""
        if self.imap_client:
            self.imap_client.logout()
            self.imap_client = None

    def connect_smtp(self):
        """Connect to SMTP server"""
        try:
            self.smtp_client = smtplib.SMTP(self.smtp_server)
            self.smtp_client.starttls()
            self.smtp_client.login(self.email, self._password)
        except smtplib.SMTPAuthenticationError:
            raise SMTPConnectionError("SMTP Authentication Error: Invalid email or password.")
        except Exception as e:
            raise SMTPConnectionError(f"SMTP Connection Error: {e}")

    def disconnect_smtp(self):
        """Disconnect from SMTP server"""
        if self.smtp_client:
            self.smtp_client.quit()
            self.smtp_client = None

    def __enter__(self):
        self.connect_imap()
        self.connect_smtp()
        return self

    def __exit__(self, exc_type, exec_value, traceback):
        self.disconnect_imap()
        self.disconnect_smtp()
