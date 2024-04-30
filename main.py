from fastapi import FastAPI
from Projects import my_ecommes

app=FastAPI()
app.include_router(my_ecommes.router)

