from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Literal

from mail.connection import Connection

class Sender(Connection):
    """Classe para envio de emails"""

    def __init__(self, email, password, smtp_server):
        super().__init__(email, password, smtp_server=smtp_server)
        self.connect_smtp()
    
    def send_email(self, subject, to, body, content_type:Literal['html','plain']='plain'):
        message = MIMEMultipart()
        message['subject'] = subject
        message['from'] = self.email
        message['to'] = to

        if content_type == 'html':
            body_part = MIMEText(body, 'html')
        elif content_type == 'plain':
            body_part = MIMEText(body, 'plain')
        else:
            raise ValueError('Error: content type wrong.')
        
        message.attach(body_part)
        # Cabeçalho Content-Type já definido pelo MIMEText
        # message.add_header('Content-Type', 'text/html; charset=utf-8') -> Removido

        return self.smtp_client.sendmail(self.email, to, message.as_string())
