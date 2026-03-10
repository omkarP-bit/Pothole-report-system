-- Supabase PostgreSQL Schema - Hackathon Optimized
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "postgis";

CREATE TABLE custom_user (
    id SERIAL PRIMARY KEY,
    user_id UUID DEFAULT uuid_generate_v4() UNIQUE NOT NULL,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    phone_number VARCHAR(15),
    password_hash VARCHAR(255) NOT NULL,
    credits INTEGER DEFAULT 0,
    is_staff BOOLEAN DEFAULT FALSE,
    badge_level VARCHAR(20) DEFAULT 'BRONZE',
    total_reports INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE pothole_report (
    id SERIAL PRIMARY KEY,
    report_id UUID DEFAULT uuid_generate_v4() UNIQUE NOT NULL,
    user_id UUID REFERENCES custom_user(user_id) ON DELETE CASCADE,
    image_url VARCHAR(500),
    s3_bucket_path VARCHAR(300),
    description TEXT,
    location_name VARCHAR(200),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    location_point GEOMETRY(POINT, 4326),
    severity VARCHAR(20) CHECK (severity IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')) NOT NULL,
    status VARCHAR(20) CHECK (status IN ('PENDING', 'VERIFIED', 'REJECTED', 'IN_PROGRESS', 'COMPLETED')) DEFAULT 'PENDING',
    credits_awarded INTEGER DEFAULT 5,
    ai_confidence DECIMAL(5,2),
    estimated_cost DECIMAL(10,2),
    priority_score INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE municipal_verification (
    id SERIAL PRIMARY KEY,
    report_id UUID REFERENCES pothole_report(report_id) ON DELETE CASCADE,
    verified_by VARCHAR(100),
    verification_status VARCHAR(20) CHECK (verification_status IN ('APPROVED', 'REJECTED', 'NEED_INFO')),
    verification_notes TEXT,
    verification_date TIMESTAMP DEFAULT NOW(),
    estimated_repair_date DATE
);

CREATE TABLE accident_predictions (
    id SERIAL PRIMARY KEY,
    report_id UUID REFERENCES pothole_report(report_id) ON DELETE CASCADE,
    risk_level VARCHAR(20) CHECK (risk_level IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')),
    accident_probability DECIMAL(5,2),
    factors JSONB,
    recommendations TEXT[],
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE repair_teams (
    id SERIAL PRIMARY KEY,
    team_id UUID DEFAULT uuid_generate_v4() UNIQUE NOT NULL,
    team_name VARCHAR(100) NOT NULL,
    contact_info JSONB,
    current_location GEOMETRY(POINT, 4326),
    status VARCHAR(20) DEFAULT 'AVAILABLE',
    specialization VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE work_orders (
    id SERIAL PRIMARY KEY,
    order_id UUID DEFAULT uuid_generate_v4() UNIQUE NOT NULL,
    report_id UUID REFERENCES pothole_report(report_id),
    team_id UUID REFERENCES repair_teams(team_id),
    priority VARCHAR(20) DEFAULT 'MEDIUM',
    estimated_duration INTEGER,
    actual_duration INTEGER,
    cost DECIMAL(10,2),
    materials_used JSONB,
    status VARCHAR(20) DEFAULT 'ASSIGNED',
    scheduled_date DATE,
    completed_date DATE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE analytics_dashboard (
    id SERIAL PRIMARY KEY,
    metric_name VARCHAR(100),
    metric_value DECIMAL(15,2),
    metric_type VARCHAR(50),
    time_period VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES custom_user(user_id),
    title VARCHAR(200),
    message TEXT,
    type VARCHAR(50),
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_user_id ON custom_user(user_id);
CREATE INDEX idx_username ON custom_user(username);
CREATE INDEX idx_report_location ON pothole_report USING GIST(location_point);
CREATE INDEX idx_report_status ON pothole_report(status);
CREATE INDEX idx_report_severity ON pothole_report(severity);
CREATE INDEX idx_report_priority ON pothole_report(priority_score DESC);
CREATE INDEX idx_predictions_risk ON accident_predictions(risk_level);
CREATE INDEX idx_teams_location ON repair_teams USING GIST(current_location);
CREATE INDEX idx_work_orders_status ON work_orders(status);

-- Triggers
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE OR REPLACE FUNCTION update_location_point()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.latitude IS NOT NULL AND NEW.longitude IS NOT NULL THEN
        NEW.location_point = ST_SetSRID(ST_MakePoint(NEW.longitude, NEW.latitude), 4326);
    END IF;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE OR REPLACE FUNCTION calculate_priority_score()
RETURNS TRIGGER AS $$
BEGIN
    NEW.priority_score = 
        CASE NEW.severity
            WHEN 'CRITICAL' THEN 100
            WHEN 'HIGH' THEN 75
            WHEN 'MEDIUM' THEN 50
            WHEN 'LOW' THEN 25
        END +
        CASE 
            WHEN NEW.created_at < NOW() - INTERVAL '7 days' THEN 20
            WHEN NEW.created_at < NOW() - INTERVAL '3 days' THEN 10
            ELSE 0
        END;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_pothole_report_updated_at
    BEFORE UPDATE ON pothole_report
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_pothole_location_point
    BEFORE INSERT OR UPDATE ON pothole_report
    FOR EACH ROW
    EXECUTE FUNCTION update_location_point();

CREATE TRIGGER calculate_report_priority
    BEFORE INSERT OR UPDATE ON pothole_report
    FOR EACH ROW
    EXECUTE FUNCTION calculate_priority_score();

-- Views for Analytics
CREATE VIEW dashboard_stats AS
SELECT 
    COUNT(*) as total_reports,
    COUNT(*) FILTER (WHERE status = 'PENDING') as pending_reports,
    COUNT(*) FILTER (WHERE status = 'COMPLETED') as completed_reports,
    COUNT(*) FILTER (WHERE severity = 'CRITICAL') as critical_reports,
    AVG(priority_score) as avg_priority,
    COUNT(*) FILTER (WHERE created_at >= NOW() - INTERVAL '24 hours') as reports_today
FROM pothole_report;

CREATE VIEW high_risk_areas AS
SELECT 
    location_name,
    COUNT(*) as report_count,
    AVG(priority_score) as avg_priority,
    ST_Centroid(ST_Collect(location_point)) as center_point
FROM pothole_report 
WHERE status IN ('PENDING', 'VERIFIED', 'IN_PROGRESS')
GROUP BY location_name
HAVING COUNT(*) >= 3
ORDER BY avg_priority DESC;

-- Sample Data
INSERT INTO custom_user (username, email, password_hash, is_staff, credits, badge_level, total_reports) VALUES
('municipal_admin', 'admin@municipal.gov', 'pbkdf2:sha256:260000$salt$hash', TRUE, 0, 'ADMIN', 0),
('john_doe', 'john@example.com', 'pbkdf2:sha256:260000$salt$hash', FALSE, 150, 'GOLD', 25),
('jane_smith', 'jane@example.com', 'pbkdf2:sha256:260000$salt$hash', FALSE, 75, 'SILVER', 12);

INSERT INTO repair_teams (team_name, contact_info, specialization, status) VALUES
('Alpha Team', '{"phone": "+1234567890", "email": "alpha@repair.com"}', 'EMERGENCY', 'AVAILABLE'),
('Beta Team', '{"phone": "+1234567891", "email": "beta@repair.com"}', 'ROUTINE', 'BUSY');

INSERT INTO pothole_report (user_id, description, location_name, latitude, longitude, severity, status) VALUES
((SELECT user_id FROM custom_user WHERE username = 'john_doe'), 
 'Critical pothole causing accidents', 'Main St & 1st Ave', 40.7128, -74.0060, 'CRITICAL', 'PENDING'),
((SELECT user_id FROM custom_user WHERE username = 'jane_smith'), 
 'Medium sized pothole', 'Oak Ave', 40.7500, -73.9850, 'MEDIUM', 'VERIFIED');

-- Functions for ML Integration
CREATE OR REPLACE FUNCTION get_nearby_reports(lat DECIMAL, lng DECIMAL, radius_km DECIMAL DEFAULT 1.0)
RETURNS TABLE(report_id UUID, distance_km DECIMAL) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        pr.report_id,
        ROUND(ST_Distance(ST_SetSRID(ST_MakePoint(lng, lat), 4326), pr.location_point) / 1000, 2) as distance_km
    FROM pothole_report pr
    WHERE ST_DWithin(ST_SetSRID(ST_MakePoint(lng, lat), 4326), pr.location_point, radius_km * 1000)
    ORDER BY distance_km;
END;
$$ LANGUAGE plpgsql;