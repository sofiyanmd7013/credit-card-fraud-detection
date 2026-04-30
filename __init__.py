-- Credit Card Fraud Detection System
-- MySQL Schema
-- Run: mysql -u root -p < schema.sql

CREATE DATABASE IF NOT EXISTS fraud_detection_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE fraud_detection_db;

CREATE TABLE IF NOT EXISTS users (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    username      VARCHAR(64)  NOT NULL UNIQUE,
    email         VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(256),
    role          VARCHAR(20)  DEFAULT 'analyst',
    is_active     BOOLEAN      DEFAULT TRUE,
    created_at    DATETIME     DEFAULT CURRENT_TIMESTAMP,
    last_login    DATETIME,
    INDEX idx_username (username),
    INDEX idx_email (email)
);

CREATE TABLE IF NOT EXISTS transactions (
    id                  INT AUTO_INCREMENT PRIMARY KEY,
    transaction_id      VARCHAR(64)  NOT NULL UNIQUE,
    amount              DOUBLE       NOT NULL,
    merchant            VARCHAR(128),
    merchant_category   VARCHAR(64),
    card_number_masked  VARCHAR(20),
    customer_id         VARCHAR(64),
    transaction_time    DATETIME     NOT NULL,
    country             VARCHAR(64),
    city                VARCHAR(64),
    -- PCA features V1-V28
    v1 DOUBLE, v2 DOUBLE, v3 DOUBLE, v4 DOUBLE, v5 DOUBLE, v6 DOUBLE,
    v7 DOUBLE, v8 DOUBLE, v9 DOUBLE, v10 DOUBLE, v11 DOUBLE, v12 DOUBLE,
    v13 DOUBLE, v14 DOUBLE, v15 DOUBLE, v16 DOUBLE, v17 DOUBLE, v18 DOUBLE,
    v19 DOUBLE, v20 DOUBLE, v21 DOUBLE, v22 DOUBLE, v23 DOUBLE, v24 DOUBLE,
    v25 DOUBLE, v26 DOUBLE, v27 DOUBLE, v28 DOUBLE,
    -- Detection
    ml_fraud_score      DOUBLE       DEFAULT 0.0,
    rule_fraud_flags    JSON,
    final_fraud_score   DOUBLE       DEFAULT 0.0,
    is_fraud_predicted  BOOLEAN      DEFAULT FALSE,
    is_fraud_actual     BOOLEAN,
    status              VARCHAR(20)  DEFAULT 'pending',
    risk_level          VARCHAR(10)  DEFAULT 'low',
    -- Review
    reviewed_by         INT,
    reviewed_at         DATETIME,
    review_notes        TEXT,
    created_at          DATETIME     DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (reviewed_by) REFERENCES users(id),
    INDEX idx_customer_id (customer_id),
    INDEX idx_transaction_id (transaction_id),
    INDEX idx_status (status),
    INDEX idx_risk_level (risk_level),
    INDEX idx_created_at (created_at)
);

CREATE TABLE IF NOT EXISTS fraud_alerts (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    transaction_id  INT          NOT NULL,
    alert_type      VARCHAR(64),
    severity        VARCHAR(10),
    message         TEXT,
    is_resolved     BOOLEAN      DEFAULT FALSE,
    resolved_by     INT,
    resolved_at     DATETIME,
    created_at      DATETIME     DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (transaction_id) REFERENCES transactions(id),
    FOREIGN KEY (resolved_by) REFERENCES users(id),
    INDEX idx_is_resolved (is_resolved),
    INDEX idx_severity (severity)
);

CREATE TABLE IF NOT EXISTS model_metrics (
    id                  INT AUTO_INCREMENT PRIMARY KEY,
    model_version       VARCHAR(32),
    precision_score     DOUBLE,
    recall_score        DOUBLE,
    f1_score            DOUBLE,
    auc_roc             DOUBLE,
    accuracy            DOUBLE,
    training_samples    INT,
    fraud_samples       INT,
    legitimate_samples  INT,
    trained_at          DATETIME DEFAULT CURRENT_TIMESTAMP,
    notes               TEXT
);

-- Seed default admin user (password: admin123)
INSERT IGNORE INTO users (username, email, password_hash, role)
VALUES (
    'admin',
    'admin@fraudshield.io',
    'scrypt:32768:8:1$placeholder$hash',
    'admin'
);
