# 2. main_api.py - Düzenlenmiş Hali

from fastapi import FastAPI, Request, HTTPException
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

# Gelen verinin doğru şekilde yapılandırılması için ResponseData modeli
class FormDataModel(BaseModel):
    ad_soyad: str
    ogr_no: str
    email: str
    sinif: str
    cevaplar: dict

class ResponseData(BaseModel):
    exam_key: str
    exam_name: str
    group: str
    created_at: str = None  # Varsayılan olarak None, eksikse ekleyeceğiz
    form_data: FormDataModel

@app.post("/submit_response")
async def submit_response(request: Request):
    try:
        incoming_data = await request.json()
        data = ResponseData(**incoming_data)

        # Eğer created_at eksikse tamamla
        if not data.created_at:
            data.created_at = datetime.utcnow().isoformat()

        success = submit_exam_response(data.dict())

        if success:
            return JSONResponse(content={"status": "ok", "message": "Kayıt başarıyla tamamlandı."})
        else:
            return JSONResponse(content={"status": "error", "message": "Supabase kayıt hatası."})

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Geçersiz veri: {e}")
ckend