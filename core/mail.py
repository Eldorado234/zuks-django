from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from markdown import Markdown
import premailer
from django.core.mail import send_mail

def sendMail(sender, receivers, markdown_content, subject, display_unsubscribe=True):
	"""
		Sends a multipart to the receivers. Both, the raw text and the html,
		are generated out of the markdown content.

		Args:
      		sender (string): 			the email adress of the sender
      		receivers (array): 			an array with receivers. Each receiver has
      									to have the two attributes `email` and
      									`confirm_id`. The second attribute is used to
      									generate the unsubscribe link in the mail.
      		markdown_content (string):	the content of the mail encoded in the markdown
      									markup language.
      		subject (string):			the subject of the mail.
      		display_unsubscribe (bool): True, if the unsubscribe link should be displayed,
      									False otherwise

	"""

	# Send mails to the receiver
	for receiver in receivers:

		uid = receiver.confirm_id if display_unsubscribe else None
		text, html = renderContent(markdown_content, uid)

		send_mail(subject, text, sender, [receiver.email], html_message=html)

def renderContent(markdown_content, unsubscribe_id=None):
	"""
		Converts the markdown content to a raw text and a html version that could
		be used as content in an email. The text is embedded in the core/mail/base_mail.txt,
		the html in the core/mail/base_mail_inline.html template.

		Args:
      		markdown_content (string): the content in a valid markdown syntax
      		unsubscribe_id   (string): the id which could be used by the user to
      								   unsubscribe from the newsletter. Is embedded
      								   in the unsubscribe link in the templates.

      	Returns:
      		a tuple with the text version at the first index and
      		the html version at the second
	"""

	content_dic = {
		'content' 			: markdown_content,
		'unsubscribe_id' 	: unsubscribe_id
	}

	# Render text
	text = render_to_string('core/mail/base_mail.txt', content_dic)

	# Convert markdown to html (mark_safe is needed to prevent the html to be escaped)
	content_dic['content'] = mark_safe(Markdown().convert(markdown_content))
	# Render html
	html = render_to_string('core/mail/base_mail_inline.html', content_dic)
	# Inline css styles
	html = premailer.transform(html)

	return (text, html)
