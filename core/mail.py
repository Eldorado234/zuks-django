# This file is part of ZUKS-Website.
#
# ZUKS-Website is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ZUKS-Website is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ZUKS-Website. If not, see <http://www.gnu.org/licenses/>.

from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from markdown import Markdown
from django.utils.html import escape
import premailer
from django.core.mail import send_mail

def sendMail(sender, receivers, markdown_content, news_id, subject,
			 display_unsubscribe=True, context=None, skip_errors=False):
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
			news_id (integer):			the news id for the link of the online version
      		subject (string):			the subject of the mail.
      		display_unsubscribe (bool): True, if the unsubscribe link should be displayed,
      									False otherwise
			skip_errors (bool):			If set, all errors are catched and the mail
										is sent to the outstanding receivers. The last
										exception is raised at the end.

	"""
	error = None

	# Send mails to the receiver
	for receiver in receivers:

		uid = receiver.confirm_id if display_unsubscribe else None
		text, html = renderContent(markdown_content, news_id, uid, context)

		try:
			send_mail(subject, text, sender, [receiver.email], html_message=html)
		except Exception as e:
			error = e
			if not skip_errors:
				raise error

	if error:
		raise error


def renderContent(markdown_content, news_id, unsubscribe_id=None, context=None, tpl='core/mail/base_mail.html'):
	"""
		Converts the markdown content to a raw text and a html version that could
		be used as content in an email. The text is embedded in the core/mail/base_mail.txt,
		the html in the core/mail/base_mail_inline.html template.

		Args:
      		markdown_content (string):  the content in a valid markdown syntax
      		news_id 		 (integer): id for the news (read online link)
      		unsubscribe_id   (string):  the id which could be used by the user to
      								    unsubscribe from the newsletter. Is embedded
      								    in the unsubscribe link in the templates.
            context 		 (Context):	Context object.

      	Returns:
      		a tuple with the text version at the first index and
      		the html version at the second
	"""

	if not context:
		from django.template import Context
		from django.conf import settings
		context = Context({'settings' : settings})

	content_dic = {
		'content' 			: markdown_content,
		'unsubscribe_id' 	: unsubscribe_id,
		'news_id'			: news_id
	}

	# Render text
	text = render_to_string('core/mail/base_mail.txt', content_dic, context)

	# Escape potential html in the markdown content
	markdown_content = escape(markdown_content)
	# Convert markdown to html
	# (mark_safe is needed to prevent the converted html to be escaped)
	content_dic['content'] = mark_safe(Markdown().convert(markdown_content))
	# Render html
	html = render_to_string(tpl, content_dic, context)
	# Inline css styles
	html = premailer.transform(html)

	return (text, html)
