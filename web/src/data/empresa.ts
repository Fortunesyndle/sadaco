// Los campos en null no se muestran en el sitio hasta que se completen.
export const empresa = {
	nombre: 'SADACO C.A.',
	lema: 'Servicios y suministros',
	direccion: 'Carretera L, entre 34 y 41, Residencias Gira Luna, Planta Baja',
	ciudad: 'Ciudad Ojeda, estado Zulia, Venezuela',
	mapa: 'https://www.openstreetmap.org/?mlat=10.2&mlon=-71.31#map=14/10.2/-71.31',
	// Marcadores: reemplazar por los datos reales antes de publicar.
	telefono: '+58 265 000 0000' as string | null,
	whatsapp: null as string | null,
	correo: 'contacto@ejemplo.com' as string | null,
	rif: 'J-00000000-0' as string | null,
	horario: 'Lunes a viernes, 8:00 a. m. a 5:00 p. m.',
	internacional: 'https://www.sadacointernational.com/',
};

export const whatsappUrl = empresa.whatsapp
	? `https://wa.me/${empresa.whatsapp.replace(/\D/g, '')}`
	: null;

export const contactoDirecto = [
	...(whatsappUrl ? [{ texto: 'WhatsApp', href: whatsappUrl, externo: true }] : []),
	...(empresa.telefono ? [{ texto: empresa.telefono, href: `tel:${empresa.telefono.replace(/\s/g, '')}` }] : []),
	...(empresa.correo ? [{ texto: empresa.correo, href: `mailto:${empresa.correo}` }] : []),
];

export const especialidades = [
	'Instrumentación',
	'Automatización',
	'Sistemas de control',
	'Mecánica',
	'Electricidad',
];

// Lo que distingue a la empresa, según su presentación corporativa. Cada pilar lleva su foto en Pilares.astro.
export const pilares = [
	{
		titulo: 'Experiencia en la industria',
		texto: 'Una sólida trayectoria y capacidades técnicas de alto nivel para los sectores más exigentes, con un enfoque orientado a resultados que asegura la continuidad y la eficiencia de sus operaciones.',
	},
	{
		titulo: 'Calidad y seguridad industrial',
		texto: 'Planes de control, buenas prácticas y criterios alineados con normativas nacionales e internacionales, para ejecutar cada operación de forma segura y resguardar al personal, los procesos y los activos.',
	},
	{
		titulo: 'Enfoque integral',
		texto: 'Planificación, procura, suministro y conocimiento técnico coordinados en todas las etapas, para entender el alcance completo de cada desafío y responder a lo que su proyecto necesita.',
	},
	{
		titulo: 'Flexibilidad contractual',
		texto: 'Participamos bajo distintos esquemas de asistencia y contratación, y nos integramos con eficiencia a proyectos de diversa magnitud y complejidad.',
	},
];

// icono: trazo SVG en un lienzo de 24×24.
export const razones = [
	{
		titulo: 'Marcas reconocidas',
		texto: 'Equipos y materiales de fabricantes con respaldo en el mercado nacional e internacional.',
		icono: 'M12 15a6 6 0 1 0 0-12 6 6 0 0 0 0 12Zm-3.5 4.5L12 17l3.5 2.5-1-5.8m-5 0-1 5.8M12 6.5l1 2 2.2.3-1.6 1.5.4 2.2-2-1-2 1 .4-2.2-1.6-1.5 2.2-.3 1-2Z',
	},
	{
		titulo: 'Personal calificado',
		texto: 'Profesionales y técnicos especializados en ingeniería y gestión de proyectos, listos para integrarse a su operación.',
		icono: 'M12 12a3 3 0 1 0 0-6 3 3 0 0 0 0 6Zm-6 8a6 6 0 0 1 12 0M5 9.5a2 2 0 1 0 0-4m14 4a2 2 0 1 1 0-4M2 17a4 4 0 0 1 3-3.9M22 17a4 4 0 0 0-3-3.9',
	},
	{
		titulo: 'Movilización y traslado',
		texto: 'Nos encargamos de llevar cada pedido completo hasta el sitio donde se necesita.',
		icono: 'M3 6.5h11v9H3zm11 3h4l3 3v3h-7M7 18.5a2 2 0 1 0 0-4 2 2 0 0 0 0 4Zm10 0a2 2 0 1 0 0-4 2 2 0 0 0 0 4Z',
	},
	{
		titulo: 'Cobertura nacional',
		texto: 'Desde el Zulia atendemos proyectos de diversa complejidad en todo el territorio venezolano.',
		icono: 'M12 21s-7-6.1-7-11.5a7 7 0 0 1 14 0C19 14.9 12 21 12 21Zm0-8.5a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z',
	},
];

// Del enfoque integral: de la planificación a la puesta en marcha.
export const etapas = [
	{ titulo: 'Planificación', texto: 'Entendemos el alcance completo del requerimiento y definimos cómo abordarlo.' },
	{ titulo: 'Procura y suministro', texto: 'Gestionamos equipos y materiales de marcas reconocidas, con movilización hasta el sitio.' },
	{ titulo: 'Ingeniería y construcción', texto: 'Desarrollamos la ingeniería de detalle y ejecutamos la obra con personal calificado.' },
	{ titulo: 'Puesta en marcha', texto: 'Acompañamos el arranque para asegurar la continuidad operativa desde el primer día.' },
];

export const sectores = [
	{
		nombre: 'Petrolero',
		texto: 'Suministro y servicios para operaciones de producción, mantenimiento y nuevas instalaciones.',
	},
	{
		nombre: 'Petroquímico',
		texto: 'Equipos, materiales e instrumentación para procesos que exigen control y confiabilidad.',
	},
	{
		nombre: 'Industria pública y privada',
		texto: 'Soluciones para plantas y empresas de todo el país, con la misma exigencia técnica.',
	},
];
