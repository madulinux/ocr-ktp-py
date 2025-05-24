# OCR KTP API

A lightweight Flask API for Indonesian ID card (KTP) OCR processing. This application uses Google Cloud Vision API for text recognition and custom processing to extract structured information from KTP images.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Running Locally](#running-locally)
- [Running with Docker](#running-with-docker)
- [API Endpoints](#api-endpoints)
- [Detailed Documentation](#detailed-documentation)

## Prerequisites

- Python 3.6+ (for local development)
- Docker and Docker Compose (for containerized deployment)
- Google Cloud Vision API credentials

## Running Locally

1. Set up a Python virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up Google Cloud Vision API credentials:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/your-credentials.json"
   ```

4. Run the application:
   ```bash
   python app.py
   ```

   The API will be available at http://localhost:5001

## Running with Docker

1. Make sure Docker and Docker Compose are installed on your system.

2. Configure your environment variables:
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit the .env file with your preferred settings
   nano .env  # or use any text editor
   ```

3. Build and start the container:
   ```bash
   docker-compose up -d
   ```

   This will build the Docker image and start the container in detached mode.

4. To provide Google Cloud credentials, either:
   - Set the `GOOGLE_APPLICATION_CREDENTIALS` path in your .env file, or
   - Place your credentials file as `credentials.json` in the project root directory

5. The API will be available at the port specified in your .env file (default: http://localhost:5001)

6. To stop the container:
   ```bash
   docker-compose down
   ```

### Environment Variables

The following environment variables can be configured in the .env file:

| Variable | Description | Default |
|----------|-------------|---------|
| PORT | The port on which the API will run | 5001 |
| DEBUG | Enable debug mode (True/False) | False |
| GOOGLE_APPLICATION_CREDENTIALS | Path to Google Cloud credentials file | - |

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

**Example with cURL:**
```bash
curl -X POST -F "image=@/path/to/ktp.jpg" http://localhost:5001/ocr/ktp
```

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

## Detailed Documentation

For more detailed API documentation, code examples in different programming languages, and error handling information, please refer to the [API_DOCUMENTATION.md](API_DOCUMENTATION.md) file.
