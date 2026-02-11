# Soil Data Management and Prediction Platform - Backend

## Setup Instructions

### 1. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Health Check
- **GET** `/api/health`
- Returns API status

### Get All Datasets
- **GET** `/api/datasets`
- Returns both datasets with their data and metadata

### Get Specific Dataset
- **GET** `/api/dataset/<dataset_id>`
- Returns dataset (1 or 2) with statistics

### Get Statistics
- **GET** `/api/statistics`
- Returns statistical analysis, correlations, and missing values

### Train Model
- **POST** `/api/train`
- Body: `{"target": "column_name", "dataset_id": 1}`
- Trains a Random Forest model for prediction

### Make Prediction
- **POST** `/api/predict`
- Body: `{"target": "column_name", "dataset_id": 1, "input_data": {...}}`
- Returns prediction based on trained model

## Features

- Soil data management with two datasets
- Statistical analysis and correlations
- Machine Learning predictions using Random Forest
- Model persistence for reuse
- RESTful API with CORS support
