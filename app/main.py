from fastapi import FastAPI
from app.api.routes.chat import router
app=FastAPI(title='Walmart-style Claude Assistant • Educational Demo')
app.include_router(router,prefix='/api/v1')
@app.get('/health')
def health():return {'status':'ok','mode':'educational'}
