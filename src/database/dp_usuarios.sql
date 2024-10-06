SELECT * FROM usuarios;
INSERT INTO Usuarios(codigo, dni, nombre, apellido, correo, contra, rol) 
VALUES 
	('11111111','23200000','Jean','Huanacuni Gomez','jean.huanacuni@unmsm.edu.pe','password123', 'administrador'),
	('11111112','23200001','Jose','Pereda Carranza','jose.pereda@unmsm.edu.pe', 'password123', 'administrador'),
	('11111113','23200002','Miguel Angel','Sanchez Osorio','miguel.sanchezo@unmsm.edu.pe','password123', 'administrador'),
	('11111114','23200003','Renzo','Ccente Alfonso ','renzo.ccente@unmsm.edu.pe','password123', 'administrador');

SHOW CREATE TABLE Usuarios;


