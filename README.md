# Music-Library

It's my MCA last semester project based on Python/Django. 
A web based application where users can upload and share music to other users. Users can create album and playlist and also listen them.

### Run followin commands to run project after clone
* ```cd Music-Library```
* ```pip install virtualenv```
* ```virtualenv .```
* (activate virtual env)
* ```cd src```
* ```pip install -r requirements.txt```
* ```python manage.py migrate```
* ```python manage.py collectstatic```
* configure `MusicLibrary/settings.py` file
  * add your email id in `EMAIL_HOST_USER` variable to sent email in case of forgate password of users
  * add password in `EMAIL_HOST_PASSWORD` variable
 * ```python manage.py runserver```
