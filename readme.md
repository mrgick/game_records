
# Game records
University project on the subject "Methods and means of designing information systems and technologies".

## About
This project implements the registration of players and their games and the results of games played. 

Also, this project is designed for only one person - administrator.

Based on MVT with asynchronous python 3.11 and libraries: FastApi, SqlAlchemy and Jinja2. Tests wrote on PyTest with plugin AnyIO for asynchronous.

## How to run

### Using docker
- Build
```bash
docker build -t game_records .
```
- Run (sqlite database will be in memory)
```bash
docker run -e DB_URL="sqlite+aiosqlite://" -p 80:80 game_records
```
Now you can access web on [localhost](http://127.0.0.1:80)

### Manually
- Install python 3.11
- Clone game_records from github
```bash
git clone https://github.com/mrgick/game_records.git
```
- Open directory game_records
```
cd game_records
```
- Create python virtual env
```bash
python -m venv venv
```
- Activate it
    
On Linux/MacOS

```bash
. venv/bin/activate
```

On Windows

```bash
source venv/scripts/activate
```
- Install requirements
```bash
pip install -r requirements.txt
```
- Create .env file (just copy .env_example)
```env
DB_URL="sqlite+aiosqlite:///game_records.db"
```
- Run web server
```bash
python -m uvicorn app.main:app --port 8000
```

Now you can access web on [localhost:8000](http://127.0.0.1:8000)

## Tests
To run tests do guide "Manually" in "How to run" and then type in terminal
```bash
python -m pytest tests
```