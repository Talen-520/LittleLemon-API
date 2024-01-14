# LittleLemon API

Welcome to the LittleLemon API! This project is designed to provide a comprehensive suite of functionalities for managing users, menu items, carts, and orders.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Before you begin, ensure you have the following tools installed:

- Python 3
- pip3
- pipenv

### Setting Up the Environment

To set up your development environment, run the following commands:

```bash
pip3 install pipenv
pipenv shell
pipenv install django djangorestframework djoser
```

Running the Application
```
python manage.py runserver 9000 # Change port to 9000 (optional)
```

# Usage
### Superuser
Username: tao

Email: tao@gmail.com

Password: 123

Token: a4b5486f9f1a69c06149f0b26a4748ad46eeea33
### Manager
Username: SomeUserName

Email: tao@gmail.com

Password: someemail@email.com

Token: 900c14dfb2716cdb1c86ad2d4e46feaeb12c2940

### Delivery Crew
Username: Josn

Email: n/a

Password: 86562568@

Token: a314cbe704610ea20a4d0761c049a25f3e56fdb8

# API Endpoints
### User Registration and Token Generation
```
Role: Anyone
POST: http://127.0.0.1:8000/api/users
GET: http://127.0.0.1:8000/api/users/users/me/
POST: http://127.0.0.1:8000/token/login/
```
### Menu-items Management
````
Role: Customer, Delivery Crew, Manager
GET/POST/DELETE/PATCH/PUT: http://127.0.0.1:8000/api/menu-items
GET/PUT/PATCH/DELETE: http://127.0.0.1:8000/api/menu_items/1
```
### User Group Management
```
Role: Manager
GET/POST: http://127.0.0.1:8000/api/groups/manager/users
DELETE: http://127.0.0.1:8000/api/groups/delivery-crew/users/3/
```
### Cart Management
```
Role: Customer
Endpoint: http://127.0.0.1:8000/api/cart/menu-items
Order Management
Role: Customer, Delivery Crew, Manager
GET/POST: http://127.0.0.1:8000/api/orders
GET/PUT/PATCH: http://127.0.0.1:8000/api/orders/1/
```
