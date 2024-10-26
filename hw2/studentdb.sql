CREATE TABLE `students` (
    `id` INT AUTO_INCREMENT,
    `student_id` INT UNIQUE,
    `name` VARCHAR(50),
    `gender` ENUM('Male', 'Female', 'Other'),
    PRIMARY KEY (`id`)
);

CREATE TABLE `class` (
    `id` INT AUTO_INCREMENT,
    `class_id` VARCHAR(50),
    `student_id` INT,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`student_id`) REFERENCES `students`(`student_id`) ON DELETE CASCADE
);

CREATE TABLE `subject` (
    `id` INT AUTO_INCREMENT,
    `fav_subject` VARCHAR(50),
    `student_id` INT,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`student_id`) REFERENCES `students`(`student_id`) ON DELETE CASCADE
);

-- Insert data into the `students` table
INSERT INTO `students` (`student_id`, `name`, `gender`) VALUES
(101, 'John Doe', 'Male'),
(102, 'Jane Smith', 'Female'),
(103, 'Alex Johnson', 'Other'),
(104, 'Emily Davis', 'Female'),
(105, 'Michael Brown', 'Male');

-- Insert data into the `class` table with `student_id` references
INSERT INTO `class` (`class_id`, `student_id`) VALUES
('A', 101),
('B', 102),
('C', 103),
('C', 104),
('D', 105);

-- Insert data into the `subject` table with `student_id` references
INSERT INTO `subject` (`fav_subject`, `student_id`) VALUES
('Mathematics', 101),
('Science', 102),
('History', 103),
('Art', 104),
('Physical Education', 105);