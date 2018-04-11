# Dronestream

## Getting Started

Checkout the latest version of the code as you normally would:

```
git clone https://github.com/mjun/dronestream.git
```

Initialize python 3 enabled virtualenv in project directory:

```
cd dronestream
virtualenv -p python3 venv
source venv/bin/activate
```

Install requirements:

```
pip install -r requirements.txt
```

Run migrations:

```
python manage.py migrate
```

Import dronestream data:

```
python manage.py import_data
```

_(Optional)_ Create superuser if you wish to access the admin interface:

```
python manage.py createsuperuser
```

Setup `GOOGLE_MAPS_API_KEY` property in project settings.py. You can get API key from 
[Google Maps Developers page](https://developers.google.com/maps/documentation/javascript/get-api-key)

Run the app as usual:

```
python manage.py runserver
```

