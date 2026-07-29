-- Pega esto en Supabase Dashboard → SQL Editor → New query
-- Inserta 10 testimonios para la landing page

INSERT INTO testimonials (name, product, opinion, rating, active, created_at) VALUES
('Carlos Marcano', 'Uniforme de fútbol personalizado', 'Mandé a hacer los uniformes para todo el equipo y quedaron espectaculares. La sublimación de primera, los colores bien vibrantes. Recomendados totalmente.', 5, true, NOW()),
('María Velásquez', 'Conjunto deportivo', 'Pedí un conjunto para entrenar y me encantó. La tela es súper fresca, ideal para el calor de la isla. El delivery llegó rapidísimo a mi casa.', 5, true, NOW() - INTERVAL '1 minute'),
('José Marcano', 'Camisa personalizada', 'Mandé a personalizar unas camisas para mi negocio y el trabajo quedó impecable. Los detalles bien cuidados y la atención excelente. Volveré a pedir sin duda.', 5, true, NOW() - INTERVAL '2 minutes'),
('Andreína Gil', 'Short y top deportivo', 'Me hice un conjunto short-top para el gym y me quedó perfecto. La tela es de buena calidad y la personalización quedó tal cual lo pedí por WhatsApp. Súper recomendadas.', 5, true, NOW() - INTERVAL '3 minutes'),
('Luis Salazar', 'Uniforme de béisbol', 'Pedimos los uniformes para el equipo de béisbol infantil y todos quedaron felices. Buenos materiales, bien cosidos y los números y nombres quedaron perfectos. Excelente.', 5, true, NOW() - INTERVAL '4 minutes'),
('Rosmary Guzmán', 'Suéter personalizado', 'Encargué un suéter con un diseño especial y me llegó antes de lo esperado. La calidad es buenísima, no ha perdido el color después de varios lavados. Muy contenta.', 5, true, NOW() - INTERVAL '5 minutes'),
('Jesús Romero', 'Shorts de entrenamiento', 'Buenísimos los shorts, frescos y cómodos. Los uso para correr en la playa y aguantan bien el sol y la arena. Precio justo y buena atención.', 5, true, NOW() - INTERVAL '6 minutes'),
('Yulianny León', 'Conjunto deportivo personalizado', 'Me encantó todo el proceso. Mandé las referencias por WhatsApp y en días tenía mi conjunto listo. Quedó idéntico a lo que quería. La mejor tienda de la isla.', 5, true, NOW() - INTERVAL '7 minutes'),
('Ángel Salazar', 'Uniforme de fútbol sala', 'Hice el pedido de los uniformes para el equipo del barrio y todos quedaron contentísimos. Buena calidad, buenos precios y el diseño quedó brutal. Full recomendados.', 5, true, NOW() - INTERVAL '8 minutes'),
('Génesis Mata', 'Accesorios personalizados', 'Pedí gorras y mochilas con el logo de mi emprendimiento y el trabajo quedó súper profesional. La atención al cliente excelente, me asesoraron en todo. 10/10.', 5, true, NOW() - INTERVAL '9 minutes');

-- Verificar: debe mostrar 10 filas
SELECT id, name, product, rating, active FROM testimonials ORDER BY id;
