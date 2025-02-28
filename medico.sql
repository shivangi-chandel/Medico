-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 24, 2025 at 09:27 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `medico`
--

-- --------------------------------------------------------

--
-- Table structure for table `admins`
--

CREATE TABLE `admins` (
  `admin_id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `registration_date` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admins`
--

INSERT INTO `admins` (`admin_id`, `username`, `password`, `registration_date`) VALUES
(1, 'shivangi', 'shivangi', '2025-02-22 22:42:52');

-- --------------------------------------------------------

--
-- Table structure for table `appointments`
--

CREATE TABLE `appointments` (
  `appointment_id` int(11) NOT NULL,
  `patient_id` int(11) NOT NULL,
  `doctor_id` int(11) NOT NULL,
  `appointment_date` datetime NOT NULL,
  `status` enum('Scheduled','Completed','Cancelled') DEFAULT 'Scheduled'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `bookings`
--

CREATE TABLE `bookings` (
  `id` int(11) NOT NULL,
  `doctor_id` int(11) NOT NULL,
  `patient_id` int(11) NOT NULL,
  `date` date NOT NULL,
  `time` varchar(20) NOT NULL,
  `room_name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `bookings`
--

INSERT INTO `bookings` (`id`, `doctor_id`, `patient_id`, `date`, `time`, `room_name`) VALUES
(1, 1, 6, '2025-02-13', '02:00 PM', 'MedicoRoom-5bbc154b'),
(7, 12, 6, '0000-00-00', '02:00 PM', 'MedicoRoom-6459ee7b'),
(8, 12, 6, '2025-02-28', '05:00 PM', 'MedicoRoom-a02982ba'),
(9, 12, 6, '2025-02-28', '06:00 PM', 'MedicoRoom-c3226450'),
(10, 12, 6, '2025-03-29', '07:00 PM', 'MedicoRoom-c929c5e5'),
(11, 12, 10, '2025-02-28', '05:00 PM', 'MedicoRoom-946dad89'),
(12, 12, 10, '2025-02-28', '07:00 PM', 'MedicoRoom-2927114e');

-- --------------------------------------------------------

--
-- Table structure for table `categories`
--

CREATE TABLE `categories` (
  `category_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `price` int(255) NOT NULL,
  `icon_url` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `categories`
--

INSERT INTO `categories` (`category_id`, `name`, `description`, `price`, `icon_url`, `created_at`) VALUES
(2, 'General Physician', 'cold cough all general', 499, '/static/uploads\\categories\\general-physician.png', '2025-01-28 12:27:10'),
(3, 'Gynecology', '', 499, '/static/uploads\\categories\\gyno.png', '2025-01-28 12:28:34'),
(4, 'Cardiology', '', 499, '/static/uploads\\categories\\cardio.png', '2025-01-28 12:29:08'),
(5, 'Gastroenterology', '', 499, '/static/uploads\\categories\\gastro.png', '2025-01-28 12:29:47'),
(6, 'Psychiatry', '', 599, '/static/uploads\\categories\\psychiatry.png', '2025-01-28 12:33:05'),
(7, 'Endocrinology', '', 499, '/static/uploads\\categories\\endocrinology.png', '2025-01-28 12:33:38'),
(8, 'ENT', 'Ear, Nose, and Throat', 299, '/static/uploads\\categories\\ent.png', '2025-01-28 12:34:18');

-- --------------------------------------------------------

--
-- Table structure for table `department`
--

CREATE TABLE `department` (
  `id` int(11) NOT NULL,
  `department_id` varchar(100) NOT NULL,
  `department_name` varchar(100) NOT NULL,
  `department_title` varchar(255) DEFAULT NULL,
  `picture` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `department`
--

INSERT INTO `department` (`id`, `department_id`, `department_name`, `department_title`, `picture`) VALUES
(1, '111', 'Emergency Department', 'Emergency department', 'static/uploads\\department_icon_1 (1).svg'),
(3, '112', 'Pediatric Department', 'kids Department', 'static/uploads\\department_icon_2.svg'),
(4, '113', 'Cardiology Department', 'Cardiology Department', 'static/uploads\\department_icon_4.svg'),
(5, '114', 'Neurology Department', 'Neurology Department', 'static/uploads\\department_icon_5.svg'),
(6, '115', 'Psychiatry Department', 'Psychiatry Department', 'static/uploads\\department_icon_6.svg'),
(7, '116', 'Gynecology Department', 'Gynecology Department', 'static/uploads\\department_icon_3.svg');

-- --------------------------------------------------------

--
-- Table structure for table `doctors`
--

CREATE TABLE `doctors` (
  `doctor_id` int(11) NOT NULL,
  `full_name` varchar(255) NOT NULL,
  `specialization` varchar(255) DEFAULT NULL,
  `contact_number` varchar(15) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `profile_picture` varchar(255) DEFAULT NULL,
  `account_id` varchar(255) NOT NULL,
  `experience` int(255) NOT NULL,
  `registration_date` datetime DEFAULT current_timestamp(),
  `status` enum('Active','Inactive') DEFAULT 'Active',
  `category_id` int(11) DEFAULT NULL,
  `fees` int(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `doctors`
--

INSERT INTO `doctors` (`doctor_id`, `full_name`, `specialization`, `contact_number`, `email`, `profile_picture`, `account_id`, `experience`, `registration_date`, `status`, `category_id`, `fees`) VALUES
(1, 'komal verma ', 'neurology', '2147483647', 'komal@gmail.com', '/static/uploads/7_dr-rashmi-nandwana-66f61dbfea1f2.jpg', '7', 0, '2025-02-12 16:53:05', 'Active', 2, 0),
(12, 'Vinod Gupta', 'psychiatry', '2147483647', 'vinod@gmail.com', '/static/uploads/9_avatar_1.png', '9', 6, '2025-02-13 00:34:17', 'Active', 6, 599);

-- --------------------------------------------------------

--
-- Table structure for table `labtest`
--

CREATE TABLE `labtest` (
  `test_id` int(250) NOT NULL,
  `test_name` varchar(250) NOT NULL,
  `description` varchar(250) NOT NULL,
  `test_price` int(250) NOT NULL,
  `icon_url` varchar(250) NOT NULL,
  `type` enum('Top Test','Women Care','Daily Routine') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `labtest`
--

INSERT INTO `labtest` (`test_id`, `test_name`, `description`, `test_price`, `icon_url`, `type`) VALUES
(1, 'Lipid Profile', 'Measures cholesterol and triglyceride levels to assess heart disease risk.', 800, '/static/uploads\\labTest\\Heart.png', 'Top Test'),
(2, 'Complete Blood Count (CBC)', 'A comprehensive blood test that evaluates overall health and detects disorders like anemia, infection, and leukemia.', 500, '/static/uploads\\labTest\\Blood_Studies.png', 'Top Test'),
(3, 'Liver Function Test (LFT) ', 'Evaluates liver enzymes and bilirubin levels.', 500, '/static/uploads\\labTest\\Liver.png', 'Daily Routine'),
(4, 'Kidney Function Test (KFT)', 'Checks creatinine and urea levels for kidney health.', 600, '/static/uploads\\labTest\\Kidney.png', 'Daily Routine'),
(5, 'HbA1c Test ', 'Determines average blood sugar levels over the past 3 months.', 1000, '/static/uploads\\labTest\\Diabetes.png', 'Top Test'),
(6, 'Fasting Blood Sugar (FBS) ', 'Measures blood glucose levels after fasting.', 500, '/static/uploads\\labTest\\Blood_Studies.png', 'Top Test'),
(7, 'Vitamin D Test ', 'Checks vitamin D levels essential for bone health.', 299, '/static/uploads\\labTest\\VITAMIN.png', 'Daily Routine'),
(8, 'Iron Studies', 'Measures iron, ferritin, and TIBC levels for anemia diagnosis.', 489, '/static/uploads\\labTest\\Iron_Studies.png', 'Daily Routine'),
(9, 'PCOD Screening', 'periods related problems', 499, '/static/uploads\\labTest\\WOMENS_HEALTH_0.png', 'Women Care'),
(10, 'Pregnancy', 'pregnant women sonography', 900, '/static/uploads\\labTest\\Pregnancy.png', 'Women Care'),
(11, 'Full Body Checkup', 'full body chekup', 1000, '/static/uploads\\labTest\\Full_Body_Checkup.png', 'Daily Routine'),
(12, 'Diabetes', 'sugar test for insulin', 500, '/static/uploads\\labTest\\Diabetes.png', 'Daily Routine'),
(13, 'HairFall', '', 300, '/static/uploads\\labTest\\Hairfall.png', 'Daily Routine'),
(14, 'Blood Studies', '', 299, '/static/uploads\\labTest\\Blood_Studies_Anemia.png', 'Women Care'),
(15, 'Hormone Panel Test', 'Checks estrogen, progesterone, and other hormone levels for reproductive health.', 500, '/static/uploads\\labTest\\STD.png', 'Women Care'),
(16, 'Covid 19', '', 300, '/static/uploads\\labTest\\Covid.png', 'Daily Routine'),
(17, 'Senior Citizen', '', 1000, '/static/uploads\\labTest\\Senior_Citizen.png', 'Daily Routine'),
(18, 'Fever ', '', 389, '/static/uploads\\labTest\\Fever.png', 'Daily Routine'),
(19, 'Allergy ', '', 300, '/static/uploads\\labTest\\Allergy_1.png', 'Daily Routine'),
(20, 'Reproductive & Fertility', '', 1100, '/static/uploads\\labTest\\Infertility.png', 'Women Care'),
(21, 'Hormone', '', 699, '/static/uploads\\labTest\\HORMONE.png', 'Women Care'),
(22, 'Cancer Screening', '', 2000, '/static/uploads\\labTest\\Cancer__Screening_0.png', 'Daily Routine');

-- --------------------------------------------------------

--
-- Table structure for table `patient_profiles`
--

CREATE TABLE `patient_profiles` (
  `patient_id` int(11) NOT NULL,
  `full_name` varchar(255) NOT NULL,
  `gender` enum('Male','Female','Other') NOT NULL,
  `dob` date NOT NULL,
  `contact_number` varchar(15) NOT NULL,
  `email` varchar(255) NOT NULL,
  `address` text DEFAULT NULL,
  `blood_group` varchar(10) DEFAULT NULL,
  `allergies` text DEFAULT NULL,
  `chronic_conditions` text DEFAULT NULL,
  `current_medications` text DEFAULT NULL,
  `emergency_contact_name` varchar(255) NOT NULL,
  `emergency_contact_number` varchar(15) NOT NULL,
  `last_visit_date` date DEFAULT NULL,
  `next_appointment_date` date DEFAULT NULL,
  `visit_notes` text DEFAULT NULL,
  `insurance_provider` varchar(255) DEFAULT NULL,
  `policy_number` varchar(255) DEFAULT NULL,
  `insurance_expiry_date` date DEFAULT NULL,
  `profile_picture` varchar(255) DEFAULT NULL,
  `registration_date` datetime DEFAULT current_timestamp(),
  `age` int(100) NOT NULL,
  `height_feet` int(10) NOT NULL,
  `height_inch` int(200) NOT NULL,
  `city` varchar(250) NOT NULL,
  `state` varchar(250) NOT NULL,
  `weight` int(200) NOT NULL,
  `status` enum('active','inactive') DEFAULT 'active'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `patient_profiles`
--

INSERT INTO `patient_profiles` (`patient_id`, `full_name`, `gender`, `dob`, `contact_number`, `email`, `address`, `blood_group`, `allergies`, `chronic_conditions`, `current_medications`, `emergency_contact_name`, `emergency_contact_number`, `last_visit_date`, `next_appointment_date`, `visit_notes`, `insurance_provider`, `policy_number`, `insurance_expiry_date`, `profile_picture`, `registration_date`, `age`, `height_feet`, `height_inch`, `city`, `state`, `weight`, `status`) VALUES
(6, 'mandeep singh chandel', 'Male', '2025-02-01', '2221789932', 'mandeep@gmail.com', NULL, 'AB+', 'none', 'none', 'none', 'shivangi', '9509489976', NULL, NULL, NULL, 'healthify', '12433577', '2025-02-28', '/static/uploads/6_CARD.PNG', '2025-02-16 17:12:29', 0, 0, 0, '', '', 0, 'inactive'),
(10, 'shivangi', 'Female', '2003-12-01', '2147483647', 'shivangi@gmail.com', 'chandpole chowka', 'AB+', 'none', 'migraine', 'none', 'komal verma', '9509489976', NULL, NULL, NULL, 'healthify', '12933568', '2025-02-28', '/static/uploads/avatar_3.PNG', '2025-02-22 21:45:54', 21, 5, 1, 'jodhpur', 'Rajasthan', 60, 'active');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(250) NOT NULL,
  `email` varchar(150) NOT NULL,
  `password` varchar(200) NOT NULL,
  `contact_number` int(10) NOT NULL,
  `role` enum('patient','doctor') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password`, `contact_number`, `role`) VALUES
(6, 'mandeep', 'mandeep@gmail.com', 'mandeep', 2147483647, 'patient'),
(7, 'komal verma', 'komal@gmail.com', 'komal', 2147483647, 'doctor'),
(8, 'Rashmika Dr.', 'rashmika@gmail.com', 'rashmika', 2147483647, 'doctor'),
(9, 'Vinod gupta', 'vinod@gmail.com', 'vinod', 2147483647, 'doctor'),
(10, 'shivangi', 'shivangi@gmail.com', 'shivangi', 2147483647, 'patient'),
(11, 'garvita', 'garvita@gmail.com', 'garvita', 2147483647, 'doctor');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admins`
--
ALTER TABLE `admins`
  ADD PRIMARY KEY (`admin_id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `appointments`
--
ALTER TABLE `appointments`
  ADD PRIMARY KEY (`appointment_id`),
  ADD KEY `patient_id` (`patient_id`),
  ADD KEY `doctor_id` (`doctor_id`);

--
-- Indexes for table `bookings`
--
ALTER TABLE `bookings`
  ADD PRIMARY KEY (`id`),
  ADD KEY `doctor_id` (`doctor_id`),
  ADD KEY `patient_id` (`patient_id`);

--
-- Indexes for table `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`category_id`);

--
-- Indexes for table `department`
--
ALTER TABLE `department`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `doctors`
--
ALTER TABLE `doctors`
  ADD PRIMARY KEY (`doctor_id`),
  ADD UNIQUE KEY `account_id` (`account_id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `fk_category` (`category_id`);

--
-- Indexes for table `labtest`
--
ALTER TABLE `labtest`
  ADD PRIMARY KEY (`test_id`);

--
-- Indexes for table `patient_profiles`
--
ALTER TABLE `patient_profiles`
  ADD PRIMARY KEY (`patient_id`),
  ADD UNIQUE KEY `contact_number` (`contact_number`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admins`
--
ALTER TABLE `admins`
  MODIFY `admin_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `appointments`
--
ALTER TABLE `appointments`
  MODIFY `appointment_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `bookings`
--
ALTER TABLE `bookings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `department`
--
ALTER TABLE `department`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `doctors`
--
ALTER TABLE `doctors`
  MODIFY `doctor_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `labtest`
--
ALTER TABLE `labtest`
  MODIFY `test_id` int(250) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `patient_profiles`
--
ALTER TABLE `patient_profiles`
  MODIFY `patient_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `appointments`
--
ALTER TABLE `appointments`
  ADD CONSTRAINT `appointments_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patient_profiles` (`patient_id`),
  ADD CONSTRAINT `appointments_ibfk_2` FOREIGN KEY (`doctor_id`) REFERENCES `doctors` (`doctor_id`);

--
-- Constraints for table `bookings`
--
ALTER TABLE `bookings`
  ADD CONSTRAINT `bookings_ibfk_1` FOREIGN KEY (`doctor_id`) REFERENCES `doctors` (`doctor_id`),
  ADD CONSTRAINT `bookings_ibfk_2` FOREIGN KEY (`patient_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `doctors`
--
ALTER TABLE `doctors`
  ADD CONSTRAINT `fk_category` FOREIGN KEY (`category_id`) REFERENCES `categories` (`category_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
