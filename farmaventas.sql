CREATE DATABASE  IF NOT EXISTS farmaventas;
/*se usa la base de daos*/
USE farmaventas;

CREATE TABLE IF NOT EXISTS copid(
	id_copid INT(10) NOT NULL AUTO_INCREMENT,
	cod_drog INT(5),
	fecha DATE,
	factura	INT(20),
	refcopi	INT(15),
	descripcion CHAR(60),
	cod_barras INT(13)
	cantidad INT(7),
	costo_desc INT(10),
	costo_full INT(10),
	iva FLOAT(4.2),
	DESCUENTO FLOAT(7,2),
	cod_fab CHAR(5),
	unidad CHAR(4),
	algo1 INT(10),
	algo2 INT(8),
	
	PRIMARY KEY(id_copi)
	
)ENGINE=innoDB DEFAULT CHARSET=latin1;