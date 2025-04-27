# main_api.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase_submitter import submit_exam_response
from fastapi.responses import JSONResponse
from datetime import datetime

app = FastAPI()

# CORS ayarları (her yerden erişim izni veriyoruz)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Formdan gelen verinin yapısını tanımlıyoruz
class ResponseData(BaseModel):
    exam_key: str
    exam_name: str
    group: str
    form_data: dict

# Form verilerini Supabase'a gönderecek endpoint
@app.post("/submit_response")
async def submit_response(request: Request):
    form_data = await request.json()
    
    # Eğer created_at yoksa burada ekleyelim
    if "created_at" not in form_data:
        form_data["created_at"] = datetime.utcnow().isoformat()
    
    success = submit_exam_response(form_data)

    if success:
        return JSONResponse(content={"status": "ok", "message": "Kayıt başarıyla tamamlandı."})
    else:
        return JSONResponse(content={"status": "error", "message": "Supabase kayıt hatası."})
