import unittest
from unittest.mock import patch, MagicMock
from mail.reader import Reader, IMAPConnectionError

class TestReader(unittest.TestCase):

    @patch('mail.connection.imapclient.IMAPClient')
    def setUp(self, MockIMAPClient):
        self.mock_imap_client = MockIMAPClient.return_value
        self.reader = Reader('test@example.com', 'password', 'imap.example.com')
        
    def test_list_folders(self):
        self.mock_imap_client.list_folders.return_value = ['INBOX', 'Sent', 'Trash']
        folders = self.reader.list_folders()
        self.assertEqual(folders, ['INBOX', 'Sent', 'Trash'])
        self.mock_imap_client.list_folders.assert_called_once()

    def test_list_folders_error(self):
        self.mock_imap_client.list_folders.side_effect = Exception('Failed to list folders')
        with self.assertRaises(IMAPConnectionError) as context:
            self.reader.list_folders()
        self.assertEqual(str(context.exception), 'Failed to list folders: Failed to list folders')
        
    def test_select_folder(self):
        self.mock_imap_client.select_folder.return_value = 'OK'
        result = self.reader.select_folder('INBOX')
        self.assertEqual(result, 'OK')
        self.mock_imap_client.select_folder.assert_called_once_with('INBOX')

    def test_select_folder_error(self):
        self.mock_imap_client.select_folder.side_effect = Exception('Failed to select folder')
        with self.assertRaises(IMAPConnectionError) as context:
            self.reader.select_folder('INBOX')
        self.assertEqual(str(context.exception), "Failed to select folder 'INBOX': Failed to select folder")

    def test_search_emails(self):
        self.mock_imap_client.search.return_value = [1, 2, 3]
        result = self.reader.search_emails('ALL')
        self.assertEqual(result, [1, 2, 3])
        self.mock_imap_client.search.assert_called_once_with('ALL')

    def test_search_emails_error(self):
        self.mock_imap_client.search.side_effect = Exception('Failed to search emails')
        with self.assertRaises(IMAPConnectionError) as context:
            self.reader.search_emails('ALL')
        self.assertEqual(str(context.exception), "Failed to search emails with criteria 'ALL': Failed to search emails")

    def test_fetch_email(self):
        self.mock_imap_client.fetch.return_value = {1: {'FLAGS': (), 'RFC822': b''}}
        result = self.reader.fetch_email(1)
        self.assertEqual(result, {1: {'FLAGS': (), 'RFC822': b''}})
        self.mock_imap_client.fetch.assert_called_once_with(1, ['FLAGS', 'RFC822'])

    def test_fetch_email_error(self):
        self.mock_imap_client.fetch.side_effect = Exception('Failed to fetch email')
        with self.assertRaises(IMAPConnectionError) as context:
            self.reader.fetch_email(1)
        self.assertEqual(str(context.exception), "Failed to fetch email with UID '1': Failed to fetch email")

    @patch('mail.reader.email.message_from_bytes')
    def test_get_email_body(self, mock_message_from_bytes):
        mock_email_message = MagicMock()
        mock_email_message.is_multipart.return_value = False
        mock_email_message.get_content_charset.return_value = 'utf-8'
        mock_email_message.get_payload.return_value = 'Hello, World!'.encode('utf-8')
        
        mock_message_from_bytes.return_value = mock_email_message
        self.mock_imap_client.fetch.return_value = {1: {b'BODY[]': b''}}
        
        body = self.reader.get_email_body(1)
        self.assertEqual(body, 'Hello, World!')
        
    def test_get_email_body_error(self):
        self.mock_imap_client.fetch.side_effect = Exception('Failed to fetch email body')
        with self.assertRaises(IMAPConnectionError) as context:
            self.reader.get_email_body(1)
        self.assertEqual(str(context.exception), "Failed to get email body for UID '1': Failed to fetch email body")

if __name__ == '__main__':
    unittest.main()
