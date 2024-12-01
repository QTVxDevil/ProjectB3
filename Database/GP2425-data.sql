use `gp2425`;

-- ---------------------------------------- image_storage ------------------------------------

INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13387', '001.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/quyet/001.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13387', '002.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/quyet/002.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13387', '003.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/quyet/003.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13387', '004.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/quyet/004.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13387', '005.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/quyet/005.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13387', '006.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/quyet/006.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13387', '007.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/quyet/007.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13387', '008.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/quyet/008.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13387', '009.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/quyet/009.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13387', '0010.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/quyet/0010.jpg'));
INSERT INTO `image_storage`(`student_id`, `image_name`, `image_data`) VALUES ('22BI13387', '0011.jpg', LOAD_FILE('D:/USTH_SUBJECTS/B3/GroupProject/Database/quyet/0011.jpg'));

-- ---------------------------------------student_details ---------------------------------------------------

INSERT INTO `student_details` (`student_id`, `student_name`, `birthday`, `birthplace`, `household_registration`, `citizen_identification`, `telephone`, `email`, `major`, `training_system`, `class`, `course`)
VALUES 
('22BI13387', 'TRỊNH VĂN QUYẾT', '2004-02-13', 'Hải Phòng', 'Hòa Bình, Vinh Quang, Tiên Lãng, Hải Phòng', '123456789012', '1234567890', 'QuyetTV.22BI13387@usth.edu.vn', 'DS', 'University', 'DS BI13', '2022-2025'),
('22BI13049', 'ĐÀO XUÂN BÁCH', '2004-01-01', 'Hải Phòng', 'Hòa Bình, Vinh Quang, Tiên Lãng, Hải Phòng', '012345678910', '1234567890', 'BachDX.22BI13049@usth.edu.vn', 'DS', 'University', 'DS BI13', '2022-2025');
















