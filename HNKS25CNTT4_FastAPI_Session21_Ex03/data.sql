create database auth_db;
use auth_db;

INSERT INTO users (email, password_hash, full_name, role, is_active)
VALUES
('student01@gmail.com', '$2b$12$78MhSneqt.erygwYFVpXHOOaSgqi9iub/Bdnx9Y00FFhF6UXEtZvG', 'Nguyễn Văn An', 'student', 1),
('student02@gmail.com', '$2b$12$78MhSneqt.erygwYFVpXHOOaSgqi9iub/Bdnx9Y00FFhF6UXEtZvG', 'Trần Thị Bình', 'student', 1),
('admin@gmail.com', '$2b$12$78MhSneqt.erygwYFVpXHOOaSgqi9iub/Bdnx9Y00FFhF6UXEtZvG', 'Admin', 'admin', 1),
('student03@gmail.com', '$2b$12$78MhSneqt.erygwYFVpXHOOaSgqi9iub/Bdnx9Y00FFhF6UXEtZvG', 'Messi', 'student', 0);