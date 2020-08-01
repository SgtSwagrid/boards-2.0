# Boards

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
\boards\boards\.env:
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
python manage.py makemigrations
python manage.py migrate
```
