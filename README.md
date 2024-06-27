# PyMailAccess

PyMailAccess is a Python module for accessing emails (reading and sending). It provides a simple interface for authentication, reading messages, sending emails, and manipulating messages.

## Index

- [Installation](#installation)
- [Usage](#usage)
- [Contribution](#contribution)
- [License](#license)
- [Future Features](#future-features)

## Installation

To install PyMailAccess, you can clone this repository and install the dependencies using `pip`.

```bash
git clone https://github.com/JonasChristiano/PyMailAccess
cd PyMailAccess
pip install -r requirements.txt
```

## Usage

### Reading Emails

Here is an example of how to use the `Reader` class to read emails:

```python
from mail.reader import Reader

reader = EmailReader('your@email.com', 'password', 'imap.example.com')
reader.select_folder('INBOX')

for email_id in reader.search_emails():
    email_body = reader.get_email_body(email_id)
    print(email_body)
```

### Sending Emails

Here is an example of how to use the `Sender` class to send emails:

```python
from mail.sender import Sender

sender = Sender('your@email.com', 'password', 'smtp.example.com:578', )
sender.send_email('Subject', 'recipient@example.com', 'This is a plain message.')
sender.send_email(
    subject='Subject',
    to=['recipient@example.com'],
    body='<h1>This is an HTML message.</h1>',
    content_type='html'
)
```

## Contribution

If you want to contribute to PyMailAccess, follow these steps:

1. Fork this repository.
2. Create a branch for your feature (`git checkout -b my-feature`).
3. Commit your changes (`git commit -m "Add my feature"`).
4. Push to the branch (`git push origin my-feature`).
5. Open a Pull Request.

Please ensure that you follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) commit pattern when making your commits.

## License

This project is licensed under the MIT license - see the [LICENSE](LICENSE) file for details.

## Future Features

- **File Attachments:** Enable sending emails with attachments such as PDFs, images, Word documents, etc.
- **Email Templates:** Implement a system for email templates to facilitate sending consistently formatted messages like newsletters, account confirmations, etc.
- **Advanced Error Handling:** Improve error handling to manage connection failures, sending errors, and other issues that may occur during the email sending process.
- **Sending Logs:** Implement logging to record all email sending attempts, aiding in debugging and monitoring.
- **Bulk Email Sending:** Add support for sending emails to a list of recipients, optimizing communication for large-scale operations.
- **Scheduled Sending:** Allow scheduling emails for specific times, useful for marketing campaigns or automated reminders.
