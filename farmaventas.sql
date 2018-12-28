CREATE DATABASE  IF NOT EXISTS farmacompras;
/*se usa la base de daos*/
USE farmacompras;
-- DROP TABLE copid;

CREATE TABLE IF NOT EXISTS `items` (
  `ID_ITEM` char(6) NOT NULL,
  `ID_REFERENCIA` char(15) DEFAULT NULL,
  `DESCRIPCION` char(40) DEFAULT NULL,
  `ID_LINEA2` char(6) DEFAULT NULL,
  `ID_GRUPO2` char(6) DEFAULT NULL,
  `UNIMED_INV_1` char(3) DEFAULT NULL,
  `UNIMED_EMPAQ` char(3) DEFAULT NULL,
  `UNIMED_COM` char(3) NOT NULL,
  `FACTOR_EMPAQ` decimal(20,4) DEFAULT NULL,
  `FACTOR_COM` decimal(20,4) NOT NULL,
  `PESO` decimal(20,4) DEFAULT NULL,
  `VOLUMEN` decimal(20,4) DEFAULT NULL,
  `ULTIMO_COSTO_ED` decimal(20,4) DEFAULT NULL,
  `FECHA_INGRESO` char(8) DEFAULT NULL,
  `IVA` float(20,2) DEFAULT NULL,
  PRIMARY KEY (`ID_ITEM`),
  KEY `ID_REFERENCIA` (`ID_REFERENCIA`),
  KEY `DESCRIPCION` (`DESCRIPCION`)
) ENGINE=InnoDB DEFAULT CHARSET=LATIN1;

CREATE TABLE IF NOT EXISTS `cod_barras` (
  `ID_ITEMS` CHAR(6) NOT NULL,
  `ID_CODBAR` CHAR(15) CHARACTER SET latin1 COLLATE latin1_bin NOT NULL,
  `UNIMED_VENTA` CHAR(3) DEFAULT NULL,
  PRIMARY KEY (`ID_CODBAR`),
  KEY `BAR_ITEM` (`ID_ITEMS`),
  CONSTRAINT `BAR_ITEM` FOREIGN KEY (`ID_ITEMS`) REFERENCES `items` (`ID_ITEM`)
) ENGINE=InnoDB DEFAULT CHARSET=LATIN1;


CREATE TABLE IF NOT EXISTS copid(
	refcopi	CHAR(15) NOT NULL,
	cod_drog CHAR(5),
	fecha DATE,
	factura	CHAR(20),
	descripcion CHAR(60),
	cantidad INT(7),
	costo_desc INT(10),
	costo_full INT(10),
	iva FLOAT(4.2),
	descuento FLOAT(7,2),
	cod_barras CHAR(13),
	cod_fab CHAR(5),
	control_line INT(10),
	descuento_2 FLOAT(7,2),
	unidad CHAR(4),
	algo1 INT(10),
	algo2 INT(8),
	estado INT(1),
	
	PRIMARY KEY(refcopi)
	
)ENGINE=innoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS sedes(
	codigo CHAR(3),
	descripcion CHAR(40),
	direccion1 CHAR(40),
	direccion2 CHAR(40),
	direccion3 CHAR(40),
	grupo_co CHAR(2),
	
	PRIMARY KEY(codigo)
);

CREATE TABLE IF NOT EXISTS factura(
	num_factura CHAR(8),
	nitcomp CHAR(13) DEFAULT '860026123',
	codcomp CHAR(4),
	sede CHAR(5),
	nombre CHAR(40),
	fecha DATE,
	fecha_ingreso DATE,
	
	PRIMARY KEY(num_factura),
	
	CONSTRAINT fact_sede 
	FOREIGN KEY (sede)
	REFERENCES sedes (codigo) 
);

CREATE TABLE IF NOT EXISTS citems(
	id_item CHAR(15),
	cod_barras CHAR(15),
	factura CHAR(8),
	unidad CHAR(3),
	factor FLOAT(9,4),
	transaccion FLOAT(13,3),
	transaccion2 FLOAT(13,3) DEFAULT 0,
	precio_unidad FLOAT(12.2),
	descuento1 FLOAT(4,2),
	descuento2 FLOAT(4,2) DEFAULT 0,
	iva FLOAT(4,2),
	motivo_compra INT(2) DEFAULT 01,
	
	
	PRIMARY KEY(id_item,factura),
		
	CONSTRAINT citem_fact 
	FOREIGN KEY (factura)
	REFERENCES factura (num_factura),
	
	CONSTRAINT citem_items
	FOREIGN KEY (id_item)
	REFERENCES ITEMS (ID_ITEM) 
);
