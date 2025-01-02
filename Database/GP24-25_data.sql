USE `GP2425`;

-- --------------------------- lecturer account ----------------------------------------
INSERT INTO `user_auth`(`account`, `password`, `role`, `nameoflecturer`)
VALUES
('lecturer-1@usth.edu.vn', '123456789', 'Lecturer', 'lecturer-1'),
('lecturer-2@usth.edu.vn', '123456789', 'Lecturer', 'lecturer-2'),
('lecturer-3@usth.edu.vn', '123456789', 'Lecturer', 'lecturer-3');


-- ------------------------------- data for student_information -------------------------

INSERT INTO `student_infor`(`student_id`, `student_name`, `major`) VALUES('22BI13280', 'Do Duy Minh', 'DS');
INSERT INTO `student_infor`(`student_id`, `student_name`, `major`) VALUES('22BI13049', 'Dao Xuan Bach', 'DS');
INSERT INTO `student_infor`(`student_id`, `student_name`, `major`) VALUES('22BI13387', 'Trinh Van Quyet', 'DS');
INSERT INTO `student_infor`(`student_id`, `student_name`, `major`) VALUES('22BI13375', 'Nguyen Tran Minh Quan', 'DS');
INSERT INTO `student_infor`(`student_id`, `student_name`, `major`) VALUES('22BI13256', 'Le Xuan Loc', 'DS');
INSERT INTO `student_infor`(`student_id`, `student_name`, `major`) VALUES('22BI13394', 'Hoang Trung Son', 'ICT');
INSERT INTO `student_infor`(`student_id`, `student_name`, `major`) VALUES('22BI13067', 'Nguyen Tien Cong', 'DS');

-- ------------------------------- data for student_information_details ------------------------

INSERT INTO `student_infor_details` (`student_id`, `birthday`, `birthplace`, `household_registration`, `citizen_identification`, `telephone`, `email`, `training_system`, `class`, `course`)
VALUES 
('22BI13280', '2004-07-19', 'Ha Noi', 'Cau Giay, Ha Noi', '0123414827121', '1234567893', 'MinhDD.22BI13280@usth.edu.vn', 'University', 'DS BI13', '2022-2025'),
('22BI13049', '2004-01-01', 'Thanh Hoa', 'Thai Ha, Dong Da, Ha Noi', '012345678910', '1234567890', 'BachDX.22BI13049@usth.edu.vn', 'University', 'DS BI13', '2022-2025'),
('22BI13394', '2004-01-26', 'Thanh Hoa', 'Phu Dien, Bac Tu Liem, Ha Noi', '012335678910', '1233567890', 'SonHT.22BI13394@usth.edu.vn', 'University', 'ICT BI13', '2022-2025'),
('22BI13256', '2004-11-26', 'Ha Noi', 'To Hieu, Cau Giay, Ha Noi', '112435678910', '0233567890', 'LocLX.22BI13256@usth.edu.vn', 'University', 'DS BI13', '2022-2025'),
('22BI13067', '2004-11-10', 'Ha Noi', 'Nhan Chinh, Thanh Xuan, Ha Noi', '112435878910', '0233567890', 'CongNT.22BI13067@usth.edu.vn', 'University', 'DS BI13', '2022-2025'),
('22BI13387', '2004-02-13', 'Hai Phong', 'Hoa Binh, Vinh Quang, Tien Lang, Hai Phong', '123456789012', '1234567890', 'QuyetTV.22BI13387@usth.edu.vn', 'University', 'DS BI13', '2022-2025'),
('22BI13375', '2004-02-02', 'Ha Noi', 'Hai Ba Trung, Ha Noi', '1123414827121', '2234567893', 'QuanNTM.22BI13375@usth.edu.vn', 'University', 'DS BI13', '2022-2025');

-- ------------------------------ data for image_storage -------------------------------------

INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13387', '387-1.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/387-1.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13387', '387-2.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/387-2.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13387', '387-3.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/387-3.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13387', '387-4.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/387-4.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13387', '387-5.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/387-5.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13387', '387-6.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/387-6.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13387', '387-7.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/387-7.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13387', '387-8.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/387-8.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13387', '387-9.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/387-9.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13387', '387-10.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/387-10.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13387', '387-11.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/387-11.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13387', '387-12.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/387-12.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13387', '387-13.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/387-13.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13387', '387-14.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/387-14.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13387', '387-15.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/387-15.jpg'));

INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13256', '256-1.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/256-1.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13256', '256-2.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/256-2.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13256', '256-3.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/256-3.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13256', '256-4.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/256-4.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13256', '256-5.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/256-5.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13256', '256-6.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/256-6.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13256', '256-7.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/256-7.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13256', '256-8.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/256-8.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13256', '256-9.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/256-9.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13256', '256-10.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/256-10.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13256', '256-11.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/256-11.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13256', '256-12.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/256-12.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13256', '256-13.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/256-13.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13256', '256-14.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/256-14.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13256', '256-15.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/256-15.jpg'));

INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13067', '067-1.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/067-1.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13067', '067-2.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/067-2.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13067', '067-3.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/067-3.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13067', '067-4.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/067-4.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13067', '067-5.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/067-5.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13067', '067-6.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/067-6.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13067', '067-7.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/067-7.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13067', '067-8.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/067-8.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13067', '067-9.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/067-9.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13067', '067-10.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/067-10.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13067', '067-11.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/067-11.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13067', '067-12.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/067-12.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13067', '067-13.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/067-13.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13067', '067-14.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/067-14.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13067', '067-15.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/067-15.jpg'));

