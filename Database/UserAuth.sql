CREATE DATABASE IF NOT EXISTS `user_auth`;

USE `user_auth`;

CREATE TABLE IF NOT EXISTS `users` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `email` VARCHAR(255) NOT NULL UNIQUE,
    `password` VARCHAR(255) NOT NULL,
    `role` VARCHAR(50) NOT NULL
);

INSERT INTO `users` (`email`, `password`, `role`) VALUES
('lecturer@usth.edu.vn', 'password123', 'Lecturer'),
('student@usth.edu.vn', 'password123', 'Student'),
('admin@usth.edu.vn', 'password123', 'Admin')
ON DUPLICATE KEY UPDATE
 `password` = VALUES(`password`),
 `role` = VALUES(`role`);
