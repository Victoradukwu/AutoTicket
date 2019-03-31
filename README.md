# AutoTicket

## Introduction
**AutoTicket** is an application that automates airline ticketing system.
## __Application Link__
https://auto-ticket.herokuapp.com/

## Key Application features  
* User can register abd log in
* User can upload passport photographs
* User can book tickets
* User can receive tickets as an email
* User can check the status of their flight
* User can make flight reservations
* User can make online payment using credit/debit card
## Technologies used
* Python: A fast growing programming language
* Postgres DBMS: An open-source RDBMS for storing data
* Django web framework: A fullstack Python web application framework
* Drango Restframework: A pakage for clean development of RESTful API in django


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

```

* Migrate the application
```Sh
> $ python manage.py migrate
```
* Start the application
```sh
> $ python manage.py runserver
```
* Run tests
```sh
> $ coverage run manage.py test
> $ coverage report
```

