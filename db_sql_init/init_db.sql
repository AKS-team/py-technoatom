CREATE DATABASE task_tracker_db CHARACTER SET UTF8;
CREATE USER tracker_admin@localhost IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON task_tracker_db.* TO tracker_admin@localhost;
FLUSH PRIVILEGES;
