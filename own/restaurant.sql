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
-- Database: `restaurant`
--
Drop database if exists `restaurant`;
create database if not exists `restaurant`;
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

-- --------------------------------------------------------

--
-- Table structure for table `orderdetail`
--

DROP TABLE IF EXISTS `orderdetail`;
CREATE TABLE IF NOT EXISTS `orderdetail` (
  `orderId` int(11) NOT NULL,
  `menuId` varchar(45) NOT NULL,
  `Qty` int(11) NOT NULL,
  PRIMARY KEY (`orderId`,`menuId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `orderdetail`
--

INSERT INTO `orderdetail` (`orderId`, `menuId`, `Qty`) VALUES
(1, 'F01', 5);

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
CREATE TABLE IF NOT EXISTS `orders` (
  `orderId` int(11) NOT NULL AUTO_INCREMENT,
  `userID` varchar(45) NOT NULL,
  `billingAddress` varchar(45) NOT NULL,
  `postalCode` varchar(45) NOT NULL,
  `contactNo` varchar(45) NOT NULL,
  PRIMARY KEY (`orderId`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`orderId`, `userID`, `billingAddress`, `postalCode`, `contactNo`) VALUES
(1, 'a', 'address 1', '313456', 'Alex');

-- --------------------------------------------------------

--
-- Table structure for table `temp_cart`
--

DROP TABLE IF EXISTS `temp_cart`;
CREATE TABLE IF NOT EXISTS `temp_cart` (
  `userid` varchar(45) NOT NULL,
  `menuID` varchar(45) NOT NULL,
  `quantity` int(11) NOT NULL,
  PRIMARY KEY (`userid`,`menuID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `temp_cart`
--

INSERT INTO `temp_cart` (`userid`, `menuID`, `quantity`) VALUES
('a', 'F09', 4);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `userID` varchar(45) NOT NULL,
  `password` varchar(45) NOT NULL,
  PRIMARY KEY (`userID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`userID`, `password`) VALUES
('a', 'b'),
('admin', 'password'),
('user', 'password');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
