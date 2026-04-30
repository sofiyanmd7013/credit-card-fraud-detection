"""Dashboard routes."""
from flask import Blueprint, render_template
from flask_login import login_required
from sqlalchemy import func
from app.models import Transaction, FraudAlert, db

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@login_required
def index():
    total = Transaction.query.count()
    fraud = Transaction.query.filter_by(is_fraud_predicted=True).count()
    pending = Transaction.query.filter_by(status='pending').count()
    alerts = FraudAlert.query.filter_by(is_resolved=False).count()

    recent_fraud = Transaction.query.filter_by(
        is_fraud_predicted=True
    ).order_by(Transaction.created_at.desc()).limit(10).all()

    # Risk breakdown
    risk_counts = db.session.query(
        Transaction.risk_level, func.count(Transaction.id)
    ).group_by(Transaction.risk_level).all()

    return render_template('dashboard/index.html',
        total=total, fraud=fraud, pending=pending,
        alerts=alerts, recent_fraud=recent_fraud,
        risk_counts=dict(risk_counts)
    )
