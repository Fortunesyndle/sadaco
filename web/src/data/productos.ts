import type { ImageMetadata } from 'astro';
import fotoInstrumentacion from '../assets/fotos/producto-instrumentacion.png';
import fotoAutomatizacion from '../assets/fotos/producto-automatizacion.png';
import fotoValvulas from '../assets/fotos/producto-valvulas.png';
import fotoElectrico from '../assets/fotos/producto-electrico.png';
import fotoMecanico from '../assets/fotos/producto-mecanico.png';
import fotoMetales from '../assets/fotos/producto-metales.png';
import catalogoInstrumentacion from '../assets/fotos/catalogo-instrumentacion.jpg';
import catalogoAutomatizacion from '../assets/fotos/catalogo-automatizacion.jpg';
import catalogoValvulas from '../assets/fotos/catalogo-valvulas.jpg';
import catalogoElectrico from '../assets/fotos/catalogo-electrico.jpg';
import catalogoMecanico from '../assets/fotos/catalogo-mecanico.jpg';
import catalogoMetales from '../assets/fotos/catalogo-metales.jpg';

export interface Producto {
	slug: string;
	nombre: string;
	/** Fondo oscuro: para banners y portadas a sangre con texto blanco encima. */
	foto: ImageMetadata;
	/** Fondo gris claro de catálogo: para tarjetas. */
	catalogo: ImageMetadata;
	alt: string;
	resumen: string;
	descripcion: string;
	/** Trazo SVG en un lienzo de 24×24. */
	icono: string;
	lineas: { titulo: string; items: string[] }[];
}

