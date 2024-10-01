SELECT * FROM Programacion_cursos;
INSERT INTO Programacion_cursos(seccion, id_curso, hora_inicio, hora_final)
VALUES
	(1, '201230702', 1),
    (2, '201230702', 2),
    (1, '201231005', 3),
    (2, '201231005', 4),
    (1, '201231001', 5),
    (2, '201231001', 6);
    
SELECT 
    p.seccion,
    p.profesor,
    p.cantidad_matriculados,
    c.nombre AS nombre_curso,
    h.hora_inicio,
    h.hora_fin
FROM
    Programacion_cursos p
JOIN
    Cursos c ON p.id_curso = c.id_curso
JOIN
    Horario h ON p.id_horario = h.id_horario;