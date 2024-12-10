CREATE DATABASE IF NOT EXISTS `GP24-25`;

USE `GP24-25`;

-- ----------------------- student information ----------------------------------- 

CREATE TABLE IF NOT EXISTS `student_infor` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `student_id` VARCHAR(20) NOT NULL UNIQUE,
    `student_name` VARCHAR(100) NOT NULL,
    `major` VARCHAR(100) NOT NULL
);

-- ------------------------- student_infor_details --------------------------

CREATE TABLE IF NOT EXISTS `student_infor_details` (
    `student_id` VARCHAR(20) NOT NULL,
    `birthday` DATE NOT NULL,
    `birthplace` VARCHAR(100) NOT NULL,
    `household_registration` VARCHAR(100) NOT NULL,
    `citizen_identification` VARCHAR(20) NOT NULL,
    `telephone` VARCHAR(15) NOT NULL,
    `email` VARCHAR(100) NOT NULL,
    `training_system` VARCHAR(50) NOT NULL,
    `class` VARCHAR(50) NOT NULL,
    `course` VARCHAR(50) NOT NULL,
    PRIMARY KEY (`student_id`),
    FOREIGN KEY (`student_id`) REFERENCES `student_infor`(`student_id`) ON DELETE CASCADE
);

-- ------------------- user_auth ---------------------------------

CREATE TABLE IF NOT EXISTS `user_auth` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `account` VARCHAR(100) NOT NULL UNIQUE,
    `password` VARCHAR(255) NOT NULL DEFAULT '123456789',
    `role` ENUM('Lecturer', 'Student') NOT NULL DEFAULT 'Student',
    `nameoflecturer` VARCHAR(100),
    `student_id` VARCHAR(20),
    FOREIGN KEY (`student_id`) REFERENCES `student_infor_details`(`student_id`) ON DELETE CASCADE
);
-- Trigger to automatically create student account
DELIMITER //

CREATE TRIGGER auto_create_student_account
AFTER INSERT ON `student_infor_details`
FOR EACH ROW
BEGIN
    INSERT INTO `user_auth` (`account`, `password`, `role`, `student_id`)
    VALUES (NEW.email, '123456789', DEFAULT, NEW.student_id);
END;
//

DELIMITER ;

-- --------------------------- classroom ------------------------------

CREATE TABLE IF NOT EXISTS `course` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `nameofclass` VARCHAR(100) NOT NULL,
    `major` VARCHAR(100) NOT NULL,
    `begindate` DATE NOT NULL,
    `enddate` DATE NOT NULL,
    `nameoflecturer` VARCHAR(100) NOT NULL
);

-- --------------------------- student_class -----------------------------

CREATE TABLE IF NOT EXISTS `student_in_course` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `student_id` VARCHAR(20) NOT NULL,
    `course_id` INT NOT NULL,
    FOREIGN KEY (`student_id`) REFERENCES `student_infor_details`(`student_id`) ON DELETE CASCADE,
    FOREIGN KEY (`course_id`) REFERENCES `course`(`id`) ON DELETE CASCADE
);

-- --------------------------- attendance_checked ---------------------------

CREATE TABLE IF NOT EXISTS `attendance_checked` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `start_time`DATETIME NOT NULL,
    `place` VARCHAR(100) NOT NULL,
    `end_time` DATETIME NOT NULL,
    `course_id` INT NOT NULL,
    FOREIGN KEY (`course_id`) REFERENCES `course`(`id`) ON DELETE CASCADE
);

DELIMITER //

CREATE TRIGGER set_end_time
BEFORE INSERT ON `attendance_checked`
FOR EACH ROW
BEGIN
    SET NEW.end_time = DATE_ADD(NEW.start_time, INTERVAL 3 MINUTE);
END;
//

DELIMITER ;

-- ---------------------------- student_attendance ----------------------------

CREATE TABLE IF NOT EXISTS `student_attendance` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `student_id` VARCHAR(20) NOT NULL,
    `time_checking` TIME NOT NULL,
    `attendance_id` INT NOT NULL,
    FOREIGN KEY (`student_id`) REFERENCES `student_infor_details`(`student_id`) ON DELETE CASCADE,
    FOREIGN KEY (`attendance_id`) REFERENCES `attendance_checked`(`id`) ON DELETE CASCADE
);

-- ----------------------------- image_storage -----------------------------------

CREATE TABLE IF NOT EXISTS `image_storage` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `student_id` VARCHAR(20) NOT NULL,
    `image_name` VARCHAR(255) NOT NULL,
    `image_data` LONGBLOB NOT NULL,
    `upload_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`student_id`) REFERENCES `student_infor_details`(`student_id`) ON DELETE CASCADE
);