-- phpMyAdmin SQL Dump
-- version 5.0.3
-- https://www.phpmyadmin.net/
--
-- 主機： 127.0.0.1:3307
-- 產生時間： 2020-11-29 13:32:36
-- 伺服器版本： 10.4.14-MariaDB
-- PHP 版本： 7.3.23

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫： `advancedsw`
--

-- --------------------------------------------------------

--
-- 資料表結構 `food`
--

CREATE TABLE `food` (
  `ingredientid` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ingredientname` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='食材';

--
-- 傾印資料表的資料 `food`
--

INSERT INTO `food` (`ingredientid`, `ingredientname`) VALUES
('1', '糖'),
('2', '鹽');

-- --------------------------------------------------------

--
-- 資料表結構 `foodandrecipe`
--

CREATE TABLE `foodandrecipe` (
  `selfid` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `mealid` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ingredientid` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- 傾印資料表的資料 `foodandrecipe`
--

INSERT INTO `foodandrecipe` (`selfid`, `mealid`, `ingredientid`) VALUES
('1', '1', '1'),
('2', '1', '2'),
('3', '2', '1');

-- --------------------------------------------------------

--
-- 資料表結構 `link`
--

CREATE TABLE `link` (
  `meallink` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- 傾印資料表的資料 `link`
--

INSERT INTO `link` (`meallink`) VALUES
('https://www.youtube.com/watch?v=5s-JNrKtQtQ&ab_channel=%E5%85%8B%E9%87%8C%E6%96%AF%E9%A4%90%E6%A1%8C'),
('https://www.youtube.com/watch?v=b8VZQ7sLyNI&t=1s&ab_channel=Wecook123%E6%96%99%E7%90%86123'),
('https://www.youtube.com/watch?v=haRLSizTMf0&ab_channel=Wecook123%E6%96%99%E7%90%86123'),
('https://www.youtube.com/watch?v=hLkHCVEd9Yk&ab_channel=%E8%82%A5%E5%A4%A7%E5%8F%94FatUncle');

-- --------------------------------------------------------

--
-- 資料表結構 `linkandrecipe`
--

CREATE TABLE `linkandrecipe` (
  `selfid` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `mealid` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `meallink` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- 傾印資料表的資料 `linkandrecipe`
--

INSERT INTO `linkandrecipe` (`selfid`, `mealid`, `meallink`) VALUES
('1', '1', 'https://www.youtube.com/watch?v=b8VZQ7sLyNI&t=1s&ab_channel=Wecook123%E6%96%99%E7%90%86123'),
('2', '1', 'https://www.youtube.com/watch?v=5s-JNrKtQtQ&ab_channel=%E5%85%8B%E9%87%8C%E6%96%AF%E9%A4%90%E6%A1%8C'),
('3', '2', 'https://www.youtube.com/watch?v=hLkHCVEd9Yk&ab_channel=%E8%82%A5%E5%A4%A7%E5%8F%94FatUncle'),
('4', '2', 'https://www.youtube.com/watch?v=haRLSizTMf0&ab_channel=Wecook123%E6%96%99%E7%90%86123');

-- --------------------------------------------------------

--
-- 資料表結構 `recipe`
--

CREATE TABLE `recipe` (
  `mealid` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `mealname` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- 傾印資料表的資料 `recipe`
--

INSERT INTO `recipe` (`mealid`, `mealname`) VALUES
('1', '炒飯'),
('2', '炒麵');

-- --------------------------------------------------------

--
-- 資料表結構 `refrigerator`
--

CREATE TABLE `refrigerator` (
  `selfid` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ingredientname` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `date` date NOT NULL,
  `expire` date NOT NULL,
  `account` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `deadline` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- 傾印資料表的資料 `refrigerator`
--

INSERT INTO `refrigerator` (`selfid`, `ingredientname`, `date`, `expire`, `account`, `deadline`) VALUES
('1', '哭阿', '2020-11-11', '2020-11-30', '123', '19');

-- --------------------------------------------------------

--
-- 資料表結構 `user`
--

CREATE TABLE `user` (
  `account` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- 傾印資料表的資料 `user`
--

INSERT INTO `user` (`account`, `password`) VALUES
('123', '123');

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `food`
--
ALTER TABLE `food`
  ADD PRIMARY KEY (`ingredientid`);

--
-- 資料表索引 `foodandrecipe`
--
ALTER TABLE `foodandrecipe`
  ADD PRIMARY KEY (`selfid`),
  ADD KEY `mealid` (`mealid`),
  ADD KEY `ingredientid` (`ingredientid`);

--
-- 資料表索引 `link`
--
ALTER TABLE `link`
  ADD PRIMARY KEY (`meallink`);

--
-- 資料表索引 `linkandrecipe`
--
ALTER TABLE `linkandrecipe`
  ADD PRIMARY KEY (`selfid`),
  ADD KEY `mealid` (`mealid`);

--
-- 資料表索引 `recipe`
--
ALTER TABLE `recipe`
  ADD PRIMARY KEY (`mealid`);

--
-- 資料表索引 `refrigerator`
--
ALTER TABLE `refrigerator`
  ADD KEY `account` (`account`);

--
-- 資料表索引 `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`account`);

--
-- 已傾印資料表的限制式
--

--
-- 資料表的限制式 `foodandrecipe`
--
ALTER TABLE `foodandrecipe`
  ADD CONSTRAINT `foodandrecipe_ibfk_1` FOREIGN KEY (`mealid`) REFERENCES `recipe` (`mealid`),
  ADD CONSTRAINT `foodandrecipe_ibfk_2` FOREIGN KEY (`ingredientid`) REFERENCES `food` (`ingredientid`);

--
-- 資料表的限制式 `linkandrecipe`
--
ALTER TABLE `linkandrecipe`
  ADD CONSTRAINT `linkandrecipe_ibfk_1` FOREIGN KEY (`mealid`) REFERENCES `recipe` (`mealid`);

--
-- 資料表的限制式 `refrigerator`
--
ALTER TABLE `refrigerator`
  ADD CONSTRAINT `refrigerator_ibfk_1` FOREIGN KEY (`account`) REFERENCES `user` (`account`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
