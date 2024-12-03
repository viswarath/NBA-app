CREATE DATABASE `mynbadb` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
CREATE TABLE `team` (
  `team_id` char(3) NOT NULL,
  `div_name` varchar(255) DEFAULT NULL,
  `div_place` int DEFAULT NULL,
  `conf_name` varchar(255) DEFAULT NULL,
  `conf_place` int DEFAULT NULL,
  PRIMARY KEY (`team_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `player` (
  `player_id` int NOT NULL,
  `team_id` char(3) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `age` int DEFAULT NULL,
  `position` varchar(255) DEFAULT NULL,
  `games_started` int DEFAULT NULL,
  `player_rank` int DEFAULT NULL,
  PRIMARY KEY (`player_id`),
  KEY `team_id` (`team_id`),
  CONSTRAINT `player_ibfk_1` FOREIGN KEY (`team_id`) REFERENCES `team` (`team_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
