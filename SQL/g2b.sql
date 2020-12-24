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


DROP TABLE IF EXISTS `HrcspSsstndrdInfoService`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `HrcspSsstndrdInfoService` (
  `oper` char(30) NOT NULL,                     -- 서비스 구분
  `bsnsDivNm` char(20) NOT NULL,                -- 업무구분명
  `refNo` char(105) NOT NULL,                   -- 참조번호
  `prdctClsfcNoNm` char(200) DEFAULT NULL,
  `orderInsttNm` char(200) DEFAULT NULL,
  `rlDminsttNm` char(200) DEFAULT NULL,
  `asignBdgtAmt` char(25) DEFAULT NULL,
  `swBizObjYn` char(1) DEFAULT NULL,
  `rcptDt` char(19) DEFAULT NULL,
  `bfSpecRgstNo` char(10) DEFAULT NULL,
  `rgstDt` char(19) DEFAULT NULL,
  `bidNtceNoList` char(500) DEFAULT NULL,
  `bidNtceDtlUrl` varchar(512) DEFAULT NULL,

  PRIMARY KEY (`bfSpecRgstNo`) USING BTREE,
  KEY `oper` (`oper`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;


DROP TABLE IF EXISTS `NotiHistoryHrcsp`;
DROP TABLE IF EXISTS `NotiHistoryBid`;
CREATE TABLE `NotiHistoryHrcsp` (
  `user` char(10) NOT NULL,
  `bfSpecRgstNo` char(10) DEFAULT NULL,
  PRIMARY KEY (`user`,`bfSpecRgstNo`)
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `NotiHistoryBid` (
  `user` char(10) NOT NULL,
  `bidNtceNo` char(40) DEFAULT NULL ,
  `bidNtceOrd` char(2) DEFAULT NULL,
  PRIMARY KEY (`user`,`bidNtceNo`,`bidNtceOrd`)
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `SearchWord`;
CREATE TABLE `SearchWord` (
  `user` char(10) NOT NULL,
  `command` char(100) DEFAULT NULL,
  PRIMARY KEY (`user`,`command`)
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


