# OCR KTP API

A lightweight Flask API for Indonesian ID card (KTP) OCR processing.

## Prerequisites

- Python 3.6+
- Google Cloud Vision API credentials

## Setup

1. Set up Google Cloud Vision API credentials:
   ```
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/your-credentials.json"
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python app.py
   ```

## API Endpoints

### Health Check

```
GET /health
```

Returns a simple status check to verify the API is running.

### OCR KTP

```
POST /ocr/ktp
```

Process an Indonesian ID card (KTP) image and extract information.

**Request:**
- Form data with an image file in the 'image' field

**Response:**
```json
{
  "success": true,
  "score": 0.95,
  "content": {
    "nik": "1234567890123456",
    "nama": "NAMA LENGKAP",
    "tempat_lahir": "JAKARTA",
    "tanggal_lahir": "01-01-1990",
    "jenis_kelamin": "LAKI-LAKI",
    "alamat": "JL. CONTOH ALAMAT",
    "rt_rw": "001/002",
    "kel_desa": "KELURAHAN",
    "kecamatan": "KECAMATAN",
    "agama": "ISLAM",
    "status_perkawinan": "BELUM KAWIN",
    "pekerjaan": "PELAJAR/MAHASISWA",
    "kewarganegaraan": "WNI",
    "berlaku_hingga": "SEUMUR HIDUP"
  }
}
```
