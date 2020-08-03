# Boards
Boards is an online platform for the design and testing of game playing bots. With an assortment of abstract strategy board games available, Boards is able to facilitate games featuring any combination of human and computer-controlled players.

## Installation
Requirements:
* [MySQL](https://www.mysql.com/products/community/)
* [Docker](https://www.docker.com/products/docker-desktop)
```powershell
virtualenv .
.\Scripts\activate
pip install channels_redis
pip install mysqlclient
pip install python-dotenv
```
/boards/boards/.env:
```python
SECRET_KEY=...
DB_NAME=...
DB_USER=...
DB_PASSWORD=...
```

## Execution
```powershell
.\Scripts\activate
docker run -p 6379:6379 -d redis:5
python manage.py migrate
python manage.py runserver
```
