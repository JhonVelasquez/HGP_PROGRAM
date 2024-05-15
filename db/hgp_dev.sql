CREATE TABLE "Habitacion_caracteristica" (
	"id_hab_car"	INTEGER NOT NULL UNIQUE,
	"value"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id_hab_car")
);

CREATE TABLE "Habitacion_cama" (
	"id_hab_cam"	INTEGER NOT NULL UNIQUE,
	"value"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id_hab_cam")
);

CREATE TABLE "Habitacion_estado" (
	"id_hab_est"	INTEGER NOT NULL UNIQUE,
	"value"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id_hab_est")
);

CREATE TABLE "Habitacion" (
	"id_hab"	TEXT NOT NULL UNIQUE,
	"nombre"	TEXT,
	"descripcion"	TEXT,
	"precioReferencia"	NUMERIC,
	"piso"	INTEGER NOT NULL,
	PRIMARY KEY("id_hab")
);

CREATE TABLE "Habitacion_caracteristica_join" (
	"id_hab_car_join"	INTEGER NOT NULL UNIQUE,
	"id_hab"	TEXT NOT NULL,
	"id_hab_car"	INTEGER NOT NULL,
	PRIMARY KEY("id_hab_car_join" AUTOINCREMENT),
	FOREIGN KEY("id_hab_car") REFERENCES "Habitacion_caracteristica"("id_hab_car"),
	FOREIGN KEY("id_hab") REFERENCES "Habitacion"("id_hab")
)

CREATE TABLE "Habitacion_cama_join" (
	"id_hab_cam_join"	INTEGER,
	"id_hab"	TEXT NOT NULL,
	"id_hab_cam"	INTEGER NOT NULL,
	FOREIGN KEY("id_hab") REFERENCES "Habitacion"("id_hab"),
	FOREIGN KEY("id_hab_cam") REFERENCES "Habitacion_cama"("id_hab_cam"),
	PRIMARY KEY("id_hab_cam_join")
)

CREATE TABLE "Habitaciones_registro" (
	"id_hab_reg"	INTEGER NOT NULL UNIQUE,
	"id_hab"	TEXT NOT NULL,
	"id_hab_est"	INTEGER NOT NULL,
	"fechaInicio"	TEXT NOT NULL,
	"horaInicio"	TEXT NOT NULL,
	"fechaFin"	TEXT NOT NULL,
	"horaFin"	TEXT NOT NULL,
	FOREIGN KEY("id_hab_est") REFERENCES "Habitacion_estado"("id_hab_est"),
	FOREIGN KEY("id_hab") REFERENCES "Habitacion"("id_hab"),
	PRIMARY KEY("id_hab_reg" AUTOINCREMENT)
);

CREATE TABLE "Empleado" (
	"id_emp"	INTEGER NOT NULL UNIQUE,
	"nombre"	TEXT NOT NULL,
	"apellido"	TEXT NOT NULL,
	"contrasena"	TEXT NOT NULL,
	PRIMARY KEY("id_emp")
);

CREATE TABLE "Cliente" (
	"id_cli"	INTEGER NOT NULL UNIQUE,
	"nDocumento"	TEXT UNIQUE,
	"nombre"	TEXT,
	"apellido"	TEXT,
	"datosAdicionales"	TEXT,
	"celular"	TEXT,
	PRIMARY KEY("id_cli" AUTOINCREMENT)
);

CREATE TABLE "Arquiler" (
	"id_arq"	INTEGER NOT NULL UNIQUE,
	"id_hab"	TEXT NOT NULL,
	"id_cli"	INTEGER NOT NULL,
	"precioReal"	NUMERIC NOT NULL,
	"deuda"	NUMERIC,
	"fechaChecking"	TEXT,
	"horaChecking"	TEXT,
	FOREIGN KEY("id_hab") REFERENCES "Habitacion"("id_hab"),
	FOREIGN KEY("id_cli") REFERENCES "Cliente"("id_cli"),
	PRIMARY KEY("id_arq" AUTOINCREMENT)
);



INSERT INTO Habitacion_caracteristica (id_hab_car, value)
VALUES
('1', 'agua caliente'),
('2', 'cable'),
('3', 'netflix'),
('4', 'vista de ventana'),
('5', 'internet');


INSERT INTO Habitacion_cama (id_hab_cam, value)
VALUES
('1', '1 plaza'),
('2', '1.5 plaza'),
('3', '2 plaza'),
('4', '2.5 plaza');

INSERT INTO Habitacion_estado (id_hab_est, value)
VALUES
('0', 'No disponible'),
('1', 'Libre'),
('2', 'Ocupado'),
('3', 'Reservado'),
('4', 'Solicita Limpieza'),
('5', 'Falta Limpieza'),
('6', 'Limpiando SL'),
('7', 'Limpiando FL');

INSERT INTO Habitacion (id_hab, nombre, descripcion, precioReferencia, piso)
VALUES
('21', 'Matrimonial Queen', 'Comodo y abrigado', '200', '2'),
('22', 'Matrimonial', 'Comodo y abrigado', '180', '2'),
('23', 'Estandar', 'Comodo y abrigado', '120', '2'),
('24', 'Matrimonial Queen', 'Comodo y abrigado', '200', '2'),
('25', 'Familiar (dos camas)', 'Comodo y abrigado', '210', '2'),

('31', 'Matrimonial Queen', 'Comodo y limpio', '200', '3'),
('32', 'Matrimonial', 'Comodo y limpio', '180', '3'),
('33', 'Estandar', 'Comodo y limpio', '120', '3'),
('34', 'Matrimonial Queen', 'Comodo y limpio', '200', '3'),
('35', 'Familiar (dos camas)', 'Comodo y limpio', '210', '3'),

