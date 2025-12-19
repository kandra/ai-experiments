from fastapi import FastAPI
from app.routers import ocr_invoices

app = FastAPI(
    title="AI Invoice Parser",
    version="1.0.0"
)

# Aquí "enchufamos" el router de facturas
app.include_router(ocr_invoices.router)

@app.get("/")
def root():
    return {"message": "System Online 🟢"}