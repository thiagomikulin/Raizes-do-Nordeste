-- MySQL dump 10.13  Distrib 8.0.46, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: raizes_do_nordeste
-- ------------------------------------------------------
-- Server version	9.7.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ 'f0593c82-72b6-11f1-b853-a6c088ab17fe:1-412';

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('ddf3f70ac9ae');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `campanhaPromos`
--

DROP TABLE IF EXISTS `campanhaPromos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `campanhaPromos` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Nome` varchar(80) NOT NULL,
  `Desconto(%)` int NOT NULL,
  `Validade` datetime NOT NULL,
  `Ativo` tinyint(1) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `campanhaPromos`
--

LOCK TABLES `campanhaPromos` WRITE;
/*!40000 ALTER TABLE `campanhaPromos` DISABLE KEYS */;
INSERT INTO `campanhaPromos` VALUES (1,'Festão Nordestino',10,'2026-07-30 00:00:00',1),(2,'Aniversário Raízes do Nordeste',5,'2026-03-30 00:00:00',1),(3,'Carnaval Raiz',8,'2026-02-05 00:00:00',1),(4,'Promoção nova',10,'2026-12-28 00:00:00',0);
/*!40000 ALTER TABLE `campanhaPromos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clientes`
--

DROP TABLE IF EXISTS `clientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clientes` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Nome` varchar(50) NOT NULL,
  `Email` varchar(50) NOT NULL,
  `CPF` varchar(50) NOT NULL,
  `Escaneamento_facial` varchar(200) DEFAULT NULL,
  `Senha` varchar(200) NOT NULL,
  `Endereço` varchar(80) DEFAULT NULL,
  `Fidelidade` int NOT NULL,
  `Nascimento` date DEFAULT NULL,
  `Ativo` tinyint(1) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clientes`
--

LOCK TABLES `clientes` WRITE;
/*!40000 ALTER TABLE `clientes` DISABLE KEYS */;
INSERT INTO `clientes` VALUES (1,'Thiago Mikulin','thiagomikulin@gmail.com','999.999.999-99','','$2b$12$P37Fap.uEU9D5TZ4iqZxyeUlZZWCVMG.A4psVKO9Y5vHiH7YkZPcO','',10,'2000-03-28',1);
/*!40000 ALTER TABLE `clientes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `estoqueItens`
--

DROP TABLE IF EXISTS `estoqueItens`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estoqueItens` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Estoque` int DEFAULT NULL,
  `Ingrediente` int DEFAULT NULL,
  `Quantidade` int NOT NULL,
  `UnidadeMedida` varchar(2) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `Estoque` (`Estoque`),
  KEY `Ingrediente` (`Ingrediente`),
  CONSTRAINT `estoqueItens_ibfk_1` FOREIGN KEY (`Estoque`) REFERENCES `estoques` (`ID`),
  CONSTRAINT `estoqueItens_ibfk_2` FOREIGN KEY (`Ingrediente`) REFERENCES `ingredientes` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estoqueItens`
--

LOCK TABLES `estoqueItens` WRITE;
/*!40000 ALTER TABLE `estoqueItens` DISABLE KEYS */;
INSERT INTO `estoqueItens` VALUES (1,1,29,5,'UN');
/*!40000 ALTER TABLE `estoqueItens` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `estoques`
--

DROP TABLE IF EXISTS `estoques`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estoques` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Filial` int DEFAULT NULL,
  `Ativo` tinyint(1) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `Filial` (`Filial`),
  CONSTRAINT `estoques_ibfk_1` FOREIGN KEY (`Filial`) REFERENCES `filiais` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estoques`
--

LOCK TABLES `estoques` WRITE;
/*!40000 ALTER TABLE `estoques` DISABLE KEYS */;
INSERT INTO `estoques` VALUES (1,1,1);
/*!40000 ALTER TABLE `estoques` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `filiais`
--

DROP TABLE IF EXISTS `filiais`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `filiais` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Cidade` varchar(100) NOT NULL,
  `Estrutura` enum('Completa','Reduzida') NOT NULL,
  `Endereco` varchar(100) NOT NULL,
  `Ativo` tinyint(1) NOT NULL,
  `ContaBanco` blob NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `filiais`
--

LOCK TABLES `filiais` WRITE;
/*!40000 ALTER TABLE `filiais` DISABLE KEYS */;
INSERT INTO `filiais` VALUES (1,'Recife-BA','Completa','string',1,_binary 'gAAAAABqQTgKzNBixnm3g-YwBniV2kqzWUXziOeZ6vr0tOBoNT4S8PnuhbA8X-YG0NQNhCe7phtu6ww24j8lJALVfVIlutujDg==');
/*!40000 ALTER TABLE `filiais` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `filiaisPromos`
--

DROP TABLE IF EXISTS `filiaisPromos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `filiaisPromos` (
  `CampanhaPromo` int NOT NULL,
  `Filial` int NOT NULL,
  `Ativo` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`CampanhaPromo`,`Filial`),
  KEY `Filial` (`Filial`),
  CONSTRAINT `filiaisPromos_ibfk_1` FOREIGN KEY (`CampanhaPromo`) REFERENCES `campanhaPromos` (`ID`),
  CONSTRAINT `filiaisPromos_ibfk_2` FOREIGN KEY (`Filial`) REFERENCES `filiais` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `filiaisPromos`
--

LOCK TABLES `filiaisPromos` WRITE;
/*!40000 ALTER TABLE `filiaisPromos` DISABLE KEYS */;
/*!40000 ALTER TABLE `filiaisPromos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ingredientes`
--

DROP TABLE IF EXISTS `ingredientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ingredientes` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Nome` varchar(80) NOT NULL,
  `Periodo` enum('Verão','Outono','Inverno','Primavera') NOT NULL,
  `Ativo` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ingredientes`
--

LOCK TABLES `ingredientes` WRITE;
/*!40000 ALTER TABLE `ingredientes` DISABLE KEYS */;
INSERT INTO `ingredientes` VALUES (1,'Camarão','Verão',1),(2,'Cebola','Verão',1),(3,'Tomate','Verão',1),(4,'Leite de coco','Verão',1),(5,'Azeite de dendê','Verão',1),(6,'Cheiro Verde','Verão',1),(7,'Pão','Verão',1),(8,'Pimenta cheirosa','Verão',1),(9,'Sal','Verão',1),(10,'Pimenta malagueta','Verão',1),(11,'Castanha de caju','Verão',1),(12,'Amendoim','Verão',1),(13,'Gengibre','Verão',1),(14,'Macaxeira','Verão',1),(15,'Leite','Verão',1),(16,'Manteiga','Verão',1),(17,'Creme de Leite','Verão',1),(18,'Charque','Verão',1),(19,'Pimentão Verde','Verão',1),(20,'Coentro','Verão',1),(21,'Queijo Mussarela','Verão',1),(22,'Queijo Parmesão','Verão',1),(23,'Alho','Verão',1),(24,'Calabresa','Verão',1),(25,'Farinha de trigo','Verão',1),(26,'Açúcar','Verão',1),(27,'Essência de Baunilha','Verão',1),(28,'Fermento químico','Verão',1),(29,'Milharina','Verão',1);
/*!40000 ALTER TABLE `ingredientes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `logs`
--

DROP TABLE IF EXISTS `logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `logs` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Acao` enum('criar','ativar','desativar','editar','excluir','alterar status','atualizar campo') NOT NULL,
  `Tabela` enum('pedidos','pedidoItens','movimentos','movimentoItens','usuarios','clientes','variacoes','produtos','ingredientes','filiais','estoqueItens','estoques','campanhaPromos','variacoesFiliais','usuariosFiliais','filiaisPromos','receitasItens') DEFAULT NULL,
  `IdModificado` varchar(12) NOT NULL,
  `Campo` varchar(100) NOT NULL,
  `ValorAnterior` varchar(200) NOT NULL,
  `ValorNovo` varchar(200) NOT NULL,
  `TipoPessoa` enum('Usuario','Cliente') DEFAULT NULL,
  `IdPessoa` int NOT NULL,
  `DataHora` datetime NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=145 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logs`
--

LOCK TABLES `logs` WRITE;
/*!40000 ALTER TABLE `logs` DISABLE KEYS */;
INSERT INTO `logs` VALUES (1,'criar','usuarios','id','id','','3','Usuario',2,'2026-06-28 06:03:58'),(2,'criar','usuarios','id','id','','4','Usuario',2,'2026-06-28 06:04:41'),(3,'editar','usuarios','3','nome, email, cargo','Cozinheiro , cozinheiro@cozinheiro.com , Não Classificado','UsuAtendente , atendente@atendente.com , Atendente','Usuario',2,'2026-06-28 06:04:55'),(4,'editar','usuarios','3','nome, email, cargo','Cozinheiro , cozinheiro@cozinheiro.com , Não Classificado','UsuAtendente , atendente@atendente.com , Atendente','Usuario',2,'2026-06-28 06:04:55'),(5,'editar','usuarios','3','nome, email, cargo','Cozinheiro , cozinheiro@cozinheiro.com , Não Classificado','UsuAtendente , atendente@atendente.com , Atendente','Usuario',2,'2026-06-28 06:04:55'),(6,'editar','usuarios','3','nome, email, cargo','UsuAtendente , atendente@atendente.com , Atendente','Cozinheiro , cozinheiro@cozinheiro.com , Cozinheiro','Usuario',2,'2026-06-28 06:05:45'),(7,'editar','usuarios','3','nome, email, cargo','UsuAtendente , atendente@atendente.com , Atendente','Cozinheiro , cozinheiro@cozinheiro.com , Cozinheiro','Usuario',2,'2026-06-28 06:05:45'),(8,'editar','usuarios','3','nome, email, cargo','UsuAtendente , atendente@atendente.com , Atendente','Cozinheiro , cozinheiro@cozinheiro.com , Cozinheiro','Usuario',2,'2026-06-28 06:05:45'),(9,'editar','usuarios','4','cargo','Não Classificado','Atendente','Usuario',2,'2026-06-28 06:06:22'),(10,'desativar','usuarios','id','ativo','True','False','Usuario',2,'2026-06-28 06:13:51'),(11,'ativar','usuarios','id','ativo','False','True','Usuario',2,'2026-06-28 06:20:33'),(12,'criar','usuarios','id','id','','5','Usuario',2,'2026-06-28 06:25:35'),(13,'editar','usuarios','5','cargo','Não Classificado','TI','Usuario',2,'2026-06-28 06:29:53'),(14,'criar','usuarios','id','id','','6','Usuario',2,'2026-06-28 12:39:29'),(15,'desativar','usuarios','id','ativo','True','False','Usuario',2,'2026-06-28 12:56:04'),(16,'ativar','usuarios','id','ativo','False','True','Usuario',2,'2026-06-28 12:56:17'),(17,'criar','clientes','id','id','','1','Usuario',4,'2026-06-28 13:13:43'),(18,'criar','usuarios','id','id','','7','Usuario',2,'2026-06-28 13:30:52'),(19,'editar','clientes','1','data_nasc','None','2000-03-28','Usuario',2,'2026-06-28 13:32:22'),(20,'editar','usuarios','7','cargo','Não Classificado','Gerente','Usuario',2,'2026-06-28 13:33:25'),(21,'editar','clientes','1','nome','Thiago Mikulin','Thiago dos Santos Mikulin','Usuario',2,'2026-06-28 13:33:49'),(22,'editar','clientes','1','nome','Thiago dos Santos Mikulin','Thiago Mikulin','Usuario',7,'2026-06-28 13:34:10'),(23,'desativar','clientes','id','ativo','True','False','Usuario',5,'2026-06-28 13:40:43'),(24,'ativar','clientes','id','ativo','False','True','Usuario',5,'2026-06-28 13:42:14'),(25,'atualizar campo','clientes','id','fidelidade','0','10','Usuario',2,'2026-06-28 14:23:19'),(26,'criar','filiais','id','id','','1','Usuario',5,'2026-06-28 15:04:43'),(27,'editar','filiais','1','estrutura, endereco','Reduzida , Praça Juscelino Kubitschek, s/n','Completa , string','Usuario',5,'2026-06-28 15:09:07'),(28,'editar','filiais','1','estrutura, endereco','Reduzida , Praça Juscelino Kubitschek, s/n','Completa , string','Usuario',5,'2026-06-28 15:09:07'),(29,'desativar','filiais','id','ativo','True','False','Usuario',5,'2026-06-28 15:13:08'),(30,'ativar','filiais','id','ativo','False','True','Usuario',5,'2026-06-28 15:13:47'),(31,'criar','filiaisPromos','promocao','promocao, filial','','1 , 1','Usuario',5,'2026-06-28 15:24:04'),(32,'criar','filiaisPromos','promocao','promocao, filial','','1 , 1','Usuario',5,'2026-06-28 15:24:04'),(33,'criar','filiaisPromos','promocao','promocao, filial','','1 , 1','Usuario',5,'2026-06-28 15:27:08'),(34,'criar','filiaisPromos','promocao','promocao, filial','','1 , 1','Usuario',5,'2026-06-28 15:27:08'),(35,'criar','usuariosFiliais','usuario','usuario, filial','','4 , 1','Usuario',2,'2026-06-28 15:32:54'),(36,'criar','usuariosFiliais','usuario','usuario, filial','','4 , 1','Usuario',2,'2026-06-28 15:32:54'),(37,'excluir','usuariosFiliais','usuario','usuario, filial','','4 , 1','Usuario',5,'2026-06-28 15:38:00'),(38,'excluir','usuariosFiliais','usuario','usuario, filial','','4 , 1','Usuario',5,'2026-06-28 15:38:00'),(39,'criar','usuariosFiliais','usuario','usuario, filial','','4 , 1','Usuario',5,'2026-06-28 15:41:00'),(40,'criar','usuariosFiliais','usuario','usuario, filial','','4 , 1','Usuario',5,'2026-06-28 15:41:00'),(41,'criar','filiaisPromos','promocao','promocao, filial','','1 , 1','Usuario',2,'2026-06-28 15:57:03'),(42,'criar','filiaisPromos','promocao','promocao, filial','','1 , 1','Usuario',2,'2026-06-28 15:57:03'),(43,'criar','filiaisPromos','promocao','promocao, filial','','1 , 1','Usuario',5,'2026-06-28 15:57:44'),(44,'criar','filiaisPromos','promocao','promocao, filial','','1 , 1','Usuario',5,'2026-06-28 15:57:44'),(45,'criar','filiaisPromos','promocao','promocao, filial','','1 , 1','Usuario',5,'2026-06-28 16:05:38'),(46,'criar','filiaisPromos','promocao','promocao, filial','','1 , 1','Usuario',5,'2026-06-28 16:05:38'),(47,'excluir','filiaisPromos','filial','filial, promocao','','1 , 1','Usuario',5,'2026-06-28 16:05:42'),(48,'excluir','filiaisPromos','filial','filial, promocao','','1 , 1','Usuario',5,'2026-06-28 16:05:42'),(49,'criar','campanhaPromos','id','id','','4','Usuario',5,'2026-06-28 16:27:57'),(50,'editar','campanhaPromos','4','validade','2026-07-15 00:00:00','2026-12-28 00:00:00','Usuario',2,'2026-06-29 00:59:11'),(51,'ativar','campanhaPromos','id','ativo','False','True','Usuario',5,'2026-06-29 01:07:07'),(52,'desativar','campanhaPromos','id','ativo','True','False','Usuario',5,'2026-06-29 01:09:24'),(53,'criar','filiaisPromos','promocao','promocao, filial','','4 , 1','Usuario',5,'2026-06-29 01:34:08'),(54,'criar','filiaisPromos','promocao','promocao, filial','','4 , 1','Usuario',5,'2026-06-29 01:34:08'),(55,'excluir','filiaisPromos','filial','filial, promocao','','1 , 4','Usuario',5,'2026-06-29 01:37:24'),(56,'excluir','filiaisPromos','filial','filial, promocao','','1 , 4','Usuario',5,'2026-06-29 01:37:24'),(57,'criar','produtos','id','id','','4','Usuario',5,'2026-06-29 01:57:20'),(58,'editar','produtos','4','nome','Cuscuz','Cuzcuz','Usuario',5,'2026-06-29 02:09:05'),(59,'editar','produtos','4','nome','Cuzcuz','Cuscuz','Usuario',5,'2026-06-29 02:11:55'),(60,'desativar','produtos','id','ativo','True','False','Usuario',7,'2026-06-29 02:24:11'),(61,'ativar','produtos','id','ativo','False','True','Usuario',5,'2026-06-29 02:24:40'),(62,'desativar','produtos','id','ativo','True','False','Usuario',7,'2026-06-29 02:27:24'),(63,'ativar','produtos','id','ativo','False','True','Usuario',5,'2026-06-29 02:27:53'),(64,'criar','ingredientes','id','id','','29','Usuario',5,'2026-06-29 02:32:04'),(65,'editar','ingredientes','29','periodo','Verão','Inverno','Usuario',5,'2026-06-29 02:44:29'),(66,'desativar','ingredientes','id','ativo','True','False','Usuario',7,'2026-06-29 02:54:04'),(67,'ativar','ingredientes','id','ativo','False','True','Usuario',7,'2026-06-29 02:55:51'),(68,'desativar','ingredientes','id','ativo','True','False','Usuario',7,'2026-06-29 02:56:40'),(69,'ativar','ingredientes','id','ativo','False','True','Usuario',7,'2026-06-29 03:00:03'),(70,'atualizar campo','ingredientes','id','periodo','PeriodoAno.INVERNO','PeriodoAno.VERAO','Usuario',5,'2026-06-29 03:03:28'),(71,'atualizar campo','ingredientes','id','periodo','PeriodoAno.VERAO','PeriodoAno.VERAO','Usuario',5,'2026-06-29 03:04:49'),(72,'atualizar campo','ingredientes','id','periodo','PeriodoAno.VERAO','PeriodoAno.VERAO','Usuario',5,'2026-06-29 03:04:54'),(73,'criar','variacoes','id','id','','7','Usuario',7,'2026-06-29 03:32:18'),(74,'editar','variacoes','7','preco_unitario','10.5','11.0','Usuario',7,'2026-06-29 03:57:04'),(75,'desativar','variacoes','id','ativo','True','False','Usuario',7,'2026-06-29 04:02:56'),(76,'ativar','variacoes','id','ativo','False','True','Usuario',7,'2026-06-29 04:03:28'),(77,'desativar','variacoes','id','ativo','True','False','Usuario',7,'2026-06-29 04:03:44'),(78,'ativar','variacoes','id','ativo','False','True','Usuario',7,'2026-06-29 04:03:48'),(79,'criar','receitasItens','variacao','variacao, ingrediente','','4 , 29','Usuario',5,'2026-06-29 04:18:35'),(80,'criar','receitasItens','variacao','variacao, ingrediente','','4 , 29','Usuario',5,'2026-06-29 04:18:35'),(81,'editar','receitasItens','4 , 29','quantidade','0.5','0.4','Usuario',5,'2026-06-29 04:23:51'),(82,'criar','receitasItens','variacao','variacao, ingrediente','','7 , 9','Usuario',5,'2026-06-29 04:27:47'),(83,'criar','receitasItens','variacao','variacao, ingrediente','','7 , 9','Usuario',5,'2026-06-29 04:27:47'),(84,'editar','receitasItens','4 , 29','quantidade, unidade_medida','0.4 , UN','0.1 , g','Usuario',5,'2026-06-29 04:28:07'),(85,'editar','receitasItens','4 , 29','quantidade, unidade_medida','0.4 , UN','0.1 , g','Usuario',5,'2026-06-29 04:28:07'),(86,'excluir','receitasItens','ingrediente','ingrediente, variacao','','9 , 7','Usuario',5,'2026-06-29 04:29:08'),(87,'excluir','receitasItens','ingrediente','ingrediente, variacao','','9 , 7','Usuario',5,'2026-06-29 04:29:08'),(88,'criar','variacoesFiliais','variacao','variacao, filial','','7 , 1','Usuario',2,'2026-06-29 04:42:47'),(89,'criar','variacoesFiliais','variacao','variacao, filial','','7 , 1','Usuario',2,'2026-06-29 04:42:47'),(90,'excluir','variacoesFiliais','variacao','variacao, filial','','7 , 1','Usuario',2,'2026-06-29 04:49:18'),(91,'excluir','variacoesFiliais','variacao','variacao, filial','','7 , 1','Usuario',2,'2026-06-29 04:49:18'),(92,'criar','receitasItens','variacao','variacao, ingrediente','','7 , 9','Usuario',5,'2026-06-29 04:56:08'),(93,'criar','receitasItens','variacao','variacao, ingrediente','','7 , 9','Usuario',5,'2026-06-29 04:56:08'),(94,'criar','receitasItens','variacao','variacao, ingrediente','','7 , 29','Usuario',5,'2026-06-29 05:10:45'),(95,'criar','receitasItens','variacao','variacao, ingrediente','','7 , 29','Usuario',5,'2026-06-29 05:10:45'),(96,'criar','estoqueItens','id','id','','1','Usuario',5,'2026-06-29 05:16:05'),(97,'editar','estoqueItens','1','quantidade','0','5','Usuario',5,'2026-06-29 05:24:40'),(98,'criar','pedidos','id','id','','1','Usuario',4,'2026-06-29 05:39:03'),(99,'criar','movimentos','id','id','','1','Usuario',7,'2026-06-29 06:18:01'),(100,'editar','movimentos','1','validade','2026-06-28 00:00:00','2026-06-28 00:00:00','Usuario',7,'2026-06-29 06:28:53'),(101,'editar','movimentos','1','validade','2026-06-28 00:00:00','2026-06-28 00:00:00','Usuario',7,'2026-06-29 06:29:07'),(102,'editar','movimentos','1','validade','2026-06-28 00:00:00','2026-06-28 00:00:00','Usuario',7,'2026-06-29 06:29:10'),(103,'editar','movimentos','1','validade','2026-06-28 00:00:00','2026-06-28 00:00:00','Usuario',7,'2026-06-29 06:29:12'),(104,'editar','movimentos','1','validade','2026-06-28 00:00:00','2026-06-28 00:00:00','Usuario',7,'2026-06-29 06:29:16'),(105,'criar','movimentoItens','id','id','','1','Usuario',7,'2026-06-29 11:44:40'),(106,'editar','movimentoItens','1','quantidade, validade','10 , 2026-12-12 00:00:00','12 , 2026-06-28 00:00:00','Usuario',7,'2026-06-29 11:59:38'),(107,'editar','movimentoItens','1','quantidade, validade','10 , 2026-12-12 00:00:00','12 , 2026-06-28 00:00:00','Usuario',7,'2026-06-29 11:59:38'),(108,'criar','movimentoItens','id','id','','2','Usuario',7,'2026-06-29 12:01:00'),(109,'criar','movimentoItens','id','id','','3','Usuario',7,'2026-06-29 12:08:42'),(110,'excluir','movimentoItens','id','id','','3','Usuario',7,'2026-06-29 12:08:54'),(111,'criar','pedidos','id','id','','2','Usuario',4,'2026-06-29 12:11:33'),(112,'editar','pedidos','2','desconto_fidelidade, tipo_modificador, id_modificador','0 , Usuario , 4','10 , Usuario , 4','Usuario',4,'2026-06-29 12:39:44'),(113,'editar','pedidos','2','desconto_fidelidade, tipo_modificador, id_modificador','0 , Usuario , 4','10 , Usuario , 4','Usuario',4,'2026-06-29 12:39:44'),(114,'editar','pedidos','2','desconto_fidelidade, tipo_modificador, id_modificador','0 , Usuario , 4','10 , Usuario , 4','Usuario',4,'2026-06-29 12:39:44'),(115,'excluir','pedidoItens','id','id','','5','Cliente',1,'2026-06-29 14:47:28'),(116,'criar','pedidoItens','id','id','','6','Cliente',1,'2026-06-29 15:04:38'),(117,'excluir','pedidoItens','id','id','','6','Cliente',1,'2026-06-29 15:05:03'),(118,'criar','pedidoItens','id','id','','7','Cliente',1,'2026-06-29 15:05:22'),(119,'editar','pedidoItens','7','quantidade','1','10','Cliente',1,'2026-06-29 15:26:08'),(120,'editar','pedidoItens','7','quantidade','1','10','Cliente',1,'2026-06-29 15:30:11'),(121,'editar','pedidoItens','7','quantidade','1','10','Cliente',1,'2026-06-29 15:38:11'),(122,'editar','pedidoItens','7','quantidade','10','5','Cliente',1,'2026-06-29 15:38:44'),(123,'excluir','pedidoItens','id','id','','7','Cliente',1,'2026-06-29 15:39:32'),(124,'criar','pedidoItens','id','id','','8','Cliente',1,'2026-06-29 15:41:19'),(125,'editar','pedidoItens','8','quantidade','10','11','Cliente',1,'2026-06-29 15:42:27'),(126,'editar','pedidoItens','8','quantidade','8','10','Cliente',1,'2026-06-29 15:49:25'),(127,'editar','pedidoItens','8','quantidade','10','11','Cliente',1,'2026-06-29 15:49:30'),(128,'editar','pedidoItens','8','quantidade','11','8','Cliente',1,'2026-06-29 16:36:57'),(129,'criar','pedidoItens','id','id','','9','Cliente',1,'2026-06-29 16:58:08'),(130,'excluir','pedidoItens','id','id','','9','Cliente',1,'2026-06-29 17:02:37'),(131,'criar','pedidoItens','id','id','','10','Cliente',1,'2026-06-29 17:02:48'),(132,'excluir','pedidoItens','id','id','','10','Cliente',1,'2026-06-29 17:07:57'),(133,'criar','pedidoItens','id','id','','11','Cliente',1,'2026-06-29 17:08:11'),(134,'excluir','pedidoItens','id','id','','11','Cliente',1,'2026-06-29 17:18:56'),(135,'criar','pedidoItens','id','id','','12','Cliente',1,'2026-06-29 17:19:01'),(136,'excluir','pedidoItens','id','id','','12','Cliente',1,'2026-06-29 17:20:03'),(137,'excluir','pedidoItens','id','id','','8','Cliente',1,'2026-06-29 17:20:28'),(138,'criar','pedidoItens','id','id','','13','Cliente',1,'2026-06-29 17:30:51'),(139,'excluir','pedidoItens','id','id','','13','Cliente',1,'2026-06-29 17:32:05'),(140,'criar','pedidoItens','id','id','','14','Cliente',1,'2026-06-29 17:33:24'),(141,'editar','pedidoItens','14','quantidade','10','8','Cliente',1,'2026-06-29 17:47:54'),(142,'criar','pedidoItens','id','id','','15','Cliente',1,'2026-06-29 18:10:09'),(143,'excluir','pedidoItens','id','id','','14','Cliente',1,'2026-06-29 18:11:03'),(144,'criar','pedidoItens','id','id','','16','Cliente',1,'2026-06-29 18:53:33');
/*!40000 ALTER TABLE `logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `movimentoItens`
--

DROP TABLE IF EXISTS `movimentoItens`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `movimentoItens` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Ingrediente` int DEFAULT NULL,
  `Movimento` int DEFAULT NULL,
  `Quantidade` int NOT NULL,
  `Validade` datetime NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `Ingrediente` (`Ingrediente`),
  KEY `Movimento` (`Movimento`),
  CONSTRAINT `movimentoItens_ibfk_1` FOREIGN KEY (`Ingrediente`) REFERENCES `ingredientes` (`ID`),
  CONSTRAINT `movimentoItens_ibfk_2` FOREIGN KEY (`Movimento`) REFERENCES `movimentos` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movimentoItens`
--

LOCK TABLES `movimentoItens` WRITE;
/*!40000 ALTER TABLE `movimentoItens` DISABLE KEYS */;
INSERT INTO `movimentoItens` VALUES (1,29,1,12,'2026-06-28 00:00:00');
/*!40000 ALTER TABLE `movimentoItens` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `movimentos`
--

DROP TABLE IF EXISTS `movimentos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `movimentos` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `DataHora` datetime NOT NULL,
  `Status` enum('Aguardando Entrega','Em Revisão','Inconsistente','Cancelado','Validado') NOT NULL,
  `Filial` int DEFAULT NULL,
  `Tipo` enum('Entrada','Saída') NOT NULL,
  `Validade` datetime NOT NULL,
  `ChaveNota` varchar(44) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `Filial` (`Filial`),
  CONSTRAINT `movimentos_ibfk_1` FOREIGN KEY (`Filial`) REFERENCES `filiais` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movimentos`
--

LOCK TABLES `movimentos` WRITE;
/*!40000 ALTER TABLE `movimentos` DISABLE KEYS */;
INSERT INTO `movimentos` VALUES (1,'2026-06-29 06:18:01','Aguardando Entrega',1,'Entrada','2026-06-28 00:00:00','');
/*!40000 ALTER TABLE `movimentos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedidoItens`
--

DROP TABLE IF EXISTS `pedidoItens`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedidoItens` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Pedido` int DEFAULT NULL,
  `Variacao` int DEFAULT NULL,
  `Quantidade` int NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `Pedido` (`Pedido`),
  KEY `Variacao` (`Variacao`),
  CONSTRAINT `pedidoItens_ibfk_1` FOREIGN KEY (`Pedido`) REFERENCES `pedidos` (`ID`),
  CONSTRAINT `pedidoItens_ibfk_2` FOREIGN KEY (`Variacao`) REFERENCES `variacoes` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedidoItens`
--

LOCK TABLES `pedidoItens` WRITE;
/*!40000 ALTER TABLE `pedidoItens` DISABLE KEYS */;
INSERT INTO `pedidoItens` VALUES (15,1,7,5),(16,2,7,5);
/*!40000 ALTER TABLE `pedidoItens` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedidos`
--

DROP TABLE IF EXISTS `pedidos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedidos` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Filial` int DEFAULT NULL,
  `Status` enum('Aberto','Fechado','Preparação','Aguardando Coleta','Em Trânsito','Cancelado','Recebido','Estornado') NOT NULL,
  `Tipo` enum('Entrega','Mesa','Retirada','Balcão') NOT NULL,
  `Canal` enum('App','Totem','Retirada','Pickup','Web') NOT NULL,
  `Criador` enum('Usuario','Cliente') NOT NULL,
  `IdCriador` int NOT NULL,
  `Cliente` int DEFAULT NULL,
  `Modificador` enum('Usuario','Cliente') NOT NULL,
  `IdModificador` int NOT NULL,
  `DataHora` datetime NOT NULL,
  `Mesa` int DEFAULT NULL,
  `Chamada` int DEFAULT NULL,
  `Endereco` varchar(80) DEFAULT NULL,
  `SomaItens` float NOT NULL,
  `Frete` float NOT NULL,
  `Total` float NOT NULL,
  `FormaPagamento` enum('Mock','Crédito','Débito') NOT NULL,
  `IdPagamento` int DEFAULT NULL,
  `StatusPagamento` enum('Aguardando Fechamento','Pendente','Cancelado','Estornado','Aprovado') DEFAULT NULL,
  `PontosFidelidade` int NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `Cliente` (`Cliente`),
  KEY `Filial` (`Filial`),
  CONSTRAINT `pedidos_ibfk_1` FOREIGN KEY (`Cliente`) REFERENCES `clientes` (`ID`),
  CONSTRAINT `pedidos_ibfk_2` FOREIGN KEY (`Filial`) REFERENCES `filiais` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedidos`
--

LOCK TABLES `pedidos` WRITE;
/*!40000 ALTER TABLE `pedidos` DISABLE KEYS */;
INSERT INTO `pedidos` VALUES (1,1,'Cancelado','Balcão','App','Usuario',4,1,'Usuario',4,'2026-06-29 05:39:03',0,0,'',55,0,55,'Mock',1,'Cancelado',0),(2,1,'Estornado','Balcão','App','Usuario',4,1,'Usuario',4,'2026-06-29 12:11:33',0,0,'',55,0,55,'Mock',NULL,'Estornado',10);
/*!40000 ALTER TABLE `pedidos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `produtos`
--

DROP TABLE IF EXISTS `produtos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `produtos` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Nome` varchar(80) NOT NULL,
  `Ativo` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produtos`
--

LOCK TABLES `produtos` WRITE;
/*!40000 ALTER TABLE `produtos` DISABLE KEYS */;
INSERT INTO `produtos` VALUES (1,'Vatapá',1),(2,'Escondidinho de charque',1),(3,'Bruaca',1),(4,'Cuscuz',1);
/*!40000 ALTER TABLE `produtos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `receitasItens`
--

DROP TABLE IF EXISTS `receitasItens`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `receitasItens` (
  `Variacao` int NOT NULL,
  `Ingredientes` int NOT NULL,
  `Quantidade` float NOT NULL,
  `UnidadeMedida` varchar(2) NOT NULL,
  PRIMARY KEY (`Variacao`,`Ingredientes`),
  KEY `Ingredientes` (`Ingredientes`),
  CONSTRAINT `receitasItens_ibfk_1` FOREIGN KEY (`Ingredientes`) REFERENCES `ingredientes` (`ID`),
  CONSTRAINT `receitasItens_ibfk_2` FOREIGN KEY (`Variacao`) REFERENCES `variacoes` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `receitasItens`
--

LOCK TABLES `receitasItens` WRITE;
/*!40000 ALTER TABLE `receitasItens` DISABLE KEYS */;
INSERT INTO `receitasItens` VALUES (1,1,500,'g'),(1,2,2,'UN'),(1,3,2,'UN'),(1,4,1,'UN'),(1,5,1,'UN'),(1,6,5,'g'),(1,7,10,'UN'),(1,8,2,'UN'),(1,9,1,'g'),(1,10,1,'UN'),(2,1,200,'g'),(2,2,4,'UN'),(2,4,300,'ml'),(2,5,200,'ml'),(2,7,10,'UN'),(2,11,150,'g'),(2,12,150,'g'),(2,13,1,'g'),(3,2,0.5,'UN'),(3,3,1,'UN'),(3,9,1,'g'),(3,14,1.5,'kg'),(3,15,360,'ml'),(3,16,30,'g'),(3,17,1,'UN'),(3,18,500,'g'),(3,19,0.5,'UN'),(3,20,1,'g'),(3,21,300,'g'),(3,22,30,'g'),(4,2,0.5,'UN'),(4,14,1,'kg'),(4,16,30,'g'),(4,17,2,'UN'),(4,18,400,'g'),(4,21,100,'g'),(4,23,2,'UN'),(4,24,2,'UN'),(4,29,0.1,'g'),(5,15,240,'ml'),(5,25,240,'ml'),(5,26,120,'ml'),(5,27,1,'ml'),(5,28,10,'g'),(6,15,360,'ml'),(6,16,5,'g'),(6,25,480,'g'),(6,26,480,'ml'),(7,9,0.5,'UN'),(7,29,0.5,'UN');
/*!40000 ALTER TABLE `receitasItens` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Nome` varchar(50) NOT NULL,
  `Email` varchar(50) NOT NULL,
  `Senha` varchar(200) NOT NULL,
  `Ativo` tinyint(1) NOT NULL,
  `Cargo` enum('Não Classificado','Gerente','Atendente','Cozinheiro','TI','CEO') NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (2,'root','root@root.com','$2b$12$0qKMOoT43MKnUf/M/6LQteOpM8u2u2GCt3WmN0LZd8HUEzKc156.S',1,'CEO'),(3,'Cozinheiro','cozinheiro@cozinheiro.com','$2b$12$FcjGVZ5HmnMJcQd9Y5OjbeqWXH8B9jIUdz0.KVWiJMFYFOLyb2Rwu',1,'Cozinheiro'),(4,'UsuAtendente','atendente@atendente.com','$2b$12$lLu66ns.Ht5C3mMRGRyXLeAvNHzmDne58sjGXbvYZirZA/rByUG2.',1,'Atendente'),(5,'Tecnologia','tecnologia@tecnologia.com','$2b$12$IjCZPuZ./tdAd3FSmCE/e.mOP8C.lHIj5KDNIpxj8eMg1ml02rXJW',1,'TI'),(6,'Não Classificado','naoclassifica@naoclassifica.com','$2b$12$Pip0rH/hDvy5OeFzt871TOACThnbWR0A9Ag3jgq5rgCYJG3icts/S',1,'Não Classificado'),(7,'UsuGerente','gerente@gerente.com','$2b$12$n6e3H5HTTuJPy5aun6mx.O5mQzO6bu0c/fVzRRwphFLsqf/tZJe5.',1,'Gerente');
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuariosFiliais`
--

DROP TABLE IF EXISTS `usuariosFiliais`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuariosFiliais` (
  `IdUsuario` int NOT NULL,
  `IdFilial` int NOT NULL,
  PRIMARY KEY (`IdUsuario`,`IdFilial`),
  KEY `IdFilial` (`IdFilial`),
  CONSTRAINT `usuariosFiliais_ibfk_1` FOREIGN KEY (`IdFilial`) REFERENCES `filiais` (`ID`),
  CONSTRAINT `usuariosFiliais_ibfk_2` FOREIGN KEY (`IdUsuario`) REFERENCES `usuarios` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuariosFiliais`
--

LOCK TABLES `usuariosFiliais` WRITE;
/*!40000 ALTER TABLE `usuariosFiliais` DISABLE KEYS */;
INSERT INTO `usuariosFiliais` VALUES (4,1);
/*!40000 ALTER TABLE `usuariosFiliais` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `variacoes`
--

DROP TABLE IF EXISTS `variacoes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `variacoes` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Nome` varchar(80) NOT NULL,
  `Produto` int DEFAULT NULL,
  `PrecoUnitario` float DEFAULT NULL,
  `Ativo` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `Produto` (`Produto`),
  CONSTRAINT `variacoes_ibfk_1` FOREIGN KEY (`Produto`) REFERENCES `produtos` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `variacoes`
--

LOCK TABLES `variacoes` WRITE;
/*!40000 ALTER TABLE `variacoes` DISABLE KEYS */;
INSERT INTO `variacoes` VALUES (1,'Vatapá de Camarão',1,15,1),(2,'Vatapá da Bahia',1,13,1),(3,'Escondidinho de charque nordestino',2,25,1),(4,'Escondidinho de charque e calabresa',2,30,1),(5,'Bruaca - Panqueca nordestina',3,4,1),(6,'Bruaca Cearense',3,5,1),(7,'Cuscuz Nordestino',4,11,1);
/*!40000 ALTER TABLE `variacoes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `variacoesFiliais`
--

DROP TABLE IF EXISTS `variacoesFiliais`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `variacoesFiliais` (
  `Variacao` int NOT NULL,
  `Filial` int NOT NULL,
  PRIMARY KEY (`Variacao`,`Filial`),
  KEY `Filial` (`Filial`),
  CONSTRAINT `variacoesFiliais_ibfk_1` FOREIGN KEY (`Filial`) REFERENCES `filiais` (`ID`),
  CONSTRAINT `variacoesFiliais_ibfk_2` FOREIGN KEY (`Variacao`) REFERENCES `variacoes` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `variacoesFiliais`
--

LOCK TABLES `variacoesFiliais` WRITE;
/*!40000 ALTER TABLE `variacoesFiliais` DISABLE KEYS */;
/*!40000 ALTER TABLE `variacoesFiliais` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'raizes_do_nordeste'
--
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-06-29 17:33:24
