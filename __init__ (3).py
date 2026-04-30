<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>FraudShield — Login</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background: #0a0e1a;
            color: #e8eaf0;
            font-family: 'Inter', sans-serif;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .card {
            background: #111827;
            border: 1px solid #1e2d45;
            border-radius: 16px;
            padding: 2.5rem;
            width: 380px;
        }
        .logo {
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.4rem;
            font-weight: 600;
            color: #00d4ff;
            margin-bottom: 0.25rem;
        }
        .logo span { color: #ff4757; }
        .tagline { color: #6b7a99; font-size: 0.8rem; margin-bottom: 2rem; }
        label { display: block; font-size: 0.8rem; color: #6b7a99; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 0.4rem; }
        input {
            width: 100%;
            background: #0a0e1a;
            border: 1px solid #1e2d45;
            border-radius: 8px;
            padding: 0.75rem 1rem;
            color: #e8eaf0;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.9rem;
            margin-bottom: 1.25rem;
            outline: none;
            transition: border-color 0.2s;
        }
        input:focus { border-color: #00d4ff; }
        button {
            width: 100%;
            background: #00d4ff;
            color: #0a0e1a;
            border: none;
            border-radius: 8px;
            padding: 0.85rem;
            font-weight: 700;
            font-size: 0.9rem;
            cursor: pointer;
            margin-top: 0.5rem;
        }
        .error { background: rgba(255,71,87,0.1); border: 1px solid rgba(255,71,87,0.3); border-radius: 8px; padding: 0.75rem; color: #ff4757; font-size: 0.85rem; margin-bottom: 1rem; }
    </style>
</head>
<body>
<div class="card">
    <div class="logo">Fraud<span>Shield</span></div>
    <div class="tagline">ML-Powered Credit Card Fraud Detection</div>
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% for cat, msg in messages %}<div class="error">{{ msg }}</div>{% endfor %}
    {% endwith %}
    <form method="POST">
        <label>Username</label>
        <input type="text" name="username" required autofocus>
        <label>Password</label>
        <input type="password" name="password" required>
        <button type="submit">Sign In</button>
    </form>
</div>
</body>
</html>
