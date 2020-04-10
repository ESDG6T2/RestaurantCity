-- phpMyAdmin SQL Dump
-- version 4.7.9
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Mar 11, 2020 at 05:29 AM
-- Server version: 5.7.21
-- PHP Version: 7.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `restaurant`
--
CREATE DATABASE IF NOT EXISTS `restaurantCity_menu` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `restaurantCity_menu`;

-- --------------------------------------------------------

--
-- Table structure for table `menu`
--

DROP TABLE IF EXISTS `menu`;
CREATE TABLE IF NOT EXISTS `menu` (
  `menuID` varchar(45) NOT NULL,
  `foodName` varchar(45) NOT NULL,
  `price` float(5,2) NOT NULL,
  PRIMARY KEY (`menuID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `menu`
--

INSERT INTO `menu` (`menuID`, `foodName`, `price`) VALUES
('F01', 'Bola Obi', 10.00),
('F02', 'Char Siew Rice', 10.00),
('F03', 'Chicken Chop Ipoh Hor Fun', 5.00),
('F04', 'Claypot Chicken Rice', 10.00),
('F05', 'Lei Cha', 20.00),
('F06', 'Lor Mee', 10.00),
('F07', 'Nonya Laksa', 10.00),
('F08', 'Octopus', 10.00),
('F09', 'Packet Nasi Liwet Komplit', 10.00),
('F10', 'Papua-style Nasi', 5.00);

COMMIT;