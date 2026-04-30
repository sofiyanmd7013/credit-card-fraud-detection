from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
from app.models import Transaction, db
from config import Config

transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status')
    risk = request.args.get('risk')

    query = Transaction.query
    if status:
        query = query.filter_by(status=status)
    if risk:
        query = query.filter_by(risk_level=risk)

    transactions = query.order_by(Transaction.created_at.desc()).paginate(
        page=page, per_page=Config.TRANSACTIONS_PER_PAGE
    )
    return render_template('transactions/index.html', transactions=transactions)


@transactions_bp.route('/<int:txn_id>')
@login_required
def detail(txn_id):
    txn = Transaction.query.get_or_404(txn_id)
    return render_template('transactions/detail.html', txn=txn)


@transactions_bp.route('/<int:txn_id>/review', methods=['POST'])
@login_required
def review(txn_id):
    txn = Transaction.query.get_or_404(txn_id)
    action = request.form.get('action')
    notes = request.form.get('notes', '')

    if action in ['approve', 'block']:
        txn.status = 'approved' if action == 'approve' else 'blocked'
        txn.reviewed_by = current_user.id
        txn.reviewed_at = datetime.utcnow()
        txn.review_notes = notes
        db.session.commit()
        flash(f'Transaction {action}d successfully.', 'success')
    
    return redirect(url_for('transactions.detail', txn_id=txn_id))
