CREATE DATABASE  IF NOT EXISTS farmaventas;
/*se usa la base de daos*/
USE farmaventas;
DROP TABLE copid;
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