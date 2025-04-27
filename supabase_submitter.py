# supabase_submitter.py (Güvenli .env destekli versiyon)

import requests
import os
from datetime import datetime
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

# Ortam değişkenlerinden oku
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

def submit_exam_response(form_data: dict) -> bool:
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

    try:
        payload = {
            "exam_key": form_data.get("exam_key", ""),
            "exam_name": form_data.get("exam_name", ""),
            "group": form_data.get("group", ""),
            "ad_soyad": form_data.get("form_data", {}).get("ad_soyad", ""),
            "ogr_no": form_data.get("form_data", {}).get("ogr_no", ""),
            "email": form_data.get("form_data", {}).get("email", ""),
            "sinif": form_data.get("form_data", {}).get("sinif", ""),
            "form_data": form_data.get("form_data", {}),
            "created_at": form_data.get("created_at", datetime.utcnow().isoformat()),
        }

        response = requests.post(SUPABASE_URL, headers=headers, json=payload)
        print("🔍 Supabase Response:", response.status_code, response.text)

        if 200 <= response.status_code < 300:
            print("✅ Supabase kaydı başarılı.")
            return True
        else:
            print(f"❌ Supabase hatası: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        print(f"💥 Bağlantı hatası: {e}")
        return False
