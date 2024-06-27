import unittest
from unittest.mock import patch, MagicMock
from mail.sender import Sender
import smtplib

class TestSender(unittest.TestCase):

    def setUp(self):
        self.email = "test@example.com"
        self.password = "password"
        self.smtp_server = "smtp.example.com"

    @patch.object(smtplib, 'SMTP')
    def test_send_email_plain_text(self, MockSMTP):
        self.sender = Sender(self.email, self.password, self.smtp_server)
        mock_smtp_instance = MockSMTP.return_value
        mock_smtp_instance.sendmail = MagicMock()

        subject = "Test Subject"
        to = "recipient@example.com"
        body = "This is a test email."
        content_type = "plain"

        self.sender.send_email(subject, to, body, content_type)
        
        mock_smtp_instance.sendmail.assert_called_once()
        args, kwargs = mock_smtp_instance.sendmail.call_args
        self.assertEqual(args[0], self.email)
        self.assertEqual(args[1], to)
        self.assertIn('This is a test email.', args[2])
        self.assertIn('Content-Type: text/plain', args[2])

    @patch.object(smtplib, 'SMTP')
    def test_send_email_html(self, MockSMTP):
        self.sender = Sender(self.email, self.password, self.smtp_server)
        mock_smtp_instance = MockSMTP.return_value
        mock_smtp_instance.sendmail = MagicMock()

        subject = "Test Subject"
        to = "recipient@example.com"
        body = "<h1>This is a test email.</h1>"
        content_type = "html"

        self.sender.send_email(subject, to, body, content_type)
        
        mock_smtp_instance.sendmail.assert_called_once()
        args, kwargs = mock_smtp_instance.sendmail.call_args
        self.assertEqual(args[0], self.email)
        self.assertEqual(args[1], to)
        self.assertIn('<h1>This is a test email.</h1>', args[2])
        self.assertIn('Content-Type: text/html', args[2])

    @patch.object(smtplib, 'SMTP')
    def test_send_email_invalid_content_type(self, MockSMTP):
        self.sender = Sender(self.email, self.password, self.smtp_server)

        subject = "Test Subject"
        to = "recipient@example.com"
        body = "This is a test email."
        content_type = "invalid"

        with self.assertRaises(ValueError) as context:
            self.sender.send_email(subject, to, body, content_type)
        
        self.assertEqual(str(context.exception), 'Error: content type wrong.')

if __name__ == '__main__':
    unittest.main()
