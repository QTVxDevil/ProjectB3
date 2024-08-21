CREATE DATABASE IF NOT EXISTS `information`;

USE `information`;

CREATE TABLE IF NOT EXISTS `classroom` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `nameofclass` VARCHAR(100) NOT NULL,
    `major` VARCHAR(10) NOT NULL,
    `begindate` DATE NOT NULL,
    `enddate` DATE NOT NULL,
    `nameoflecturer` VARCHAR(100) NOT NULL
);

TRUNCATE TABLE `classroom`;

INSERT INTO `classroom` (`nameofclass`, `major`, `begindate`, `enddate`, `nameoflecturer`) VALUES
('Introduction to deep learning', 'DS', '2024-08-28', '2024-10-04', 'lecturer-1'),
 ('Introduction to deep learning', 'ICT', '2024-08-28', '2024-10-04', 'lecturer-2');

select * from `classroom`;

