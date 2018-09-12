CREATE DATABASE  IF NOT EXISTS farmacompras;
/*se usa la base de daos*/
USE farmaventas;
-- DROP TABLE copid;
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
	fecha DATE,
	
	PRIMARY KEY(num_factura),
	
	CONSTRAINT fact_sede 
	FOREIGN KEY (sede)
	REFERENCES sedes (codigo) 
);

CREATE TABLE IF NOT EXISTS citems(
	id_item CHAR(15),
	unidad CHAR(3),
	transaccion FLOAT(13,3),
	transaccion FLOAT(13,3) DEFAULT 0
	precio_unidad FLOAT(12.2),
	descuento1 FLOAT(4,2),
	descuento2 FLOAT(4,2) DEFAULT 0,
	iva FLOAT(4,2),
	motivo_compra INT(2) DEFAULT 01,
	factura CHAR(8),
	
	PRIMARY KEY(id_item),
		
	CONSTRAINT citem_fact 
	FOREIGN KEY (factura)
	REFERENCES factura (num_factura),
	
	CONSTRAINT citem_items
	FOREIGN KEY (id_item)
	REFERENCES ITEMS (ID_ITEM) 
);
