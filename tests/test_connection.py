import smtplib
import unittest
from unittest.mock import patch, MagicMock
from mail.connection import Connection, IMAPConnectionError, SMTPConnectionError


class TestConnection(unittest.TestCase):

    @patch('mail.connection.imapclient.IMAPClient')
    @patch('mail.connection.smtplib.SMTP')
    def test_connect_imap_success(self, mock_smtp, mock_imap):
        mock_imap_instance = mock_imap.return_value
        mock_imap_instance.login.return_value = True

        conn = Connection(email='test@example.com', password='password', imap_server='imap.example.com')
        
        try:
            conn.connect_imap()
        except Exception:
            self.fail("connect_imap() raised Exception unexpectedly!")
        
        mock_imap_instance.login.assert_called_once_with('test@example.com', 'password')

    @patch('mail.connection.imapclient.IMAPClient')
    @patch('mail.connection.smtplib.SMTP')
    def test_connect_imap_authentication_error(self, mock_smtp, mock_imap):
        mock_imap_instance = mock_imap.return_value
        mock_imap_instance.login.side_effect = smtplib.SMTPAuthenticationError(451, b'Authentication Failed')

        conn = Connection(email='test@example.com', password='wrongpassword', imap_server='imap.example.com')
        
        with self.assertRaises(IMAPConnectionError):
            conn.connect_imap()
        
        mock_imap_instance.login.assert_called_once_with('test@example.com', 'wrongpassword')

    @patch('mail.connection.imapclient.IMAPClient')
    @patch('mail.connection.smtplib.SMTP')
    def test_connect_smtp_success(self, mock_smtp, mock_imap):
        mock_smtp_instance = mock_smtp.return_value
        mock_smtp_instance.login.return_value = True

        conn = Connection(email='test@example.com', password='password', smtp_server='smtp.example.com')
        
        try:
            conn.connect_smtp()
        except Exception:
            self.fail("connect_smtp() raised Exception unexpectedly!")
        
        mock_smtp_instance.login.assert_called_once_with('test@example.com', 'password')

    @patch('mail.connection.imapclient.IMAPClient')
    @patch('mail.connection.smtplib.SMTP')
    def test_connect_smtp_authentication_error(self, mock_smtp, mock_imap):
        mock_smtp_instance = mock_smtp.return_value
        mock_smtp_instance.login.side_effect = smtplib.SMTPAuthenticationError(451, b'Authentication Failed')

        conn = Connection(email='test@example.com', password='wrongpassword', smtp_server='smtp.example.com')
        
        with self.assertRaises(SMTPConnectionError):
            conn.connect_smtp()
        
        mock_smtp_instance.login.assert_called_once_with('test@example.com', 'wrongpassword')

    @patch('mail.connection.imapclient.IMAPClient')
    @patch('mail.connection.smtplib.SMTP')
    def test_disconnect_imap(self, mock_smtp, mock_imap):
        mock_imap_instance = mock_imap.return_value

        conn = Connection(email='test@example.com', password='password', imap_server='imap.example.com')
        conn.imap_client = mock_imap_instance
        conn.disconnect_imap()

        mock_imap_instance.logout.assert_called_once()
        self.assertIsNone(conn.imap_client)

    @patch('mail.connection.imapclient.IMAPClient')
    @patch('mail.connection.smtplib.SMTP')
    def test_disconnect_smtp(self, mock_smtp, mock_imap):
        mock_smtp_instance = mock_smtp.return_value

        conn = Connection(email='test@example.com', password='password', smtp_server='smtp.example.com')
        conn.smtp_client = mock_smtp_instance
        conn.disconnect_smtp()

        mock_smtp_instance.quit.assert_called_once()
        self.assertIsNone(conn.smtp_client)


if __name__ == '__main__':
    unittest.main()
