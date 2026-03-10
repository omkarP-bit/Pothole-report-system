from flask import Blueprint, request, jsonify, session
from functools import wraps
from advanced_ml import AdvancedAccidentPredictor
from datetime import datetime, timedelta
import json

# Create blueprint for advanced APIs
advanced_api = Blueprint('advanced_api', __name__)
advanced_predictor = AdvancedAccidentPredictor()

def staff_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or not session.get('is_staff'):
            return jsonify({'error': 'Staff access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

@advanced_api.route('/api/v2/dashboard-analytics')
@staff_required
def dashboard_analytics():
    """Advanced analytics for government dashboard"""
    from app import db
    
    # Execute raw SQL for performance
    stats = db.session.execute("""
        SELECT 
            COUNT(*) as total_reports,
            COUNT(*) FILTER (WHERE status = 'PENDING') as pending,
            COUNT(*) FILTER (WHERE status = 'COMPLETED') as completed,
            COUNT(*) FILTER (WHERE severity = 'CRITICAL') as critical,
            AVG(priority_score) as avg_priority,
            COUNT(*) FILTER (WHERE created_at >= NOW() - INTERVAL '24 hours') as today
        FROM pothole_report
    """).fetchone()
    
    return jsonify({
        'total_reports': stats[0],
        'pending_reports': stats[1],
        'completed_reports': stats[2],
        'critical_reports': stats[3],
        'average_priority': round(float(stats[4] or 0), 1),
        'reports_today': stats[5],
        'completion_rate': round((stats[2] / max(stats[0], 1)) * 100, 1)
    })

@advanced_api.route('/api/v2/risk-heatmap')
@staff_required
def risk_heatmap():
    """Generate risk heatmap for map visualization"""
    from app import PotholeReport
    
    reports = PotholeReport.query.filter(
        PotholeReport.status.in_(['PENDING', 'VERIFIED', 'IN_PROGRESS']),
        PotholeReport.latitude.isnot(None),
        PotholeReport.longitude.isnot(None)
    ).all()
    
    reports_data = [{
        'report_id': r.report_id,
        'latitude': float(r.latitude),
        'longitude': float(r.longitude),
        'severity': r.severity,
        'created_at': r.created_at.strftime('%Y-%m-%d %H:%M')
    } for r in reports]
    
    heatmap_data = advanced_predictor.generate_area_heatmap(reports_data)
    return jsonify(heatmap_data)

@advanced_api.route('/api/v2/smart-predictions')
@staff_required
def smart_predictions():
    """AI-powered predictions with environmental factors"""
    from app import PotholeReport
    
    weather = request.args.get('weather', 'sunny')
    traffic = request.args.get('traffic', 'medium')
    
    reports = PotholeReport.query.filter(
        PotholeReport.status.in_(['PENDING', 'VERIFIED', 'IN_PROGRESS'])
    ).all()
    
    predictions = []
    all_reports_data = [{
        'report_id': r.report_id,
        'latitude': float(r.latitude) if r.latitude else 0,
        'longitude': float(r.longitude) if r.longitude else 0,
        'severity': r.severity,
        'created_at': r.created_at.strftime('%Y-%m-%d %H:%M')
    } for r in reports if r.latitude and r.longitude]
    
    for report in reports[:20]:  # Limit for performance
        if report.latitude and report.longitude:
            report_data = {
                'report_id': report.report_id,
                'latitude': float(report.latitude),
                'longitude': float(report.longitude),
                'severity': report.severity,
                'created_at': report.created_at.strftime('%Y-%m-%d %H:%M')
            }
            
            prediction = advanced_predictor.predict_comprehensive_risk(
                report_data, all_reports_data, weather, traffic
            )
            
            predictions.append({
                'report_id': report.report_id,
                'location_name': report.location_name,
                'risk_analysis': prediction
            })
    
    return jsonify(predictions)

@advanced_api.route('/api/v2/optimization-suggestions')
@staff_required
def optimization_suggestions():
    """Resource optimization suggestions"""
    from app import db
    
    # Find high-density areas for bulk repairs
    high_density_areas = db.session.execute("""
        SELECT 
            location_name,
            COUNT(*) as report_count,
            AVG(priority_score) as avg_priority,
            STRING_AGG(report_id::text, ',') as report_ids
        FROM pothole_report 
        WHERE status IN ('PENDING', 'VERIFIED') 
        AND location_name IS NOT NULL
        GROUP BY location_name
        HAVING COUNT(*) >= 2
        ORDER BY avg_priority DESC
        LIMIT 10
    """).fetchall()
    
    suggestions = []
    for area in high_density_areas:
        total_cost = area[1] * 400  # Estimated cost per repair
        bulk_discount = total_cost * 0.15  # 15% bulk discount
        
        suggestions.append({
            'type': 'BULK_REPAIR',
            'location': area[0],
            'report_count': area[1],
            'priority_score': round(float(area[2]), 1),
            'estimated_cost': total_cost,
            'potential_savings': round(bulk_discount, 2),
            'report_ids': area[3].split(','),
            'recommendation': f'Deploy team for bulk repair of {area[1]} potholes'
        })
    
    return jsonify(suggestions)

@advanced_api.route('/api/v2/citizen-leaderboard')
def citizen_leaderboard():
    """Gamification leaderboard"""
    from app import db
    
    leaderboard = db.session.execute("""
        SELECT 
            u.username,
            u.credits,
            u.badge_level,
            u.total_reports,
            COUNT(pr.id) as verified_reports
        FROM custom_user u
        LEFT JOIN pothole_report pr ON u.user_id = pr.user_id AND pr.status = 'VERIFIED'
        WHERE u.is_staff = FALSE
        GROUP BY u.user_id, u.username, u.credits, u.badge_level, u.total_reports
        ORDER BY u.credits DESC
        LIMIT 10
    """).fetchall()
    
    return jsonify([{
        'rank': idx + 1,
        'username': row[0],
        'credits': row[1],
        'badge': row[2],
        'total_reports': row[3],
        'verified_reports': row[4]
    } for idx, row in enumerate(leaderboard)])

@advanced_api.route('/api/v2/real-time-stats')
def real_time_stats():
    """Real-time statistics for live dashboard"""
    from app import db
    
    stats = db.session.execute("""
        SELECT 
            COUNT(*) FILTER (WHERE created_at >= NOW() - INTERVAL '1 hour') as reports_last_hour,
            COUNT(*) FILTER (WHERE status = 'IN_PROGRESS') as active_repairs,
            COUNT(*) FILTER (WHERE severity = 'CRITICAL' AND status = 'PENDING') as urgent_pending,
            AVG(EXTRACT(EPOCH FROM (updated_at - created_at))/3600) as avg_response_hours
        FROM pothole_report
        WHERE created_at >= NOW() - INTERVAL '30 days'
    """).fetchone()
    
    return jsonify({
        'reports_last_hour': stats[0],
        'active_repairs': stats[1],
        'urgent_pending': stats[2],
        'avg_response_hours': round(float(stats[3] or 0), 1),
        'system_status': 'OPERATIONAL',
        'last_updated': datetime.now().isoformat()
    })