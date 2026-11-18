

-- 用户表
CREATE TABLE users (
    id            INT          AUTO_INCREMENT,
    username      VARCHAR(64)  NOT NULL,
    display_name  VARCHAR(64),  -- 显示名称
    email         VARCHAR(254) NOT NULL,
    created_at    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_login_at DATETIME,
    PRIMARY KEY (id),
    UNIQUE KEY uq_username (username),
    UNIQUE KEY uq_email (email)
);


INSERT INTO users (username, display_name, email) VALUES
    ('alice', '爱丽丝', 'alice@example.com'),
    ('bob',   '鲍勃',   'bob@example.com'),
    ('carol', '卡罗尔', 'carol@example.com');


