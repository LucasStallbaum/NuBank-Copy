CREATE DATABASE  IF NOT EXISTS `banco_digital` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `banco_digital`;
-- MySQL dump 10.13  Distrib 8.0.30, for Win64 (x86_64)
--
-- Host: localhost    Database: banco_digital
-- ------------------------------------------------------
-- Server version	8.0.30

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `colaborador`
--

DROP TABLE IF EXISTS `colaborador`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `colaborador` (
  `id_colaborador` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `cpf` char(11) NOT NULL,
  `rg` varchar(10) DEFAULT NULL,
  `data_nascimento` date NOT NULL,
  `sexo` char(1) DEFAULT NULL,
  `telefone` varchar(15) DEFAULT NULL,
  `endereco` varchar(100) DEFAULT NULL,
  `bairro` varchar(20) DEFAULT NULL,
  `estado` char(2) DEFAULT NULL,
  `cep` char(8) NOT NULL,
  `cidade` varchar(50) DEFAULT NULL,
  `pais` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id_colaborador`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `colaborador`
--

LOCK TABLES `colaborador` WRITE;
/*!40000 ALTER TABLE `colaborador` DISABLE KEYS */;
INSERT INTO `colaborador` VALUES (1,'ARTHUR LUFT RIBEIRO','55811614020','283280475','2022-08-03','M','45999979955','AVENIDA LAGOA VERMELHA, 2587','CIDADE ALTA','PR','85884000','MEDIANEIRA','BRASIL'),(2,'LUCAS STALLBAUM','12540208735','435745206','2000-02-09','M','1199730782','RIO DE JANEIRO, 2300','CENTRO','PR','85884000','MEDIANEIRA','BRASIL'),(3,'VINICIUS MARMENTINI','87540248722','815765267','2003-11-01','M','454473867429','ALAGOS, 840','CIDADE ALTA','PR','85884000','MEDIANEIRA','BRASIL'),(4,'EDUARDO MARMENTINI','43510248877','235765405','2003-11-01','M','459993867432','ALAGOS, 840','CIDADE ALTA','PR','85884000','MEDIANEIRA','BRASIL'),(5,'ANA PAULA ROSIN','77510248432','537765405','2006-03-14','F','45996567871','RIO GRANDE DO NORTE, 2360','CIDADE ALTA','PR','85884000','MEDIANEIRA','BRASIL');
/*!40000 ALTER TABLE `colaborador` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `conta`
--

DROP TABLE IF EXISTS `conta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `conta` (
  `id_colaborador` int NOT NULL,
  `id_conta` int NOT NULL AUTO_INCREMENT,
  `agencia` char(5) NOT NULL,
  `conta` int NOT NULL,
  `limite_credito` int NOT NULL DEFAULT '0',
  `fatura` int NOT NULL DEFAULT '0',
  `saldo` decimal(10,2) NOT NULL DEFAULT '0.00',
  `status` char(1) NOT NULL DEFAULT 'A',
  `senha` int NOT NULL,
  PRIMARY KEY (`id_conta`),
  KEY `id_colaborador` (`id_colaborador`),
  CONSTRAINT `conta_ibfk_1` FOREIGN KEY (`id_colaborador`) REFERENCES `colaborador` (`id_colaborador`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `conta`
--

LOCK TABLES `conta` WRITE;
/*!40000 ALTER TABLE `conta` DISABLE KEYS */;
INSERT INTO `conta` VALUES (1,1,'4343',465889,0,0,2000.00,'A',11111111),(2,2,'4343',870351,0,0,383000.00,'A',22222222),(3,3,'4343',485043,0,0,0.00,'A',33333333),(4,4,'4343',702347,0,0,400.00,'A',44444444),(5,5,'4343',345765,0,0,600.00,'A',55555555);
/*!40000 ALTER TABLE `conta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `historico_transacoes`
--

DROP TABLE IF EXISTS `historico_transacoes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `historico_transacoes` (
  `id_transacao` int NOT NULL AUTO_INCREMENT,
  `id_colaborador` int NOT NULL,
  `id_conta` int NOT NULL,
  `id_conta_recebimento` int NOT NULL,
  `valor` decimal(10,0) NOT NULL,
  `data_transacao` date DEFAULT NULL,
  `status` char(1) DEFAULT 'S',
  PRIMARY KEY (`id_transacao`),
  KEY `id_colaborador` (`id_colaborador`),
  KEY `id_conta` (`id_conta`),
  CONSTRAINT `historico_transacoes_ibfk_1` FOREIGN KEY (`id_colaborador`) REFERENCES `colaborador` (`id_colaborador`),
  CONSTRAINT `historico_transacoes_ibfk_2` FOREIGN KEY (`id_conta`) REFERENCES `conta` (`id_conta`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historico_transacoes`
--

LOCK TABLES `historico_transacoes` WRITE;
/*!40000 ALTER TABLE `historico_transacoes` DISABLE KEYS */;
INSERT INTO `historico_transacoes` VALUES (1,1,1,2,232,'2022-08-03','S');
/*!40000 ALTER TABLE `historico_transacoes` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-09-19 20:41:34
