# SeeJet API Tracker ✈️

SeeJet is a Python-based API (built with DRF) designed to provide information about airports, flights, and much more!
It allows users to retrieve details about:

- Routes
- Airports
- Locations
- Airplanes and more!

## Features

- **Search for Flight:** You can query the API to get information about specific flight 
by providing your current city or city you want to get in. You can even search by an airplane!
- **Book Tickets:** If you find what you were looking for, simply book a ticket!
- **Just explore:** You will be able to a lot of exciting details about airplanes, flights, 
airports, and even about crew!

---

## Installation

### Git

1.Start with cloning the repository to your local machine:
```shell
git clone https://github.com/aLEKS-e3/seejet.git
```
2. Open the project in your IDE, create, and activate a venv:
```shell
python -m venv venv
source venv/bin/activate # for linux and macos
venv/Scripts/actiavte # for windows
```
3. Install the required dependencies:
```shell
pip install -r requirements.txt
```
4. Apply all the migrations and explore!
```shell
python manage.py migrate
python manage.py runserver
```

### Docker

If you have docker installed on your desktop, then all you need to do is:

```shell
docker pull chebuster/airport-tracker-api
docker-compose build
docker-compose up
```

---

### Interaction

For more pleasant experience, you can use prepared data:
```shell
python manage.py loaddata airport_data.json
```

Create your own user via ```api/user/register/``` or use the one I've created for you:
- **Login:** jet_man@airport.com
- **Password:** 123_win_jet

**NOTE:** Access to all resources is provided via JWT. To get one go to ```api/user/token/```.

**P.S.:** To find all accessible endpoint go to ```api/doc/swagger/```.

---

## License

This project is licensed under the _Chebukin International Development Inc._- 
contact the [CEO](https://github.com/aLEKS-e3) for details.
