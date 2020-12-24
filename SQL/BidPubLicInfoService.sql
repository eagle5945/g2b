DROP TABLE IF EXISTS `BidPublicInfoService`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `BidPublicInfoService` (
  `oper` char(30) NOT NULL,
  `bidNtceNo` char(40) NOT NULL,
  `bidNtceOrd` char(2) NOT NULL,
  `bidNtceNm` char(100) DEFAULT NULL,
  `ntceInsttNm` char(200) DEFAULT NULL,
  `dminsttNm` char(200) DEFAULT NULL,
  `asignBdgtAmt` char(25) DEFAULT NULL,
  `infoBizYn` char(1) DEFAULT NULL,
  `bidNtceDt` char(19) DEFAULT NULL,
  `bidBeginDt` char(19) DEFAULT NULL,
  `bidClseDt` char(19) DEFAULT NULL,
  `rgstDt` char(19) DEFAULT NULL,
  `bidNtceDtlUrl` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`bidNtceNo`,`bidNtceOrd`) USING BTREE,
  KEY `oper` (`oper`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

