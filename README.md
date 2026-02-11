# 🏗️ Geotechnical Analysis Platform

A professional web-based platform for soil suitability assessment in construction projects, providing automated geotechnical analysis and comprehensive reporting.

![Platform](https://img.shields.io/badge/Platform-Web-blue)
![Status](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-MIT-green)

## 📋 Table of Contents

- [Problem Statement](#problem-statement)
- [Solution](#solution)
- [Sustainable Development Goals](#sustainable-development-goals)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)

## 🎯 Problem Statement

### Current Challenges in Construction Industry

1. **Inadequate Soil Assessment**: Many construction projects, especially in developing regions, proceed without proper geotechnical investigation due to high costs and limited access to experts.

2. **Project Failures**: Improper soil analysis leads to:
   - Foundation failures and structural damage
   - Cost overruns (20-40% budget increase)
   - Project delays and safety hazards
   - Environmental degradation

3. **Limited Accessibility**: Traditional geotechnical services are:
   - Expensive (₹50,000 - ₹2,00,000 per site)
   - Time-consuming (2-4 weeks for reports)
   - Require specialized expertise
   - Not available in rural/remote areas

4. **Knowledge Gap**: Small-scale builders and individual homeowners lack:
   - Understanding of soil properties
   - Awareness of construction risks
   - Access to professional guidance
   - Tools for preliminary assessment

### Impact Statistics

- **60%** of foundation failures are due to inadequate soil investigation
- **₹10,000+ crores** annual losses in India due to poor soil assessment
- **30%** of rural construction projects face structural issues within 5 years
- **Limited** geotechnical engineers in tier-2 and tier-3 cities

## 💡 Solution

Our **Geotechnical Analysis Platform** provides:

### Automated Analysis
- Instant soil classification (USCS/IS standards)
- Rule-based suitability assessment for construction
- Risk identification and recommendations
- Professional PDF report generation

### Accessibility
- Web-based platform accessible anywhere
- User-friendly interface for non-experts
- Secure user authentication
- Educational resources and guides

### Report Management
- Historical data analysis
- Comparative report analysis
- Download previous reports
- Track analysis history

### Professional Standards
- Follows IS codes and USCS classification
- Comprehensive risk assessment
- Engineering recommendations
- Detailed documentation

## 🌍 Sustainable Development Goals (SDGs)

This project directly contributes to multiple UN Sustainable Development Goals:

### SDG 9: Industry, Innovation, and Infrastructure
**Target 9.1**: Develop quality, reliable, sustainable infrastructure
- Ensures proper foundation design through soil analysis
- Reduces infrastructure failures and maintenance costs
- Promotes sustainable construction practices

**Target 9.4**: Upgrade infrastructure with increased resource efficiency
- Optimizes material usage based on soil properties
- Reduces waste from construction failures
- Promotes efficient resource allocation

### SDG 11: Sustainable Cities and Communities
**Target 11.1**: Ensure access to adequate, safe housing
- Improves housing safety through proper soil assessment
- Makes geotechnical knowledge accessible to all
- Reduces housing failures in vulnerable communities

**Target 11.3**: Enhance inclusive and sustainable urbanization
- Supports planned urban development
- Enables informed decision-making for construction
- Promotes resilient infrastructure development

**Target 11.b**: Implement integrated disaster risk reduction
- Identifies soil-related construction risks
- Provides recommendations to mitigate hazards
- Reduces vulnerability to natural disasters

### SDG 12: Responsible Consumption and Production
**Target 12.2**: Sustainable management of natural resources
- Optimizes soil usage in construction
- Reduces material waste through proper planning
- Promotes efficient resource utilization

**Target 12.5**: Substantially reduce waste generation
- Prevents construction failures and demolition waste
- Reduces rework and material wastage
- Promotes circular economy in construction

### SDG 13: Climate Action
**Target 13.1**: Strengthen resilience to climate-related hazards
- Assesses soil behavior under different moisture conditions
- Identifies climate-related construction risks
- Promotes climate-resilient infrastructure

## ✨ Features

### Core Functionality

#### 1. Soil Analysis
- **11 Parameter Input**: Liquid Limit (LL), Plastic Limit (PL), Plasticity Index (PI), Gravel (G), Coarse Sand (CS), Medium Sand (MS), Fine Sand (FS), Fines (F), Optimum Moisture Content (OMC), Maximum Dry Density (MDD), Natural Moisture Content (NMC)
- **USCS/IS Classification**: Automatic soil type identification based on standard codes
- **Behavior Analysis**: Plasticity, compaction, and drainage characteristics
- **Suitability Rating**: Suitable / Moderately Suitable / Unsuitable

#### 2. Risk Assessment
- Foundation bearing capacity evaluation
- Compressibility and settlement analysis
- Expansive soil identification
- Moisture sensitivity assessment
- Drainage risk evaluation

#### 3. Engineering Recommendations
- Foundation type suggestions
- Soil improvement methods
- Compaction requirements
- Drainage system design
- Additional testing recommendations

#### 4. Report Generation
- Professional PDF reports with structured layout
- Comprehensive analysis documentation
- Laboratory test results summary
- Color-coded suitability indicators
- Engineering recommendations

#### 5. Report Management
- View all previous reports in organized grid
- Download historical analyses as PDF
- Compare two reports side-by-side
- Track analysis history with timestamps

### User Features

#### Authentication
- Secure user registration and login
- JWT-based authentication
- Bcrypt password encryption
- Session management

#### Dashboard
- Intuitive 11-parameter input form
- Real-time form validation
- Interactive results display with color coding
- One-click PDF report download

#### Comparison Tool
- Select any two reports for comparison
- Side-by-side parameter comparison
- Risk and recommendation analysis
- Visual difference highlighting

#### Educational Resources
- User guide with step-by-step instructions
- Soil classification explanation
- Result interpretation guide
- Best practices documentation

## 🛠️ Technology Stack

### Frontend
- **React 18** - Modern UI framework
- **Vite** - Fast build tool and dev server
- **Lucide React** - Professional icon library
- **Axios** - HTTP client for API calls
- **CSS3** - Custom styling with CSS variables

### Backend
- **Flask** - Lightweight Python web framework
- **Flask-CORS** - Cross-origin resource sharing
- **Flask-Bcrypt** - Secure password hashing
- **PyJWT** - JWT token authentication
- **ReportLab** - Professional PDF generation

### Database
- **MongoDB Atlas** - Cloud NoSQL database
- **PyMongo** - MongoDB driver for Python
- Collections: `users`, `reports`

## 📦 Installation

### Prerequisites
- Node.js 16+ and npm
- Python 3.8+
- MongoDB Atlas account

### Backend Setup

1. **Clone the repository:**
```bash
git clone <repository-url>
cd Civilathon/backend
```

2. **Create virtual environment:**
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Unix/MacOS:
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install flask flask-cors flask-bcrypt pymongo python-dotenv pyjwt reportlab
```

4. **Create `.env` file:**
```env
MONGODB_URI=your_mongodb_connection_string
SECRET_KEY=your_secret_key_here
```

5. **Run the server:**
```bash
python app.py
```

Backend runs on `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend:**
```bash
cd ../frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Run development server:**
```bash
npm run dev
```

Frontend runs on `http://localhost:5173`

## 🚀 Usage

### 1. Register/Login
- Create a new account with name, email, and password
- Login with existing credentials
- Secure JWT token-based authentication

### 2. Analyze Soil
- Navigate to "Analyze" tab
- Enter 11 soil parameters from laboratory tests:
  - Atterberg Limits: LL, PL, PI
  - Grain Size: Gravel, Coarse/Medium/Fine Sand, Fines
  - Compaction: OMC, MDD, NMC
- Click "Analyze Suitability"
- View comprehensive results with classification, risks, and recommendations

### 3. Download Report
- Click "Download PDF Report" button
- Professional PDF generated with:
  - Report header and metadata
  - Soil classification
  - Laboratory test results table
  - Suitability assessment
  - Soil behavior characteristics
  - Construction risks
  - Engineering recommendations

### 4. View Reports
- Navigate to "Reports" tab
- View all previous analyses in card layout
- Each card shows:
  - Soil classification
  - Suitability status with color-coded badge
  - Creation date
  - Summary of risks and recommendations
- Download any historical report

### 5. Compare Reports
- Select two reports by clicking on cards
- Click "Compare" button
- View side-by-side comparison of:
  - All parameters
  - Classifications
  - Suitability assessments
  - Risks and recommendations

### 6. Learn More
- Check "Guide" tab for detailed instructions
- Read "About" for platform information
- Understand result interpretation

## 📁 Project Structure

```
Civilathon/
├── backend/
│   ├── reports/             # Generated PDF reports
│   ├── app.py              # Main Flask application
│   ├── .env                # Environment variables
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── About.jsx       # About page component
│   │   ├── App.jsx         # Main app component
│   │   ├── App.css         # Global styles
│   │   ├── Disclaimer.jsx  # Disclaimer component
│   │   ├── Guide.jsx       # User guide component
│   │   ├── Login.jsx       # Login component
│   │   ├── Register.jsx    # Registration component
│   │   ├── Reports.jsx     # Reports management & comparison
│   │   ├── api.js          # API client configuration
│   │   └── main.jsx        # Entry point
│   ├── package.json        # Node dependencies
│   └── vite.config.js      # Vite configuration
└── README.md               # This file
```

## 📡 API Documentation

### Authentication Endpoints

#### POST `/api/register`
Register new user

**Request:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "message": "User registered successfully"
}
```

#### POST `/api/login`
User login

**Request:**
```json
{
  "email": "john@example.com",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "token": "jwt_token_here",
  "user": {
    "name": "John Doe",
    "email": "john@example.com"
  }
}
```

### Analysis Endpoints

#### POST `/api/analyze-suitability`
Analyze soil suitability (requires authentication)

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Request:**
```json
{
  "soil_data": {
    "LL": 45,
    "PL": 25,
    "PI": 20,
    "G": 10,
    "CS": 20,
    "MS": 15,
    "FS": 10,
    "F": 45,
    "OMC%": 18,
    "MDD (kN/m3)": 17.5,
    "NMC (%)": 15
  }
}
```

**Response:**
```json
{
  "report_id": "report_id_here",
  "classification": "CL - Clay of Low Plasticity",
  "behavior": ["Highly plastic - prone to volume changes with moisture"],
  "suitability": "MODERATELY SUITABLE",
  "suitability_text": "Moderately suitable - requires soil improvement measures",
  "risks": ["Moderate bearing capacity - may require deeper foundations"],
  "recommendations": ["Install proper drainage system to control groundwater"],
  "parameters": { ... }
}
```

#### POST `/api/generate-report`
Generate PDF report (requires authentication)

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Request:**
```json
{
  "result": { /* analysis result object */ }
}
```

**Response:**
PDF file download

#### GET `/api/my-reports`
Get user's reports (requires authentication)

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response:**
```json
{
  "reports": [
    {
      "_id": "report_id",
      "classification": "CL - Clay of Low Plasticity",
      "suitability": "MODERATELY SUITABLE",
      "created_at": "2024-02-06T10:30:00",
      ...
    }
  ]
}
```

### Health Check

#### GET `/api/health`
Check API status

**Response:**
```json
{
  "status": "healthy",
  "message": "Soil Data Management API is running"
}
```

## 📄 License

This project is licensed under the MIT License.

## 👥 Team

Developed for Civilathon - Building sustainable infrastructure solutions

## 🙏 Acknowledgments

- Indian Standard (IS) codes for soil classification
- USCS (Unified Soil Classification System)
- Construction industry professionals for insights
- Open-source community for tools and libraries

---

**Note**: This platform provides preliminary analysis for educational and reference purposes. Professional geotechnical investigation and licensed engineer review are required before actual construction.

**Disclaimer**: Always consult qualified geotechnical engineers for construction projects. This tool is meant to assist, not replace, professional expertise.