export const productos: Producto[] = [
	{
		slug: 'instrumentacion',
		nombre: 'Instrumentación',
		foto: fotoInstrumentacion,
		catalogo: catalogoInstrumentacion,
		alt: 'Manómetro, transmisor de presión y transmisor de temperatura de acero inoxidable',
		resumen: 'Instrumentos de medición de presión, temperatura, nivel y caudal para procesos industriales.',
		descripcion:
			'Suministramos instrumentos de medición y sus accesorios de instalación para plantas, estaciones y facilidades de producción, seleccionados según las condiciones de proceso y la especificación técnica de cada proyecto.',
		icono: 'M12 21a8 8 0 1 0 0-16 8 8 0 0 0 0 16Zm0-8 3.5-3.5M12 3v2M4.5 13H3m18 0h-1.5',
		lineas: [
			{ titulo: 'Medición de presión', items: ['Transmisores de presión', 'Manómetros', 'Presostatos'] },
			{ titulo: 'Medición de temperatura', items: ['Transmisores de temperatura', 'Termómetros bimetálicos', 'Termopares y RTD', 'Termopozos'] },
			{ titulo: 'Nivel y caudal', items: ['Transmisores de nivel', 'Indicadores de nivel', 'Medidores de caudal'] },
			{ titulo: 'Accesorios', items: ['Manifolds', 'Tubing y conectores', 'Válvulas de instrumentación'] },
		],
	},
	{
		slug: 'automatizacion-y-control',
		nombre: 'Automatización y control',
		foto: fotoAutomatizacion,
		catalogo: catalogoAutomatizacion,
		alt: 'Controlador lógico programable con módulos, variador de frecuencia y pantalla de operador',
		resumen: 'Controladores, variadores, sensores y componentes para automatizar y controlar procesos.',
		descripcion:
			'Proveemos los componentes que integran un sistema de control, desde el sensor en campo hasta el controlador y la interfaz del operador.',
		icono: 'M9 3v3m6-3v3M9 18v3m6-3v3M3 9h3m-3 6h3m12-6h3m-3 6h3M6 6h12v12H6zM10 10h4v4h-4z',
		lineas: [
			{ titulo: 'Control', items: ['Controladores lógicos programables (PLC)', 'Controladores de proceso', 'Módulos de entrada y salida'] },
			{ titulo: 'Accionamientos', items: ['Variadores de frecuencia', 'Arrancadores suaves', 'Contactores y relés'] },
			{ titulo: 'Campo y operación', items: ['Sensores industriales', 'Interfaces de operador (HMI)', 'Actuadores'] },
		],
	},
	{
		slug: 'valvulas-y-tuberias',
		nombre: 'Válvulas, tuberías y conexiones',
		foto: fotoValvulas,
		catalogo: catalogoValvulas,
		alt: 'Válvula de bola bridada, válvula de compuerta, brida y codos de acero',
		resumen: 'Válvulas, tubería, bridas y conexiones para líneas de proceso y servicios.',
		descripcion:
			'Suministramos válvulas, tubería y conexiones en los materiales, clases de presión y normas que exige cada línea de proceso.',
		icono: 'M3 9h4v6H3zm14 0h4v6h-4zM7 12h10M12 12V6m-3 0h6',
		lineas: [
			{ titulo: 'Válvulas', items: ['Válvulas de bola', 'Válvulas de compuerta', 'Válvulas de globo', 'Válvulas de retención', 'Válvulas de alivio'] },
			{ titulo: 'Tubería y conexiones', items: ['Tubería de acero al carbono e inoxidable', 'Bridas', 'Codos, tes y reducciones', 'Empacaduras y espárragos'] },
		],
	},
	{
		slug: 'material-electrico',
		nombre: 'Material y equipos eléctricos',
		foto: fotoElectrico,
		catalogo: catalogoElectrico,
		alt: 'Rollos de cable de cobre, interruptores, caja a prueba de explosión y luminaria industrial',
		resumen: 'Conductores, protecciones, tableros e iluminación para instalaciones industriales.',
		descripcion:
			'Proveemos material y equipos eléctricos para instalaciones industriales nuevas, ampliaciones y mantenimiento, incluidos equipos para áreas clasificadas.',
		icono: 'M13 2 4 14h7l-1 8 9-12h-7l1-8Z',
		lineas: [
			{ titulo: 'Distribución', items: ['Cables y conductores', 'Tableros y centros de control de motores', 'Transformadores'] },
			{ titulo: 'Protección', items: ['Interruptores y disyuntores', 'Fusibles y protecciones', 'Sistemas de puesta a tierra'] },
			{ titulo: 'Instalación', items: ['Canalizaciones y bandejas portacables', 'Iluminación industrial', 'Equipos para áreas clasificadas'] },
		],
	},
	{
		slug: 'equipos-mecanicos',
		nombre: 'Equipos mecánicos',
		foto: fotoMecanico,
		catalogo: catalogoMecanico,
		alt: 'Bomba centrífuga acoplada a un motor eléctrico con rodamiento, sello mecánico y acople',
		resumen: 'Bombas, motores, transmisiones y repuestos para equipos rotativos.',
		descripcion:
			'Suministramos equipos mecánicos y repuestos para mantener en operación bombas, motores y sistemas de transmisión.',
		icono: 'M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6Zm7.4-1.6 1.6 1.2-2 3.4-1.9-.7a7 7 0 0 1-2.1 1.2L14.7 21h-4l-.3-2.1a7 7 0 0 1-2.1-1.2l-1.9.7-2-3.4 1.6-1.2a7 7 0 0 1 0-2.4L4.4 10.2l2-3.4 1.9.7a7 7 0 0 1 2.1-1.2L10.7 4h4l.3 2.1a7 7 0 0 1 2.1 1.2l1.9-.7 2 3.4-1.6 1.2a7 7 0 0 1 0 2.4Z',
		lineas: [
			{ titulo: 'Equipos', items: ['Bombas', 'Motores eléctricos', 'Reductores y transmisiones'] },
			{ titulo: 'Repuestos', items: ['Rodamientos', 'Sellos mecánicos', 'Acoples', 'Empaquetaduras'] },
		],
	},
	{
		slug: 'metales',
		nombre: 'Metales y aceros',
		foto: fotoMetales,
		catalogo: catalogoMetales,
		alt: 'Tubos de acero inoxidable, barras cuadradas, ángulos de aluminio y una plancha de acero',
		resumen: 'Metales ferrosos y no ferrosos en láminas, tubos, barras y perfiles.',
		descripcion:
			'Suministramos metales ferrosos y no ferrosos para fabricación, construcción y mantenimiento industrial.',
		icono: 'M3 7h18M3 17h18M8 7v10m8-10v10',
		lineas: [
			{ titulo: 'Metales ferrosos', items: ['Acero al carbono', 'Acero inoxidable', 'Aceros aleados'] },
			{ titulo: 'Metales no ferrosos', items: ['Aluminio', 'Cobre', 'Bronce'] },
			{ titulo: 'Presentaciones', items: ['Láminas y planchas', 'Tubos', 'Barras', 'Perfiles y ángulos'] },
		],
	},
];
