```
@app.on_event("startup")
async def startup_event():
    from .models.init_db import init_db
    await init_db()
```