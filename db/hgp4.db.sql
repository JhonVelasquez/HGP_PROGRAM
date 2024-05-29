BEGIN TRANSACTION;
DROP TABLE IF EXISTS "Empleado";
CREATE TABLE IF NOT EXISTS "Empleado" (
	"id"	INTEGER NOT NULL UNIQUE,
	"nombre"	TEXT NOT NULL,
	"apellido"	TEXT NOT NULL,
	"contrasena"	TEXT NOT NULL,
	PRIMARY KEY("id")
);
DROP TABLE IF EXISTS "Habitacion_cama";
CREATE TABLE IF NOT EXISTS "Habitacion_cama" (
	"id"	INTEGER NOT NULL UNIQUE,
	"value"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id")
);
DROP TABLE IF EXISTS "Habitacion_caracteristica";
CREATE TABLE IF NOT EXISTS "Habitacion_caracteristica" (
	"id"	INTEGER NOT NULL UNIQUE,
	"value"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id")
);
DROP TABLE IF EXISTS "Cliente";
CREATE TABLE IF NOT EXISTS "Cliente" (
	"id"	INTEGER NOT NULL UNIQUE,
	"nDocumento"	TEXT UNIQUE,
	"nombre"	TEXT,
	"apellido"	TEXT,
	"datosAdicionales"	TEXT,
	"celular"	TEXT,
	"lastUpdate"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "Arquiler";
CREATE TABLE IF NOT EXISTS "Arquiler" (
	"id"	INTEGER NOT NULL UNIQUE,
	"id_hab"	TEXT NOT NULL,
	"id_cli"	INTEGER NOT NULL,
	"id_emp"	INTEGER NOT NULL,
	"id_hab_reg"	INTEGER,
	"precioReal"	NUMERIC NOT NULL,
	"deuda"	NUMERIC,
	"fechaHoraChecking"	TEXT,
	"fechaHoraCheckout"	TEXT,
	"lastUpdate"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("id_hab") REFERENCES "Habitacion"("id"),
	FOREIGN KEY("id_emp") REFERENCES "Empleado"("id"),
	FOREIGN KEY("id_cli") REFERENCES "Cliente"("id"),
	FOREIGN KEY("id_hab_reg") REFERENCES "Habitaciones_registro"("id")
);
DROP TABLE IF EXISTS "Habitaciones_registro";
CREATE TABLE IF NOT EXISTS "Habitaciones_registro" (
	"id"	INTEGER NOT NULL UNIQUE,
	"id_hab"	TEXT NOT NULL,
	"id_hab_est"	INTEGER NOT NULL,
	"fechaHoraInicio"	TEXT NOT NULL,
	"fechaHoraFin"	TEXT,
	"lastUpdate"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("id_hab") REFERENCES "Habitacion"("id"),
	FOREIGN KEY("id_hab_est") REFERENCES "Habitacion_estado"("id")
);
DROP TABLE IF EXISTS "Habitacion_estado";
CREATE TABLE IF NOT EXISTS "Habitacion_estado" (
	"id"	INTEGER NOT NULL UNIQUE,
	"value"	TEXT NOT NULL UNIQUE,
	"is_in_arquiler"	TEXT,
	"is_in_hab_reg"	TEXT,
	"is_in_hab"	TEXT,
	"background"	TEXT,
	PRIMARY KEY("id")
);
DROP TABLE IF EXISTS "Habitacion";
CREATE TABLE IF NOT EXISTS "Habitacion" (
	"id"	TEXT NOT NULL UNIQUE,
	"nombre"	TEXT,
	"descripcion"	TEXT,
	"precioReferencia"	NUMERIC,
	"piso"	INTEGER NOT NULL,
	"camas"	TEXT,
	"caracteristicas"	TEXT,
	"id_permanent_state"	INTEGER,
	PRIMARY KEY("id"),
	FOREIGN KEY("id_permanent_state") REFERENCES "Habitacion_estado"("id")
);
INSERT INTO "Empleado" ("id","nombre","apellido","contrasena") VALUES (1,'Johan','Velasquez','hgp'),
 (2,'Ce','Aquino','hgp'),
 (3,'Lucho','L','hgp'),
 (4,'Roy','R','hgp'),
 (5,'General','General','hgp');
INSERT INTO "Habitacion_cama" ("id","value") VALUES (1,'1 plaza'),
 (2,'1.5 plaza'),
 (3,'2 plaza'),
 (4,'2.5 plaza');
INSERT INTO "Habitacion_caracteristica" ("id","value") VALUES (1,'agua caliente'),
 (2,'cable'),
 (3,'netflix'),
 (4,'vista de ventana'),
 (5,'internet');
INSERT INTO "Habitacion_estado" ("id","value","is_in_arquiler","is_in_hab_reg","is_in_hab","background") VALUES (0,'Inhabilitado','False','False','True','#d53e4f'),
 (1,'Disponible','False','False','True','#AACD44'),
 (2,'Ocupado','True','True','False','#fdae61'),
 (3,'Reservado','True','True','False','#abdda4'),
 (4,'SL','False','True','False','#fee08b'),
 (5,'FL','False','True','False','#f46d43'),
 (6,'Limpiando SL','False','True','False','#e6f598'),
 (7,'Limpiando FL','False','True','False','#81CDB0');
INSERT INTO "Habitacion" ("id","nombre","descripcion","precioReferencia","piso","camas","caracteristicas","id_permanent_state") VALUES ('21','Matrimonial Queen','Comodo y abrigado',2,2,'4','1,1',1),
 ('22','Matrimonial','Comodo y abrigado',180,2,'3','4',1),
 ('23','Estandar','Comodo y abrigado',12,2,'2','1,3,2',1),
 ('24','Matrimonial Queen','Comodo y abrigado',200,2,'4','1,2',1),
 ('25','Familiar (dos camas)','Comodo y abrigado',210,2,'3,4','1,3,2',1),
 ('31','Matrimonial Queen','Comodo y limpio',200,3,'4','1,2',1),
 ('32','Matrimonial','Comodo y limpio',180,3,'3','1,1',1),
 ('33','Estandar','Comodo y limpio',120,3,'2','4',1),
 ('34','Matrimonial Queen','Comodo y limpio',200,3,'4','1,3,2',1),
 ('35','Familiar (dos camas)','Comodo y limpio',210,3,'3,4','1,2',1),
 ('41','Matrimonial Queen','Comodo y limpio',200,4,'4','1,1',1),
 ('42','Matrimonial','Comodo y limpio',180,4,'3','4',1),
 ('43','Matrimonial','Comodo y limpio',180,4,'3','1,3,2',1),
 ('44','Matrimonial Queen','Comodo y limpio',200,4,'4','1,2',1),
 ('45','Estandar','Comodo y limpio',120,4,'2','1,1',1),
 ('46','Estandar','Comodo y limpio',120,4,'2','4',1),
 ('51','Matrimonial Queen','Comodo y limpio',120,5,'4','1,2',1),
 ('52','Matrimonial','Comodo y limpio',120,5,'3','1,3,2',1),
 ('53','Matrimonial','Comodo y limpio',180,5,'3','4',1),
 ('54','Matrimonial Queen','Comodo y limpio',180,5,'4','4',1),
 ('55','Estandar','Comodo y limpio',180,5,'2','1,3,2',1),
 ('56','Estandar','Comodo y limpio',180,5,'2','1,3,2',1);
COMMIT;
