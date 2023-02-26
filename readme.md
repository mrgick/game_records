```
@app.on_event("startup")
async def startup_event():
    from .database.database import init_db
    await init_db()
```

To run tests

```
python -m pytest app/tests/
```