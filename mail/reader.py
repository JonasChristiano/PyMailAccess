import email
from bs4 import BeautifulSoup
from mail.connection import Connection, IMAPConnectionError

class Reader(Connection):
    """Handles reading emails from an IMAP server using the Connection class."""

    def __init__(self, email, password, imap_server):
        super().__init__(email, password, imap_server=imap_server)
        try:
            self.connect_imap()
        except IMAPConnectionError as e:
            raise e

    def list_folders(self):
        """List all folders in the IMAP account."""
        try:
            return self.imap_client.list_folders()
        except Exception as e:
            raise IMAPConnectionError(f"Failed to list folders: {e}")

    def select_folder(self, folder):
        """Select a folder to work with."""
        try:
            return self.imap_client.select_folder(folder)
        except Exception as e:
            raise IMAPConnectionError(f"Failed to select folder '{folder}': {e}")

    def search_emails(self, criteria='ALL'):
        """Search for emails matching the given criteria."""
        try:
            return self.imap_client.search(criteria)
        except Exception as e:
            raise IMAPConnectionError(f"Failed to search emails with criteria '{criteria}': {e}")

    def fetch_email(self, uid):
        """Fetch an email by its UID."""
        try:
            return self.imap_client.fetch(uid, ['FLAGS', 'RFC822'])
        except Exception as e:
            raise IMAPConnectionError(f"Failed to fetch email with UID '{uid}': {e}")

    def get_email_body(self, uid):
        """Get the body of an email by its UID."""
        try:
            email_data = self.imap_client.fetch([uid], ['BODY[]'])
            raw_body = email_data[uid][b'BODY[]']
            email_message = email.message_from_bytes(raw_body)
            return self._extract_text_from_email(email_message)
        except Exception as e:
            raise IMAPConnectionError(f"Failed to get email body for UID '{uid}': {e}")

    def _extract_text_from_email(self, email_message, remove_html_tag=True):
        """Extract text from an email message."""
        text_body = ''
        if email_message.is_multipart():
            for part in email_message.walk():
                content_type = part.get_content_type()
                if content_type == 'text/plain':
                    charset = part.get_content_charset()
                    text_body = part.get_payload(decode=True).decode(charset)
                elif content_type == 'text/html':
                    charset = part.get_content_charset()
                    html_body = part.get_payload(decode=True).decode(charset)
                    if remove_html_tag:
                        soup = BeautifulSoup(html_body, 'html.parser')
                        text_body = soup.get_text(separator=' ')
                    else:
                        text_body = html_body
        else:
            charset = email_message.get_content_charset()
            text_body = email_message.get_payload(decode=True).decode(charset)
        return text_body
