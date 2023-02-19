```
@app.on_event("startup")
async def startup_event():
    from .models.database import init_db
    await init_db()
```