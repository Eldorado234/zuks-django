{% load i18n %}

## {% trans "Thanks" %},
{% blocktrans %}
that you are interested in our project "Civilian Support for Civil Protection".
You will receive news about ZUKS, so you could follow the progress of the project.
Just open the following link, to confirm your Email address:
{% endblocktrans %}

[{{ settings.BASE_URL }}{% url 'confirm' id=subscribe_id %}]({{ settings.BASE_URL }}{% url 'confirm' id=subscribe_id %})

{% blocktrans %}
If you are not interested in the newsletter, just ignore this mail.
You won't receive any further mails.

Stay tuned,

Your ZUKS Team
{% endblocktrans %}
