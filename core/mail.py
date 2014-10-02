from django.conf import settings
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from markdown import Markdown
import premailer
import smtplib

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
	
	# Init mail sender
	s = smtplib.SMTP('localhost')

	# Send mails to the receiver
	for receiver in receivers:

		uid = receiver.confirm_id if display_unsubscribe else None
		text, html = renderContent(markdown_content, uid)

		msg = MIMEMultipart('alternative')
		msg['Subject'] = subject
		msg['From'] = sender
		msg['To'] = receiver.email

		# Set the content of the mail
		msg.attach(MIMEText(text, 'plain', 'utf-8'))
		msg.attach(MIMEText(html, 'html', 'utf-8'))	

		s.sendmail(sender, receiver.email, msg.as_string())

	# Quit mail client connection
	s.quit()

def renderContent(markdown_content, unsubscribe_id=None):
	"""
		Converts the markdown content to a raw text and a html version that could
		be used as content in an email. The text is embedded in the core/base_mail.txt, 
		the html in the core/base_mail.html template.

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
		'unsubscribe_id' 	: unsubscribe_id,
		'settings'			: settings
	}

	# Render text
	text = render_to_string('core/base_mail.txt', content_dic)

	# Convert markdown to html (mark_safe is needed to prevent the html to be escaped)
	content_dic['content'] = mark_safe(Markdown().convert(markdown_content))
	# Render html
	html = render_to_string('core/base_mail_inline.html', content_dic)
	# Inline css styles
	html = premailer.transform(html)

	return (text, html)
