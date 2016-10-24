-- phpMyAdmin SQL Dump
-- version 4.2.11
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Sep 10, 2016 at 02:20 PM
-- Server version: 5.6.21
-- PHP Version: 5.6.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `seatdriversapp`
--

-- --------------------------------------------------------

--
-- Table structure for table `driver`
--

CREATE TABLE IF NOT EXISTS `driver` (
`id` int(11) NOT NULL,
  `name` varchar(128) NOT NULL,
  `phone_number` varchar(16) NOT NULL,
  `registered_date` datetime NOT NULL,
  `status` varchar(64) DEFAULT NULL,
  `reason` varchar(128) DEFAULT NULL,
  `status_changed_date` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `profile_image` text,
  `device_id` text NOT NULL,
  `os_type` varchar(16) NOT NULL,
  `auth_code` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `driverdetails`
--

CREATE TABLE IF NOT EXISTS `driverdetails` (
`id` int(11) NOT NULL,
  `proofname` varchar(128) NOT NULL,
  `image` text NOT NULL,
  `expiry_dl` datetime NOT NULL,
  `dl_details` text,
  `expiry_rc` datetime NOT NULL,
  `rc_details` text,
  `expiry_tax_paid` datetime NOT NULL,
  `tax_paid_details` text,
  `expiry_insurance` datetime NOT NULL,
  `insurance_details` text,
  `driver_id` int(11) NOT NULL,
  `driver_user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE IF NOT EXISTS `user` (
`id` int(11) NOT NULL,
  `name` varchar(128) NOT NULL,
  `phone_number` varchar(16) NOT NULL,
  `email_Id` varchar(128) NOT NULL,
  `user_role_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `userrole`
--

CREATE TABLE IF NOT EXISTS `userrole` (
`id` int(11) NOT NULL,
  `role` varchar(128) NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `userrole`
--

INSERT INTO `userrole` (`id`, `role`) VALUES
(1, 'Driver');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `driver`
--
ALTER TABLE `driver`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `phone_number` (`phone_number`), ADD KEY `user_id` (`user_id`), ADD KEY `user_id_2` (`user_id`), ADD KEY `user_id_3` (`user_id`);

--
-- Indexes for table `driverdetails`
--
ALTER TABLE `driverdetails`
 ADD PRIMARY KEY (`id`), ADD KEY `driver_id` (`driver_id`,`driver_user_id`), ADD KEY `driver_user_id` (`driver_user_id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `phone_number` (`phone_number`), ADD KEY `user_role_id` (`user_role_id`);

--
-- Indexes for table `userrole`
--
ALTER TABLE `userrole`
 ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `driver`
--
ALTER TABLE `driver`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `driverdetails`
--
ALTER TABLE `driverdetails`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `userrole`
--
ALTER TABLE `userrole`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=2;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `driver`
--
ALTER TABLE `driver`
ADD CONSTRAINT `driver_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `driverdetails`
--
ALTER TABLE `driverdetails`
ADD CONSTRAINT `driverdetails_ibfk_1` FOREIGN KEY (`driver_id`) REFERENCES `driver` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `user`
--
ALTER TABLE `user`
ADD CONSTRAINT `user_ibfk_1` FOREIGN KEY (`user_role_id`) REFERENCES `userrole` (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
