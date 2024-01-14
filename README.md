pip3 install pipenv
pipenv shell 
pipenv install django
pipenv install djangorestframework
pipenv install djoser



python manage.py runserver <9000> change port is optional


superuser:
user:tao
email:tao@gmail.com
password:123
TOKEN:a4b5486f9f1a69c06149f0b26a4748ad46eeea33


Manager:
user:SomeUserName
email:tao@gmail.com
password:someemail@email.com
TOKEN:900c14dfb2716cdb1c86ad2d4e46feaeb12c2940

Delivery Crew
user:Josn
email: n/a
password:86562568@
TOKEN:a314cbe704610ea20a4d0761c049a25f3e56fdb8


test url endpoint:

User registration and token generation endpoints 
Role: anyone, token, username and password pair
http://127.0.0.1:8000/api/users POST
http://127.0.0.1:8000/api/users/users/me/   GET
http://127.0.0.1:8000/token/login/  POST

Menu-items endpoints 
Role:Customer, delivery crew,Manager
http://127.0.0.1:8000/api/menu-items    GET/POST/DELETE/PATCH/PUT
http://127.0.0.1:8000/api/menu_items/1  GET/PUT/PATCH/DELETE


User group management endpoints
Role: Manager
http://127.0.0.1:8000/api/groups/manager/users  GET/POST
http://127.0.0.1:8000/api/groups/delivery-crew/users/3/ DELETE


Cart management endpoints 
Role: Customer
http://127.0.0.1:8000/api/cart/menu-items

Order management endpoints
Role:Customer, delivery crew,Manager
http://127.0.0.1:8000/api/orders    GET/POST
http://127.0.0.1:8000/api/orders/1/ GET/PUT/PATCH