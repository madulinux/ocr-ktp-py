# KTP OCR API Documentation

## Overview

This API provides OCR (Optical Character Recognition) capabilities for Indonesian ID cards (KTP). It uses Google Cloud Vision API for text recognition and custom processing to extract structured information from KTP images.

## Base URL

When running locally:
```
http://localhost:5001
```

When deployed via Docker:
```
http://<host-ip>:5001
```

## Authentication

Currently, the API does not implement authentication. If deploying to production, it is recommended to add an authentication layer.

## Endpoints

### Health Check

Verifies that the API service is running properly.

```
GET /health
```

#### Request

No parameters required.

#### Response

**Status Code:** 200 OK

```json
{
  "status": "ok"
}
```

### OCR KTP

Process an Indonesian ID card (KTP) image and extract information.

```
POST /ocr/ktp
```

#### Request

**Content-Type:** multipart/form-data

**Parameters:**

| Name  | Type | Required | Description |
|-------|------|----------|-------------|
| image | File | Yes      | The KTP image file to be processed. Supported formats: JPEG, PNG |

#### Response

**Success Response:**

**Status Code:** 200 OK

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

**Error Response:**

**Status Code:** 400 Bad Request

```json
{
  "error": "No image file provided"
}
```

**Status Code:** 500 Internal Server Error

```json
{
  "success": false,
  "error": "Error message details"
}
```

## Response Fields Description

The OCR KTP endpoint returns a JSON object with the following fields:

| Field   | Type    | Description |
|---------|---------|-------------|
| success | Boolean | Indicates if the request was successful |
| score   | Float   | Confidence score of the OCR result (0-1) |
| content | Object  | Extracted information from the KTP |

### Content Object Fields

| Field             | Type   | Description |
|-------------------|--------|-------------|
| nik               | String | National Identity Number (16 digits) |
| nama              | String | Full name |
| tempat_lahir      | String | Place of birth |
| tanggal_lahir     | String | Date of birth (format: DD-MM-YYYY) |
| jenis_kelamin     | String | Gender ("LAKI-LAKI" or "PEREMPUAN") |
| alamat            | String | Address |
| rt_rw             | String | RT/RW (neighborhood/community units) |
| kel_desa          | String | Village/Sub-district |
| kecamatan         | String | District |
| agama             | String | Religion |
| status_perkawinan | String | Marital status |
| pekerjaan         | String | Occupation |
| kewarganegaraan   | String | Nationality |
| berlaku_hingga    | String | Validity period |

## Code Examples

### cURL

```bash
curl -X POST -F "image=@/path/to/ktp.jpg" http://localhost:5001/ocr/ktp
```

### Python

```python
import requests

url = "http://localhost:5001/ocr/ktp"

files = {
    "image": ("ktp.jpg", open("/path/to/ktp.jpg", "rb"), "image/jpeg")
}

response = requests.post(url, files=files)
print(response.json())
```

### JavaScript (Fetch API)

```javascript
const formData = new FormData();
const fileField = document.querySelector('input[type="file"]');

formData.append('image', fileField.files[0]);

fetch('http://localhost:5001/ocr/ktp', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(result => {
  console.log('Success:', result);
})
.catch(error => {
  console.error('Error:', error);
});
```

### PHP

```php
<?php
$url = 'http://localhost:5001/ocr/ktp';
$image = new CURLFile('/path/to/ktp.jpg', 'image/jpeg', 'ktp.jpg');

$data = array('image' => $image);

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

$response = curl_exec($ch);
curl_close($ch);

echo $response;
?>
```

## Error Handling

The API returns appropriate HTTP status codes along with error messages in the response body. Common error scenarios include:

- **400 Bad Request**: Missing required parameters or invalid input
- **500 Internal Server Error**: Server-side errors during processing

## Dependencies

This API relies on the Google Cloud Vision API for OCR functionality. Ensure that:

1. You have a valid Google Cloud account with the Vision API enabled
2. The `GOOGLE_APPLICATION_CREDENTIALS` environment variable is set to the path of your service account key file

## Rate Limiting

Currently, there is no rate limiting implemented. When deploying to production, consider adding rate limiting to prevent abuse.

## Notes

- Image processing may take a few seconds depending on the image size and quality
- For optimal results, ensure the KTP image is clear, well-lit, and properly aligned
- The API works best with images that contain a single KTP with all fields visible
