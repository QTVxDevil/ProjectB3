USE `GP24-25`;

-- --------------------------- lecturer account ----------------------------------------
INSERT INTO `user_auth`(`account`, `password`, `role`, `nameoflecturer`)
VALUES
('lecturer-1@usth.edu.vn', '123456789', 'Lecturer', 'lecturer-1'),
('lecturer-2@usth.edu.vn', '123456789', 'Lecturer', 'lecturer-2');


-- ------------------------------- data for student_information -------------------------

INSERT INTO `student_infor`(`student_id`, `student_name`, `major`) VALUES('22BI13387', 'Trinh Van Quyet', 'DS');
INSERT INTO `student_infor`(`student_id`, `student_name`, `major`) VALUES('22BI13280', 'Do Duy Minh', 'DS');
INSERT INTO `student_infor`(`student_id`, `student_name`, `major`) VALUES('22BI13049', 'Dao Xuan Bach', 'DS');
INSERT INTO `student_infor`(`student_id`, `student_name`, `major`) VALUES('22BI13375', 'Nguyen Tran Minh Quan', 'DS');

-- ------------------------------- data for student_information_details ------------------------

INSERT INTO `student_infor_details` (`student_id`, `birthday`, `birthplace`, `household_registration`, `citizen_identification`, `telephone`, `email`, `training_system`, `class`, `course`)
VALUES 
('22BI13387', '2004-02-13', 'Hai Phong', 'Hoa Binh, Vinh Quang, Tien Lang, Hai Phong', '123456789012', '1234567890', 'QuyetTV.22BI13387@usth.edu.vn', 'University', 'DS BI13', '2022-2025'),
('22BI13280', '2004-07-19', 'Ha Noi', 'Cau Giay, Ha Noi', '0123414827121', '1234567893', 'MinhDD.22BI13280@usth.edu.vn', 'University', 'DS BI13', '2022-2025'),
('22BI13049', '2004-01-01', 'Thanh Hoa', 'Thai Ha, Dong Da, Ha Noi', '012345678910', '1234567890', 'BachDX.22BI13049@usth.edu.vn', 'University', 'DS BI13', '2022-2025'),
('22BI13375', '2004-02-02', 'Ha Noi', 'Hai Ba Trung, Ha Noi', '1123414827121', '2234567893', 'QuanNTM.22BI13375@usth.edu.vn', 'University', 'DS BI13', '2022-2025');
