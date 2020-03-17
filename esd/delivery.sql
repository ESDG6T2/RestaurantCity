-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Mar 13, 2020 at 10:06 AM
-- Server version: 5.7.19
-- PHP Version: 7.1.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `restaurantdel`
--
CREATE DATABASE IF NOT EXISTS `restaurantdel` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `restaurantdel`;
-- --------------------------------------------------------

--
-- Table structure for table `driver`
--

DROP TABLE IF EXISTS `driver`;
CREATE TABLE IF NOT EXISTS `driver` (
  `driverId` varchar(45) NOT NULL,
  `orderId` varchar(45) NOT NULL,
  `customer_name` varchar(45) NOT NULL,
  `contactNo` varchar(45) NOT NULL,
  `billingAddress` varchar(45) NOT NULL,
  PRIMARY KEY (`driverId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `driver`
--

INSERT INTO `driver` (`driverId`, `orderId`, `customer_name`, `contactNo`, `billingAddress`) VALUES
('D001', 'O001', 'James', '91234567', 'Tampines'),
('D002', 'O002', 'Joe', '91231111', 'Simei'),
('D003', 'O003', 'Jill', '91232222', 'Pasir')
;


COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
