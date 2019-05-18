[![CircleCI](https://circleci.com/gh/Victoradukwu/AutoTicket.svg?style=svg)](https://circleci.com/gh/Victoradukwu/AutoTicket)
# AutoTicket

## Introduction
**AutoTicket** is an application that automates airline ticketing system.
## __Application API Link__
https://auto-ticket.herokuapp.com/swagger/

## Key Application features  
* User can register abd log in
* User can upload passport photographs
* User can book tickets
* User can receive tickets as an email
* User can check the status of their flight
* User can make flight reservations
* User can make online payment using credit/debit card

## API Endpoints 
* Register: users/register/
* Register: POST users/register/
* Log in: POST users/login/
* List of users: GET: users/
* List available flights: GET flights/
* Details of a Flight: GET flights/pk/
* List available seat objetcs: GET seats/
* Details of a seat object: GET seat/pk/
* Make Reservation: POST tickets/reservation/
* Book ticket: POST tickets/book/
* Make pyment: 'payment/'

## Technologies used
* Python: A fast growing programming language.
* Postgres DBMS: An open-source RDBMS for storing data.
* Django web framework: A fullstack Python web application framework.
* Drango Restframework: A pakage for clean development of RESTful API in django.


## Installing the application 

* Clone the application to your local system
```Sh
> $ git clone https://github.com/Victoradukwu/AutoTicket.git
```
* Change the directory on your local system
```Sh
> $ cd /AutoTicket
```
* Install all dependencies
```Sh
> $ pip install -r requirements.txt
```
* create a .env file at you app root and populate it withb the encironment variables such as:
```Sh
DEBUG=True
EMAIL_HOST_USER=you_gmail_account
EMAIL_HOST_PASSWORD=your_gmail_password
SECRET_KEY=your_secret_key


CLOUD_NAME=your_cloudinary_username
CLOUDINARY_API_KEY=your_cloudinary_api_key
CLOUDINARY_API_SECRET=your_cloudinary_api_secret
PAYSTACK_TEST_SECRET_KEY=your_paystack_test_secret_key
PAYSTACK_TEST_PUBLICK_KEY=your_paystack_test_public_key
CELERY_BROKER_URL='redis://localhost'
```

* Migrate the application
```Sh
> $ python manage.py migrate
```
* Install Redis and start the redis server

* Start the application
```sh
> $ python manage.py runserver
```
* Run tests
```sh
> $ coverage run manage.py test
> $ coverage report
```

