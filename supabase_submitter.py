# supabase_submitter.py
import requests
from datetime import datetime

SUPABASE_URL = "https://pvunkmlhgnqjryveftie.supabase.co/rest/v1/exam_responses"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB2dW5rbWxoZ25xanJ5dmVmdGllIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0NTM5MzYyMiwiZXhwIjoyMDYwOTY5NjIyfQ.FaB-Y0nyvAPsyAuasOw3n2I2yiQE5OKdFKqMArQuqBw"

def submit_exam_response(form_data: dict) -> bool:
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

    form_data["created_at"] = datetime.utcnow().isoformat()

    try:
        # form_data içinden gerekli alanları ayıklıyoruz
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

        if response.status_code == 201:
            print("✅ Supabase kaydı başarılı.")
            return True
        else:
            print(f"❌ Supabase hatası: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"💥 Bağlantı hatası: {e}")
        return False
