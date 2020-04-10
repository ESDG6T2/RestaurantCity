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
CREATE DATABASE IF NOT EXISTS `restaurantCity_cart` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `restaurantCity_cart`;

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

COMMIT;