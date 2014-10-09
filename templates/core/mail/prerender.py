import premailer
import urllib

input = open('base_mail.html', 'r').read()
output = open('base_mail_inline.html', 'w')

result = premailer.Premailer(input).transform(input)

# Convert the quoted urls back, so they are valid django blocks again
result = urllib.unquote(result)

# Add loading of the static block
result = '{% load staticfiles %}\n\n' + result

output.write(result)
