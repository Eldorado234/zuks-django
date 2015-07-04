# ZUKS Website based on the Django Framework
The official website of the ZUKS project (www.zuks.org).

## Installation
- Create a new Python 2.x or 3.x environment with `virtualenv venv-folder` _(optional)_
- Switch to the new environment with `source venv-folder/bin/activate` _(optional)_
- Change to the root directory of the project
- Configure the `BASE_URL` option in the `zuks/settings.py` properly
- Configure the database settings in the `zuks/settings.py` _(optional)_
- Execute `pip install -r requirements.txt`
- For Python <3.2 you also have to execute `pip install wsgiref==0.1.2`
- Execute `python manage.py syncdb`
- Execute `python manage.py collectstatic`
- Execute `django-admin.py compilemessages`
- Configure the webserver to deliver all files from the url `/static/*` from the `/static` folder _(optional when using the integrated web server `python manage.py runserver`)_
- Install and configure [django-sentry](https://sentry.readthedocs.org/en/v1.13.5/install/index.html) to track application errors _(optional)_
- Configure a hook that executes `python manage.py cleandb` periodically _(optional)_

## License
Copyright of the ZUKS-Website (C) 2015 Zivile Unterstützung im Katastrophenschutz e.V.

The following license information applies to the program, not to the content.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.