# 🚧 AI-Powered Pothole Report System

> **Hackathon-Ready** | Smart city infrastructure management with ML-driven accident prediction

## 🎯 Overview

An intelligent pothole reporting system that empowers citizens to report road issues while providing government officials with AI-powered insights for optimal resource allocation and accident prevention.

## ✨ Key Features

### 🔍 **For Citizens**
- 📱 Easy pothole reporting with photo upload
- 📍 GPS location tracking
- 🏆 Gamification with credits & badges
- 📊 Personal dashboard with report history

### 🏛️ **For Government**
- 🤖 **ML-powered accident risk prediction**
- 📈 Real-time analytics dashboard
- 🗺️ Risk heatmap visualization
- 💰 Cost optimization suggestions
- 👥 Repair team management
- 📋 Work order tracking

### 🧠 **AI/ML Capabilities**
- Accident probability calculation
- Weather & traffic impact analysis
- Priority scoring algorithm
- Resource optimization recommendations
- Geospatial clustering analysis

## 🛠️ Tech Stack

- **Backend:** Flask, SQLAlchemy, PostgreSQL (Supabase)
- **ML/AI:** Scikit-learn, NumPy, Pandas
- **Storage:** AWS S3 for image uploads
- **Database:** PostgreSQL with PostGIS extension
- **Deployment:** Docker, CORS-enabled APIs
- **Frontend Ready:** RESTful APIs for any frontend

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/omkarP-bit/Pothole-report-system.git
cd Pothole-report-system
```

### 2. Environment Setup
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your credentials
nano .env
```

### 3. Database Setup
- Create Supabase project
- Run `database/supabase_schema.sql` in Supabase SQL Editor
- Update `SUPABASE_DB_URL` in `.env`

### 4. Install & Run
```bash
# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
```

### 5. Docker Deployment
```bash
docker build -t pothole-system .
docker run -p 5000:5000 pothole-system
```

## 📊 API Endpoints

### **Core APIs**
- `POST /register` - User registration
- `POST /login` - User authentication
- `POST /report-pothole` - Submit pothole report
- `GET /api/my-reports` - User's reports

### **Hackathon APIs (v2)**
- `GET /api/v2/dashboard-analytics` - Real-time statistics
- `GET /api/v2/risk-heatmap` - Risk visualization data
- `GET /api/v2/smart-predictions` - ML predictions
- `GET /api/v2/optimization-suggestions` - Resource optimization
- `GET /api/v2/citizen-leaderboard` - Gamification data

### **Government APIs**
- `GET /api/pending-reports` - Reports awaiting verification
- `POST /api/verify-report` - Verify/reject reports
- `GET /api/area-risk-analysis` - Area-wide risk assessment

## 🎮 Gamification System

| Badge Level | Credits Required | Benefits |
|-------------|------------------|----------|
| 🥉 Bronze   | 0-50            | Basic reporting |
| 🥈 Silver   | 51-150          | Priority support |
| 🥇 Gold     | 151-300         | Special recognition |
| 💎 Diamond  | 300+            | VIP status |

## 🧠 ML Model Features

### Risk Prediction Factors
- **Severity Level** (Low/Medium/High/Critical)
- **Location Density** (nearby reports count)
- **Time Decay** (days since report)
- **Weather Impact** (sunny/rainy/snowy)
- **Traffic Volume** (low/medium/high)

### Output Metrics
- Accident probability percentage
- Risk level classification
- Estimated repair cost
- Priority score (0-100)
- Actionable recommendations

## 📁 Project Structure

```
├── app.py                 # Main Flask application
├── advanced_ml.py         # ML prediction model
├── hackathon_api.py       # Advanced API endpoints
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container configuration
├── database/
│   └── supabase_schema.sql # Database schema
├── templates/            # HTML templates
├── static/              # CSS/JS assets
└── .env.example         # Environment template
```

## 🌟 Hackathon Highlights

### **Innovation**
- Real-time ML predictions for accident prevention
- Geospatial analysis for optimal resource allocation
- Gamification to boost citizen engagement

### **Technical Excellence**
- Scalable PostgreSQL with PostGIS
- Docker containerization
- RESTful API design
- Advanced ML algorithms

### **Social Impact**
- Improved road safety
- Efficient government resource utilization
- Enhanced citizen participation in city management

## 🔧 Configuration

### Environment Variables
```env
SUPABASE_DB_URL=postgresql://user:pass@host:port/db
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_BUCKET_NAME=your_bucket
AWS_REGION=us-east-1
SECRET_KEY=your_flask_secret
```

## 📈 Performance Features

- **Database Indexing** for fast geospatial queries
- **Connection Pooling** with Supabase
- **Caching** with Redis support
- **Background Tasks** with Celery
- **CORS** enabled for frontend integration

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏆 Awards & Recognition

Built for hackathons with enterprise-grade features:
- ✅ Real-time ML predictions
- ✅ Scalable architecture
- ✅ Government-ready APIs
- ✅ Citizen engagement tools
- ✅ Production deployment ready

---

**Made with ❤️ for smart cities and safer roads**