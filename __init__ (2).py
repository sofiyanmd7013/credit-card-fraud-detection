from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256))
    role = db.Column(db.String(20), default='analyst')  # admin, analyst, viewer
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    transactions = db.relationship('Transaction', backref='reviewer', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(64), unique=True, nullable=False, index=True)
    amount = db.Column(db.Float, nullable=False)
    merchant = db.Column(db.String(128))
    merchant_category = db.Column(db.String(64))
    card_number_masked = db.Column(db.String(20))
    customer_id = db.Column(db.String(64), index=True)
    transaction_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Location
    country = db.Column(db.String(64))
    city = db.Column(db.String(64))
    
    # ML features (V1-V28 from PCA-transformed features, as in real datasets)
    v1  = db.Column(db.Float); v2  = db.Column(db.Float); v3  = db.Column(db.Float)
    v4  = db.Column(db.Float); v5  = db.Column(db.Float); v6  = db.Column(db.Float)
    v7  = db.Column(db.Float); v8  = db.Column(db.Float); v9  = db.Column(db.Float)
    v10 = db.Column(db.Float); v11 = db.Column(db.Float); v12 = db.Column(db.Float)
    v13 = db.Column(db.Float); v14 = db.Column(db.Float); v15 = db.Column(db.Float)
    v16 = db.Column(db.Float); v17 = db.Column(db.Float); v18 = db.Column(db.Float)
    v19 = db.Column(db.Float); v20 = db.Column(db.Float); v21 = db.Column(db.Float)
    v22 = db.Column(db.Float); v23 = db.Column(db.Float); v24 = db.Column(db.Float)
    v25 = db.Column(db.Float); v26 = db.Column(db.Float); v27 = db.Column(db.Float)
    v28 = db.Column(db.Float)

    # Detection results
    ml_fraud_score = db.Column(db.Float, default=0.0)
    rule_fraud_flags = db.Column(db.JSON, default=list)
    final_fraud_score = db.Column(db.Float, default=0.0)
    is_fraud_predicted = db.Column(db.Boolean, default=False)
    is_fraud_actual = db.Column(db.Boolean)  # Ground truth (if known)
    
    # Status
    status = db.Column(db.String(20), default='pending')  # pending, approved, flagged, blocked
    risk_level = db.Column(db.String(10), default='low')  # low, medium, high, critical
    
    # Review
    reviewed_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    reviewed_at = db.Column(db.DateTime)
    review_notes = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_feature_vector(self):
        return [self.amount, self.v1, self.v2, self.v3, self.v4, self.v5,
                self.v6, self.v7, self.v8, self.v9, self.v10, self.v11,
                self.v12, self.v13, self.v14, self.v15, self.v16, self.v17,
                self.v18, self.v19, self.v20, self.v21, self.v22, self.v23,
                self.v24, self.v25, self.v26, self.v27, self.v28]

    def to_dict(self):
        return {
            'id': self.id,
            'transaction_id': self.transaction_id,
            'amount': self.amount,
            'merchant': self.merchant,
            'merchant_category': self.merchant_category,
            'customer_id': self.customer_id,
            'transaction_time': self.transaction_time.isoformat(),
            'country': self.country,
            'city': self.city,
            'ml_fraud_score': self.ml_fraud_score,
            'rule_fraud_flags': self.rule_fraud_flags,
            'final_fraud_score': self.final_fraud_score,
            'is_fraud_predicted': self.is_fraud_predicted,
            'is_fraud_actual': self.is_fraud_actual,
            'status': self.status,
            'risk_level': self.risk_level,
            'created_at': self.created_at.isoformat()
        }

    def __repr__(self):
        return f'<Transaction {self.transaction_id}>'


class FraudAlert(db.Model):
    __tablename__ = 'fraud_alerts'

    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id'), nullable=False)
    alert_type = db.Column(db.String(64))  # ml_detected, rule_triggered, manual
    severity = db.Column(db.String(10))    # low, medium, high, critical
    message = db.Column(db.Text)
    is_resolved = db.Column(db.Boolean, default=False)
    resolved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    resolved_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    transaction = db.relationship('Transaction', backref='alerts')

    def __repr__(self):
        return f'<FraudAlert {self.id} - {self.severity}>'


class ModelMetrics(db.Model):
    __tablename__ = 'model_metrics'

    id = db.Column(db.Integer, primary_key=True)
    model_version = db.Column(db.String(32))
    precision = db.Column(db.Float)
    recall = db.Column(db.Float)
    f1_score = db.Column(db.Float)
    auc_roc = db.Column(db.Float)
    accuracy = db.Column(db.Float)
    training_samples = db.Column(db.Integer)
    fraud_samples = db.Column(db.Integer)
    legitimate_samples = db.Column(db.Integer)
    trained_at = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)

    def __repr__(self):
        return f'<ModelMetrics v{self.model_version}>'
