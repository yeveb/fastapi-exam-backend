# main_api.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase_submitter import submit_exam_response
from fastapi.responses import JSONResponse

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
    user_id: str
    exam_name: str
    group: str
    form_data: dict

# Form verilerini Supabase'a gönderecek endpoint
@app.post("/submit_response")
async def submit_response(request: Request):
    form_data = await request.json()
    success = submit_exam_response(form_data)

    if success:
        return JSONResponse(content={"status": "ok", "message": "Kayıt başarıyla tamamlandı."})
    else:
        return JSONResponse(content={"status": "error", "message": "Supabase kayıt hatası."})
