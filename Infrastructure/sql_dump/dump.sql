-- MySQL dump 10.13  Distrib 8.0.46, for Linux (x86_64)
--
-- Host: localhost    Database: raizes_do_nordeste
-- ------------------------------------------------------
-- Server version	8.0.46-0ubuntu0.24.04.2

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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `campanhaPromos`
--

LOCK TABLES `campanhaPromos` WRITE;
/*!40000 ALTER TABLE `campanhaPromos` DISABLE KEYS */;
INSERT INTO `campanhaPromos` VALUES (1,'Festão Nordestino',10,'2026-07-30 00:00:00',1),(2,'Aniversário Raízes do Nordeste',5,'2026-03-30 00:00:00',1),(3,'Carnaval Raiz',8,'2026-02-05 00:00:00',1);
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clientes`
--

LOCK TABLES `clientes` WRITE;
/*!40000 ALTER TABLE `clientes` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estoqueItens`
--

LOCK TABLES `estoqueItens` WRITE;
/*!40000 ALTER TABLE `estoqueItens` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estoques`
--

LOCK TABLES `estoques` WRITE;
/*!40000 ALTER TABLE `estoques` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `filiais`
--

LOCK TABLES `filiais` WRITE;
/*!40000 ALTER TABLE `filiais` DISABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ingredientes`
--

LOCK TABLES `ingredientes` WRITE;
/*!40000 ALTER TABLE `ingredientes` DISABLE KEYS */;
INSERT INTO `ingredientes` VALUES (1,'Camarão','Verão',1),(2,'Cebola','Verão',1),(3,'Tomate','Verão',1),(4,'Leite de coco','Verão',1),(5,'Azeite de dendê','Verão',1),(6,'Cheiro Verde','Verão',1),(7,'Pão','Verão',1),(8,'Pimenta cheirosa','Verão',1),(9,'Sal','Verão',1),(10,'Pimenta malagueta','Verão',1),(11,'Castanha de caju','Verão',1),(12,'Amendoim','Verão',1),(13,'Gengibre','Verão',1),(14,'Macaxeira','Verão',1),(15,'Leite','Verão',1),(16,'Manteiga','Verão',1),(17,'Creme de Leite','Verão',1),(18,'Charque','Verão',1),(19,'Pimentão Verde','Verão',1),(20,'Coentro','Verão',1),(21,'Queijo Mussarela','Verão',1),(22,'Queijo Parmesão','Verão',1),(23,'Alho','Verão',1),(24,'Calabresa','Verão',1),(25,'Farinha de trigo','Verão',1),(26,'Açúcar','Verão',1),(27,'Essência de Baunilha','Verão',1),(28,'Fermento químico','Verão',1);
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logs`
--

LOCK TABLES `logs` WRITE;
/*!40000 ALTER TABLE `logs` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movimentoItens`
--

LOCK TABLES `movimentoItens` WRITE;
/*!40000 ALTER TABLE `movimentoItens` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movimentos`
--

LOCK TABLES `movimentos` WRITE;
/*!40000 ALTER TABLE `movimentos` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedidoItens`
--

LOCK TABLES `pedidoItens` WRITE;
/*!40000 ALTER TABLE `pedidoItens` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedidos`
--

LOCK TABLES `pedidos` WRITE;
/*!40000 ALTER TABLE `pedidos` DISABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produtos`
--

LOCK TABLES `produtos` WRITE;
/*!40000 ALTER TABLE `produtos` DISABLE KEYS */;
INSERT INTO `produtos` VALUES (1,'Vatapá',1),(2,'Escondidinho de charque',1),(3,'Bruaca',1);
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
INSERT INTO `receitasItens` VALUES (1,1,500,'g'),(1,2,2,'UN'),(1,3,2,'UN'),(1,4,1,'UN'),(1,5,1,'UN'),(1,6,5,'g'),(1,7,10,'UN'),(1,8,2,'UN'),(1,9,1,'g'),(1,10,1,'UN'),(2,1,200,'g'),(2,2,4,'UN'),(2,4,300,'ml'),(2,5,200,'ml'),(2,7,10,'UN'),(2,11,150,'g'),(2,12,150,'g'),(2,13,1,'g'),(3,2,0.5,'UN'),(3,3,1,'UN'),(3,9,1,'g'),(3,14,1.5,'kg'),(3,15,360,'ml'),(3,16,30,'g'),(3,17,1,'UN'),(3,18,500,'g'),(3,19,0.5,'UN'),(3,20,1,'g'),(3,21,300,'g'),(3,22,30,'g'),(4,2,0.5,'UN'),(4,14,1,'kg'),(4,16,30,'g'),(4,17,2,'UN'),(4,18,400,'g'),(4,21,100,'g'),(4,23,2,'UN'),(4,24,2,'UN'),(5,15,240,'ml'),(5,25,240,'ml'),(5,26,120,'ml'),(5,27,1,'ml'),(5,28,10,'g'),(6,15,360,'ml'),(6,16,5,'g'),(6,25,480,'g'),(6,26,480,'ml');
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `variacoes`
--

LOCK TABLES `variacoes` WRITE;
/*!40000 ALTER TABLE `variacoes` DISABLE KEYS */;
INSERT INTO `variacoes` VALUES (1,'Vatapá de Camarão',1,15,1),(2,'Vatapá da Bahia',1,13,1),(3,'Escondidinho de charque nordestino',2,25,1),(4,'Escondidinho de charque e calabresa',2,30,1),(5,'Bruaca - Panqueca nordestina',3,4,1),(6,'Bruaca Cearense',3,5,1);
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
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-06-27 18:10:19
