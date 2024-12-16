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
INSERT INTO `student_infor`(`student_id`, `student_name`, `major`) VALUES('22BI13394', 'Hoang Trung Son', 'ICT');

-- ------------------------------- data for student_information_details ------------------------

INSERT INTO `student_infor_details` (`student_id`, `birthday`, `birthplace`, `household_registration`, `citizen_identification`, `telephone`, `email`, `training_system`, `class`, `course`)
VALUES 
('22BI13387', '2004-02-13', 'Hai Phong', 'Hoa Binh, Vinh Quang, Tien Lang, Hai Phong', '123456789012', '1234567890', 'QuyetTV.22BI13387@usth.edu.vn', 'University', 'DS BI13', '2022-2025'),
('22BI13280', '2004-07-19', 'Ha Noi', 'Cau Giay, Ha Noi', '0123414827121', '1234567893', 'MinhDD.22BI13280@usth.edu.vn', 'University', 'DS BI13', '2022-2025'),
('22BI13049', '2004-01-01', 'Thanh Hoa', 'Thai Ha, Dong Da, Ha Noi', '012345678910', '1234567890', 'BachDX.22BI13049@usth.edu.vn', 'University', 'DS BI13', '2022-2025'),
('22BI13394', '2004-01-26', 'Thanh Hoa', 'Phu Dien, Bac Tu Liem, Ha Noi', '012335678910', '1233567890', 'SonHT.22BI13394@usth.edu.vn', 'University', 'ICT BI13', '2022-2025'),
('22BI13375', '2004-02-02', 'Ha Noi', 'Hai Ba Trung, Ha Noi', '1123414827121', '2234567893', 'QuanNTM.22BI13375@usth.edu.vn', 'University', 'DS BI13', '2022-2025');

-- ------------------------------ data for image_storage -------------------------------------

INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13387', '001.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/001.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13387', '002.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/002.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13387', '003.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/003.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13387', '004.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/004.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13387', '005.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/005.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13387', '006.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/006.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13387', '007.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/007.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13387', '008.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/008.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13387', '009.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/009.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13387', '0010.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/0010.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13387', '0011.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/0011.jpg'));

INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13394', '01000.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/01000.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13394', '01001.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/01001.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13394', '01002.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/01002.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13394', '01003.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/01003.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13394', '01004.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/01004.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13394', '01005.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/01005.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13394', '01006.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/01006.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13394', '01007.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/01007.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13394', '01008.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/01008.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13394', '01009.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/01009.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13394', '010010.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/010010.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13394', '010011.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/010011.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13394', '010012.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/010012.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13394', '010013.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/010013.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13394', '010014.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/010014.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13394', '010015.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/Data/010015.jpg'));


