# Technical Screening API

A minimal FastAPI application for payment calculations.

## Features
- **POST /calculate**: Calculate monthly payment amount
  - Request: `{"amount": number, "rate": number}`
  - Response: `{"monthly": calculated_monthly_amount}`
- **GET /health**: Health check endpoint returning status and timestamp

## Setup & Installation

### Prerequisites
- Python 3.8+
- pip

### Installation

1. Clone the repository:
```bash
git clone https://github.com/postumelo17-ctrl/Technical-screening.git
cd Technical-screening
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

### Development
```bash
python app.py
```

The API will be available at `http://localhost:8000`

### With Docker
```bash
docker build -t technical-screening .
docker run -p 8000:8000 technical-screening
```

## API Examples

### Calculate Endpoint
```bash
curl -X POST http://localhost:8000/calculate \
  -H "Content-Type: application/json" \
  -d '{"amount": 100000, "rate": 0.05}'
```

Response: `{"monthly": 416.66666666666663}`

### Health Check
```bash
curl http://localhost:8000/health
```

Response: `{"status": "healthy", "timestamp": "2026-06-08T10:00:00.000000"}`

## Testing

Run the test suite:
```bash
pytest tests/
```

## Documentation

Interactive API documentation available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
