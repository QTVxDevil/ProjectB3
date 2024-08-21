CREATE DATABASE IF NOT EXISTS `user_auth`;

USE `user_auth`;

CREATE TABLE IF NOT EXISTS `users` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `email` VARCHAR(255) NOT NULL UNIQUE,
    `password` VARCHAR(255) NOT NULL,
    `role` VARCHAR(50) NOT NULL
);

TRUNCATE TABLE `users`;

INSERT INTO `users` (`email`, `password`, `role`) VALUES
('lecturer-1@usth.edu.vn', '123456789', 'Lecturer'),
('lecturer-2@usth.edu.vn', '123456789', 'Lecturer'),
('student.xxBx1xxxx@usth.edu.vn', '123456789', 'Student')
ON DUPLICATE KEY UPDATE
 `password` = VALUES(`password`),
 `role` = VALUES(`role`);
 
ALTER TABLE `users`
DROP COLUMN `nameoflecturer`; 
 
ALTER TABLE `users`
ADD COLUMN `nameoflecturer` VARCHAR(50);

SET SQL_SAFE_UPDATES = 0;

UPDATE `users`
SET `nameoflecturer` = SUBSTRING_INDEX(`email`, '@', 1)
WHERE role = 'Lecturer';

select * from `users`;