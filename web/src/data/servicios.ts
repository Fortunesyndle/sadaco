import type { ImageMetadata } from 'astro';
import fotoProcura from '../assets/fotos/servicio-procura.png';
import fotoIngenieria from '../assets/fotos/servicio-ingenieria.png';
import fotoProyectos from '../assets/fotos/servicio-proyectos.png';
import fotoAsistencia from '../assets/fotos/servicio-asistencia.png';
import fotoPersonal from '../assets/fotos/servicio-personal.png';

export interface Servicio {
	slug: string;
	titulo: string;
	foto: ImageMetadata;
	alt: string;
	resumen: string;
	descripcion: string;
	incluye: string[];
	etapas?: { titulo: string; texto: string }[];
}

export const servicios: Servicio[] = [
	{
		slug: 'procura-y-suministro',
		titulo: 'Procura y suministro',
		foto: fotoProcura,
		alt: 'Montacargas cargando equipos industriales en un camión frente a un almacén con tuberías y válvulas',
		resumen: 'Equipos y materiales para el sector industrial, con movilización y traslado hasta su operación.',
		descripcion:
			'Gestionamos la procura y el suministro de equipos y materiales especializados de marcas reconocidas en el mercado nacional e internacional. Nos encargamos también de la movilización y el traslado, para que cada pedido llegue completo y a tiempo al sitio donde se necesita.',
		incluye: [
			'Equipos y materiales de instrumentación, automatización y control',
			'Equipos y materiales mecánicos y eléctricos',
			'Selección de proveedores y marcas según la especificación técnica',
			'Seguimiento del pedido desde la orden hasta la entrega',
			'Movilización y traslado al sitio de operación',
		],
	},
	{
		slug: 'ingenieria-instrumentacion-y-control',
		titulo: 'Ingeniería, instrumentación y control',
		foto: fotoIngenieria,
		alt: 'Ingeniero con casco midiendo con un multímetro en un tablero de control industrial',
		resumen: 'Soluciones integrales de ingeniería, instrumentación, control y servicios industriales especializados.',
		descripcion:
			'Desarrollamos soluciones de ingeniería en las áreas de instrumentación, automatización, sistemas de control, mecánica y electricidad. Cada solución se diseña según los requerimientos técnicos de la instalación y bajo criterios alineados con normativas nacionales e internacionales.',
		incluye: [
			'Ingeniería de instrumentación y sistemas de control',
			'Automatización de procesos industriales',
			'Ingeniería mecánica y eléctrica',
			'Mantenimiento de equipos e instalaciones',
			'Servicios industriales especializados',
		],
	},
	{
		slug: 'proyectos-integrales',
		titulo: 'Proyectos integrales',
		foto: fotoProyectos,
		alt: 'Grúa izando un módulo de acero en la construcción de un rack de tuberías industrial',
		resumen: 'Desarrollo y ejecución de proyectos, desde la ingeniería de detalle hasta la construcción y la puesta en marcha.',
		descripcion:
			'Asumimos proyectos completos con una sola coordinación. Combinamos planificación, procura y conocimiento técnico para actuar de forma ordenada en cada etapa y entregar una instalación lista para operar.',
		incluye: [
			'Planificación y control del proyecto',
			'Ingeniería de detalle',
			'Procura de equipos y materiales',
			'Construcción y montaje',
			'Pruebas y puesta en marcha',
		],
		etapas: [
			{ titulo: 'Ingeniería de detalle', texto: 'Definimos el alcance, los planos y las especificaciones de cada componente.' },
			{ titulo: 'Procura', texto: 'Adquirimos y trasladamos los equipos y materiales especificados.' },
			{ titulo: 'Construcción', texto: 'Ejecutamos la obra y el montaje con planes de control y seguridad industrial.' },
			{ titulo: 'Puesta en marcha', texto: 'Probamos la instalación y la entregamos en operación.' },
		],
	},
	{
		slug: 'asistencia-tecnica',
		titulo: 'Asistencia técnica',
		foto: fotoAsistencia,
		alt: 'Dos ingenieros revisando planos técnicos junto a una laptop con una planta industrial de fondo',
		resumen: 'Acompañamiento técnico en la elaboración de proyectos, desde el alcance hasta las especificaciones.',
		descripcion:
			'Apoyamos a su equipo en la elaboración de proyectos con criterio técnico y experiencia operativa, para que cada decisión responda a las condiciones reales de la instalación.',
		incluye: [
			'Revisión del alcance y de los requerimientos técnicos',
			'Apoyo en especificaciones de equipos y materiales',
			'Evaluación de alternativas técnicas',
			'Acompañamiento durante la ejecución',
		],
	},
	{
		slug: 'personal-especializado',
		titulo: 'Personal especializado',
		foto: fotoPersonal,
		alt: 'Equipo de ingenieros y técnicos con casco y braga azul en una instalación petrolera',
		resumen: 'Personal profesional y técnico altamente calificado en ingeniería y gestión de proyectos.',
		descripcion:
			'Suministramos personal profesional, técnico y especializado para reforzar a su equipo durante un proyecto o una operación, con la formación y la experiencia que exigen los sectores petrolero y petroquímico.',
		incluye: [
			'Ingenieros de proyecto y de especialidad',
			'Personal técnico de instrumentación, control, mecánica y electricidad',
			'Gestión y control de proyectos',
			'Integración a esquemas de trabajo del cliente',
		],
	},
];
