# supabase_submitter.py
import requests
from datetime import datetime

# Burası kendi Supabase API bilgilerinle değiştirilecek
SUPABASE_URL = "https://pvunkmlhgnqjryveftie.supabase.co"
SUPABASE_KEY = "SeyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB2dW5rbWxoZ25xanJ5dmVmdGllIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0NTM5MzYyMiwiZXhwIjoyMDYwOTY5NjIyfQ.FaB-Y0nyvAPsyAuasOw3n2I2yiQE5OKdFKqMArQuqBw"  # Bunu kendi keyinle değiştir.

def submit_exam_response(form_data: dict) -> bool:
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

    form_data["created_at"] = datetime.utcnow().isoformat()

    try:
        response = requests.post(SUPABASE_URL, headers=headers, json=form_data)
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
