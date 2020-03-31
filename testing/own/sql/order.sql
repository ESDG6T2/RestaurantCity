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
CREATE DATABASE IF NOT EXISTS `restaurantCity_order` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `restaurantCity_order`;

-- --------------------------------------------------------

--
-- Table structure for table `orderdetail`
--

DROP TABLE IF EXISTS `orderdetail`;
CREATE TABLE IF NOT EXISTS `orderdetail` (
  `orderId` char(32) NOT NULL,
  `menuId` varchar(45) NOT NULL,
  `quantity` int(11) NOT NULL,
  PRIMARY KEY (`orderId`,`menuId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `order`;
CREATE TABLE IF NOT EXISTS `order` (
  `orderId` char(32) NOT NULL,
  `userId` varchar(45) NOT NULL,
  `deliveryAddress` varchar(45) NOT NULL,
  `customerName` varchar(45) NOT NULL,
  `contactNumber` varchar(45) NOT NULL,
  `totalAmount` float(5,2) NOT NULL,
  `orderStatus` varchar(10) DEFAULT NULL,
  `datetime` datetime NOT NULL,
  `driverId` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`orderId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE `orderdetail`
  ADD CONSTRAINT `orderdetail_fk1` FOREIGN KEY (`orderId`) REFERENCES `order` (`orderId`) ON DELETE CASCADE;
COMMIT;



