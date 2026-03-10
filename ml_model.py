import numpy as np
from datetime import datetime

class AccidentRiskPredictor:
    def predict_risk(self, report_data, all_reports):
        severity_score = {'LOW': 1, 'MEDIUM': 2, 'HIGH': 3, 'CRITICAL': 4}[report_data['severity']]
        
        # Count nearby reports within 1km
        nearby_count = sum(1 for r in all_reports 
                          if self._distance(report_data, r) <= 1.0 and r['report_id'] != report_data['report_id'])
        
        # Days since report
        days_open = (datetime.now() - datetime.strptime(report_data['created_at'], '%Y-%m-%d %H:%M')).days
        
        # Calculate risk
        risk_score = (severity_score * 0.4) + (min(nearby_count, 10) * 0.4) + (min(days_open, 30) * 0.2)
        
        if risk_score >= 8: level = 'Critical'
        elif risk_score >= 6: level = 'High'  
        elif risk_score >= 3: level = 'Medium'
        else: level = 'Low'
        
        accident_prob = min(severity_score * 15 + nearby_count * 5 + days_open * 2, 95)
        
        return {
            'risk_level': level,
            'accident_probability': accident_prob,
            'recommendations': self._get_recommendations(level)
        }
    
    def _distance(self, r1, r2):
        lat1, lon1 = r1['latitude'], r1['longitude']
        lat2, lon2 = r2['latitude'], r2['longitude']
        return ((lat1-lat2)**2 + (lon1-lon2)**2)**0.5 * 111  # Rough km conversion
    
    def _get_recommendations(self, level):
        recs = {
            'Critical': ['URGENT: Immediate repair', 'Deploy barriers'],
            'High': ['Repair within 48 hours', 'Install warning signs'],
            'Medium': ['Schedule repair within 1 week'],
            'Low': ['Routine maintenance']
        }
        return recs[level]