('41', 'Matrimonial Queen', 'Comodo y limpio', '200', '4'),
('42', 'Matrimonial', 'Comodo y limpio', '180', '4'),
('43', 'Matrimonial', 'Comodo y limpio', '180', '4'),
('44', 'Matrimonial Queen', 'Comodo y limpio', '200', '4'),
('45', 'Estandar', 'Comodo y limpio', '120', '4'),
('46', 'Estandar', 'Comodo y limpio', '120', '4'),

('A', 'Matrimonial Queen', 'Comodo y limpio', '200', '5'),
('B', 'Matrimonial', 'Comodo y limpio', '180', '5'),
('C', 'Matrimonial', 'Comodo y limpio', '180', '5'),
('D', 'Matrimonial Queen', 'Comodo y limpio', '200', '5'),
('E', 'Estandar', 'Comodo y limpio', '120', '5'),
('F', 'Estandar', 'Comodo y limpio', '120', '5');

INSERT INTO Habitacion_caracteristica_join (id_hab, id_hab_car)
VALUES
(1,'21', '1'),
(2,'21', '2'),
(3,'22', '1'),
(4,'22', '3'),
(5,'23', '1'),
(6,'23', '5'),
(7,'24', '1'),
(8,'24', '4'),
(9,'25', '1'),
(10,'25', '2'),
(11,'31', '2'),
(12,'31', '5'),
(13,'32', '3'),
(14,'32', '2'),
(15,'33', '1'),
(16,'33', '2'),
(17,'34', '4'),
(18,'34', '2'),
(19,'35', '1'),
(20,'35', '2'),
(21,'41', '5'),
(22,'41', '2'),
(23,'42', '3'),
(24,'42', '2'),
(25,'43', '4'),
(26,'43', '2'),
(27,'44', '1'),
(28,'44', '3'),
(29,'45', '1'),
(30,'45', '2'),
(31,'46', '1'),
(32,'A', '2'),
(33,'A', '1'),
(34,'B', '2'),
(35,'B', '3'),
(36,'C', '2'),
(37,'C', '1'),
(38,'D', '5'),
(39,'D', '1'),
(40,'E', '2'),
(41,'E', '5'),
(42,'F', '2'),
(43,'F', '4');


INSERT INTO Habitacion_cama_join (id_hab, id_hab_cam)
VALUES
(1,'21', '1'),
(2,'21', '2'),
(3,'22', '1'),
(4,'22', '3'),
(5,'23', '1'),
(6,'23', '4'),
(7,'24', '1'),
(8,'24', '4'),
(9,'25', '1'),
(10,'25', '2'),
(11,'31', '2'),
(12,'31', '3'),
(13,'32', '3'),
(14,'32', '2'),
(15,'33', '1'),
(16,'33', '2'),
(17,'34', '4'),
(18,'34', '2'),
(19,'35', '1'),
(20,'35', '2'),
(21,'41', '3'),
(22,'41', '2'),
(23,'42', '3'),
(24,'42', '2'),
(25,'43', '4'),
(26,'43', '2'),
(27,'44', '1'),
(28,'44', '3'),
(29,'45', '1'),
(30,'45', '2'),
(31,'46', '1'),
(32,'A', '2'),
(33,'A', '1'),
(34,'B', '2'),
(35,'B', '3'),
(36,'C', '2'),
(37,'C', '1'),
(38,'D', '2'),
(39,'D', '1'),
(40,'E', '2'),
(41,'E', '3'),
(42,'F', '2'),
(43,'F', '4');

INSERT INTO Habitaciones_registro (id_hab_reg, id_hab, id_hab_est, fechaInicio, horaInicio, fechaFin, horaFin)
VALUES
('1', '22', '4', '10/01/2024', '09:00:00', '11/01/2024', '10:00:00'),
('2', '23', '4', '11/01/2024', '09:10:00', '12/01/2024', '10:10:00'),
('3', 'A', '2', '13/01/2024', '09:20:00', '14/01/2024', '10:20:00'),
('4', 'B', '5', '14/01/2024', '09:30:00', '15/01/2024', '10:30:00');

INSERT INTO Empleado (id_emp, nombre, apellido, contrasena)
VALUES
('1', 'Johan', 'Velasquez', 'hgp'),
('2', 'Ce', 'Aquino', 'hgp'),
('3', 'Lucho', 'L', 'hgp'),
('4', 'Roy', 'R', 'hgp');

INSERT INTO Cliente (id_cli, nDocumento, nombre, apellido, datosAdicionales, celular)
VALUES
('1', '6488245', 'Juan', 'Gonzales', 'Saco azul','992533675'),
('2', '4488245', 'Manuel', 'Tupac', 'Es molesto','592533675'),
('3', '2488245', 'Carlos', 'Saldanez', 'Necesita atencion especial','292533675'),
('4', '7488245', 'Alonso', 'Cerro', 'Saco rojo','192533675');

INSERT INTO Arquiler (id_arq, id_hab, id_cli, precioReal, deuda, fechaChecking, horaChecking)
VALUES
('1', '31', '1', '100', '10', '19/01/2024', '09:00:00'),
('2', '22', '3', '140', '20', '20/01/2024', '10:00:00'),
('3', 'A', '2', '120', '0', '21/01/2024', '11:00:00'),
('4', 'C', '4', '200', '12','22/01/2024', '19:00:00');


