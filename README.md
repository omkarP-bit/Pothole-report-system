# 🚧 AI-Based Pothole Report System

> Smart infrastructure management with machine learning-driven accident prediction and risk analysis

## 🎯 Overview

An intelligent pothole reporting system that enables citizens to report road infrastructure issues while providing government officials with AI-powered insights for optimal resource allocation and proactive accident prevention.

## ✨ Key Features

### 👥 **Citizen Portal**
- 📱 Simple pothole reporting with photo upload
- 📍 GPS-based location tracking
- 🏆 Credit system with achievement badges
- 📊 Personal dashboard with report history
- 📱 Mobile-responsive interface

### 🏛️ **Government Dashboard**
- 🤖 **AI-powered accident risk prediction**
- 📈 Real-time analytics and reporting
- 🗺️ Interactive risk heatmap visualization
- 💰 Resource optimization recommendations
- 👥 Repair team coordination
- 📋 Work order management system

### 🧠 **Machine Learning Engine**
- Accident probability calculation based on multiple factors
- Weather and traffic impact analysis
- Dynamic priority scoring algorithm
- Predictive maintenance recommendations
- Geospatial clustering and pattern analysis

## 🛠️ Technology Stack

- **Backend:** Flask, SQLAlchemy, PostgreSQL with PostGIS
- **Machine Learning:** Scikit-learn, NumPy, Pandas
- **Cloud Storage:** AWS S3 for secure image storage
- **Database:** Supabase PostgreSQL with geospatial extensions
- **Deployment:** Docker containerization
- **APIs:** RESTful architecture with CORS support

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- PostgreSQL database (Supabase recommended)
- AWS S3 bucket for image storage

### 1. Clone Repository
```bash
git clone https://github.com/omkarP-bit/Pothole-report-system.git
cd Pothole-report-system
```

### 2. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Configure your credentials in .env file
```

### 3. Database Setup
- Create a Supabase project at https://supabase.com
- Execute the SQL schema from `database/supabase_schema.sql`
- Update `SUPABASE_DB_URL` in your `.env` file

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

### 6. Docker Deployment (Optional)
```bash
docker build -t pothole-system .
docker run -p 5000:5000 pothole-system
```

## 📊 API Documentation

### **User Management**
- `POST /register` - User registration
- `POST /login` - User authentication
- `GET /api/user-profile` - User profile information

### **Report Management**
- `POST /report-pothole` - Submit new pothole report
- `GET /api/my-reports` - Retrieve user's reports
- `GET /api/public-reports` - Public verified reports

### **Government APIs**
- `GET /api/pending-reports` - Reports awaiting verification
- `POST /api/verify-report` - Verify or reject reports
- `POST /api/update-progress` - Update repair progress

### **Analytics & ML APIs**
- `GET /api/risk-analysis/<report_id>` - Individual risk analysis
- `GET /api/area-risk-analysis` - Area-wide risk assessment
- `GET /api/v2/dashboard-analytics` - Real-time statistics
- `GET /api/v2/risk-heatmap` - Risk visualization data
- `GET /api/v2/smart-predictions` - ML-powered predictions

## 🎮 Gamification System

| Badge Level | Credits | Description |
|-------------|---------|-------------|
| 🥉 Bronze   | 0-50    | New contributor |
| 🥈 Silver   | 51-150  | Active reporter |
| 🥇 Gold     | 151-300 | Community champion |
| 💎 Diamond  | 300+    | Infrastructure hero |

## 🧠 Machine Learning Model

### Risk Assessment Factors
- **Severity Classification** (Low, Medium, High, Critical)
- **Geographic Density** (nearby reports within radius)
- **Temporal Analysis** (time since initial report)
- **Environmental Conditions** (weather impact factors)
- **Traffic Patterns** (volume and flow analysis)

### Prediction Outputs
- Accident probability percentage (0-100%)
- Risk level classification
- Estimated repair cost
- Priority score for resource allocation
- Actionable maintenance recommendations

## 📁 Project Structure

```
├── app.py                    # Main Flask application
├── advanced_ml.py           # Machine learning prediction engine
├── advanced_api.py           # Advanced API endpoints
├── ml_model.py              # Core ML model implementation
├── config.py                # Application configuration
├── requirements.txt         # Python dependencies
├── Dockerfile              # Container configuration
├── database/
│   └── supabase_schema.sql # PostgreSQL database schema
├── templates/              # HTML templates
├── static/                 # CSS and JavaScript assets
└── .env.example           # Environment configuration template
```

## 🔧 Configuration

### Required Environment Variables
```env
# Database Configuration
SUPABASE_DB_URL=postgresql://user:password@host:port/database

# AWS S3 Configuration
AWS_ACCESS_KEY_ID=your_access_key_id
AWS_SECRET_ACCESS_KEY=your_secret_access_key
AWS_BUCKET_NAME=your_s3_bucket_name
AWS_REGION=your_aws_region

# Application Security
SECRET_KEY=your_flask_secret_key
```

## 📈 Performance Features

- **Optimized Database Queries** with proper indexing
- **Geospatial Indexing** for fast location-based searches
- **Connection Pooling** for database efficiency
- **Caching Support** with Redis integration
- **Background Processing** with Celery task queue
- **API Rate Limiting** for system protection

## 🌍 Social Impact

This system addresses critical urban infrastructure challenges:

- **Improved Road Safety** through predictive accident prevention
- **Efficient Resource Allocation** for government maintenance teams
- **Enhanced Citizen Engagement** in community infrastructure
- **Data-Driven Decision Making** for urban planning
- **Proactive Maintenance** reducing long-term costs

## 🤝 Contributing

We welcome contributions to improve the system:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For questions, issues, or contributions, please:
- Open an issue on GitHub
- Contact the development team
- Check the documentation wiki

---

**Building safer roads through intelligent technology** 🛣️✨