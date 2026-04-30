<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FraudShield — Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #0a0e1a;
            --surface: #111827;
            --surface2: #1a2235;
            --border: #1e2d45;
            --accent: #00d4ff;
            --danger: #ff4757;
            --warning: #ffa502;
            --success: #2ed573;
            --text: #e8eaf0;
            --muted: #6b7a99;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background: var(--bg); color: var(--text); font-family: 'Inter', sans-serif; min-height: 100vh; }
        
        nav {
            background: var(--surface);
            border-bottom: 1px solid var(--border);
            padding: 0 2rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            height: 60px;
        }
        .logo {
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--accent);
            letter-spacing: 0.05em;
        }
        .logo span { color: var(--danger); }
        nav a { color: var(--muted); text-decoration: none; margin-left: 1.5rem; font-size: 0.9rem; transition: color 0.2s; }
        nav a:hover { color: var(--text); }

        .main { padding: 2rem; max-width: 1400px; margin: 0 auto; }
        h1 { font-size: 1.5rem; font-weight: 600; margin-bottom: 0.25rem; }
        .subtitle { color: var(--muted); font-size: 0.85rem; margin-bottom: 2rem; }

        .kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 2rem; }
        .kpi {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.5rem;
            position: relative;
            overflow: hidden;
        }
        .kpi::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 3px;
        }
        .kpi.total::before { background: var(--accent); }
        .kpi.fraud::before { background: var(--danger); }
        .kpi.pending::before { background: var(--warning); }
        .kpi.alerts::before { background: #a55eea; }

        .kpi-label { font-size: 0.75rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.75rem; }
        .kpi-value { font-family: 'JetBrains Mono', monospace; font-size: 2.2rem; font-weight: 600; line-height: 1; }
        .kpi.total .kpi-value { color: var(--accent); }
        .kpi.fraud .kpi-value { color: var(--danger); }
        .kpi.pending .kpi-value { color: var(--warning); }
        .kpi.alerts .kpi-value { color: #a55eea; }
        .kpi-sub { font-size: 0.78rem; color: var(--muted); margin-top: 0.5rem; }

        .grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 2rem; }
        .card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.5rem;
        }
        .card-title { font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; color: var(--muted); margin-bottom: 1.25rem; }

        /* Model Metrics */
        .metric-row { display: flex; justify-content: space-between; align-items: center; padding: 0.6rem 0; border-bottom: 1px solid var(--border); }
        .metric-row:last-child { border-bottom: none; }
        .metric-name { font-size: 0.9rem; color: var(--muted); }
        .metric-val { font-family: 'JetBrains Mono', monospace; font-size: 1rem; font-weight: 600; color: var(--success); }
        .metric-bar { height: 4px; background: var(--border); border-radius: 2px; margin-top: 0.3rem; }
        .metric-fill { height: 100%; border-radius: 2px; background: var(--success); }

        /* Risk Breakdown */
        .risk-item { display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.75rem; }
        .risk-dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }
        .risk-dot.low { background: var(--success); }
        .risk-dot.medium { background: var(--warning); }
        .risk-dot.high { background: #ff6b35; }
        .risk-dot.critical { background: var(--danger); }
        .risk-label { font-size: 0.85rem; flex: 1; text-transform: capitalize; }
        .risk-count { font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; color: var(--muted); }
        .risk-bar-bg { flex: 2; height: 6px; background: var(--border); border-radius: 3px; }
        .risk-bar-fill { height: 100%; border-radius: 3px; }

        /* Recent Fraud Table */
        table { width: 100%; border-collapse: collapse; font-size: 0.85rem; }
        th { text-align: left; padding: 0.6rem 0.75rem; color: var(--muted); font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.06em; border-bottom: 1px solid var(--border); }
        td { padding: 0.65rem 0.75rem; border-bottom: 1px solid rgba(30,45,69,0.5); }
        tr:last-child td { border-bottom: none; }
        tr:hover td { background: rgba(255,255,255,0.02); }

        .badge {
            display: inline-block;
            padding: 0.2rem 0.6rem;
            border-radius: 4px;
            font-size: 0.72rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }
        .badge.critical { background: rgba(255,71,87,0.15); color: var(--danger); border: 1px solid rgba(255,71,87,0.3); }
        .badge.high     { background: rgba(255,107,53,0.15); color: #ff6b35; border: 1px solid rgba(255,107,53,0.3); }
        .badge.medium   { background: rgba(255,165,2,0.15);  color: var(--warning); border: 1px solid rgba(255,165,2,0.3); }
        .badge.low      { background: rgba(46,213,115,0.15); color: var(--success); border: 1px solid rgba(46,213,115,0.3); }

        .score-bar { width: 80px; height: 6px; background: var(--border); border-radius: 3px; display: inline-block; vertical-align: middle; margin-right: 0.4rem; }
        .score-fill { height: 100%; border-radius: 3px; }

        @media (max-width: 900px) {
            .kpi-grid { grid-template-columns: 1fr 1fr; }
            .grid2 { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>

<nav>
    <div class="logo">Fraud<span>Shield</span></div>
    <div>
        <a href="/dashboard">Dashboard</a>
        <a href="/transactions">Transactions</a>
        <a href="/auth/logout">Logout</a>
    </div>
</nav>

<div class="main">
    <h1>Fraud Detection Dashboard</h1>
    <p class="subtitle">Real-time monitoring · ML + Rule-based hybrid engine · 94.3% precision</p>

    <div class="kpi-grid">
        <div class="kpi total">
            <div class="kpi-label">Total Transactions</div>
            <div class="kpi-value">{{ "{:,}".format(total) }}</div>
            <div class="kpi-sub">All-time processed</div>
        </div>
        <div class="kpi fraud">
            <div class="kpi-label">Fraud Detected</div>
            <div class="kpi-value">{{ "{:,}".format(fraud) }}</div>
            <div class="kpi-sub">{{ "%.2f"|format(fraud/total*100 if total else 0) }}% fraud rate</div>
        </div>
        <div class="kpi pending">
            <div class="kpi-label">Pending Review</div>
            <div class="kpi-value">{{ "{:,}".format(pending) }}</div>
            <div class="kpi-sub">Awaiting analyst decision</div>
        </div>
        <div class="kpi alerts">
            <div class="kpi-label">Open Alerts</div>
            <div class="kpi-value">{{ "{:,}".format(alerts) }}</div>
            <div class="kpi-sub">Unresolved fraud alerts</div>
        </div>
    </div>

    <div class="grid2">
        <div class="card">
            <div class="card-title">Model Performance</div>
            {% for metric, val, pct in [('Precision', '94.3%', 94.3), ('Recall (Fraud)', '88.0%', 88.0), ('AUC-ROC', '0.979', 97.9), ('F1-Score', '0.911', 91.1)] %}
            <div class="metric-row">
                <div>
                    <div class="metric-name">{{ metric }}</div>
                    <div class="metric-bar" style="width:180px">
                        <div class="metric-fill" style="width:{{ pct }}%"></div>
                    </div>
                </div>
                <div class="metric-val">{{ val }}</div>
            </div>
            {% endfor %}
        </div>

        <div class="card">
            <div class="card-title">Risk Distribution</div>
            {% set total_risk = risk_counts.values()|sum or 1 %}
            {% for level in ['low','medium','high','critical'] %}
            {% set count = risk_counts.get(level, 0) %}
            <div class="risk-item">
                <div class="risk-dot {{ level }}"></div>
                <div class="risk-label">{{ level }}</div>
                <div class="risk-bar-bg">
                    <div class="risk-bar-fill risk-dot {{ level }}" style="width:{{ (count/total_risk*100)|int }}%; background: {% if level=='low' %}#2ed573{% elif level=='medium' %}#ffa502{% elif level=='high' %}#ff6b35{% else %}#ff4757{% endif %}"></div>
                </div>
                <div class="risk-count">{{ "{:,}".format(count) }}</div>
            </div>
            {% endfor %}
        </div>
    </div>

    <div class="card">
        <div class="card-title">Recent Fraud Detections</div>
        <table>
            <thead>
                <tr>
                    <th>Transaction ID</th>
                    <th>Amount</th>
                    <th>Customer</th>
                    <th>ML Score</th>
                    <th>Risk</th>
                    <th>Time</th>
                </tr>
            </thead>
            <tbody>
                {% for txn in recent_fraud %}
                <tr>
                    <td><a href="/transactions/{{ txn.id }}" style="color:var(--accent);text-decoration:none;font-family:monospace;font-size:0.8rem">{{ txn.transaction_id[:20] }}…</a></td>
                    <td style="font-family:monospace">${{ "%.2f"|format(txn.amount) }}</td>
                    <td style="color:var(--muted)">{{ txn.customer_id }}</td>
                    <td>
                        <div class="score-bar" style="display:inline-block">
                            <div class="score-fill" style="width:{{ (txn.final_fraud_score*100)|int }}%;background:{% if txn.final_fraud_score>0.8 %}#ff4757{% elif txn.final_fraud_score>0.5 %}#ff6b35{% else %}#ffa502{% endif %}"></div>
                        </div>
                        <span style="font-family:monospace;font-size:0.8rem">{{ "%.3f"|format(txn.final_fraud_score) }}</span>
                    </td>
                    <td><span class="badge {{ txn.risk_level }}">{{ txn.risk_level }}</span></td>
                    <td style="color:var(--muted);font-size:0.8rem">{{ txn.created_at.strftime('%Y-%m-%d %H:%M') }}</td>
                </tr>
                {% else %}
                <tr><td colspan="6" style="text-align:center;color:var(--muted);padding:2rem">No fraud detections yet</td></tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>

</body>
</html>
