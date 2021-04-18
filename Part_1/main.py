from fastapi import FastAPI
from v1.routers import router
import json
from mangum import Mangum
import uvicorn

app = FastAPI()

app.include_router(router, prefix="/v1")


@app.get("/")
async def read_root():
    return {"Message": "Hello welcome to the Assignment_4"}


handler = Mangum(app=app)

if __name__ == '__main__':
    uvicorn.run(app, port=8000, host="0.0.0.0")
