---
name: SADACO Venezuela
description: Sede venezolana de SADACO International. Sistema espejo del sitio sadacointernational.com (Webflow, 2022), adaptado al español y al contenido local.
colors:
  tinta: "#090b19"
  negro: "#0d0d0d"
  blanco: "#ffffff"
  niebla: "#f3f6fc"
  contorno: "#e2e7f1"
  pizarra: "#6e7488"
  foco-campo: "#d4ddee"
  logo-azul: "#004aad"
  logo-verde: "#7ed957"
  logo-rojo: "#cf142b"
typography:
  display:
    fontFamily: "Inter, sans-serif"
    fontSize: "78px"
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "-0.05em"
  headline:
    fontFamily: "Inter, sans-serif"
    fontSize: "48px"
    fontWeight: 600
    lineHeight: 1.15
    letterSpacing: "-0.03em"
  title-lg:
    fontFamily: "Inter, sans-serif"
    fontSize: "32px"
    fontWeight: 700
    lineHeight: 1.25
  title:
    fontFamily: "Inter, sans-serif"
    fontSize: "24px"
    fontWeight: 700
    lineHeight: 1.25
    letterSpacing: "-0.03em"
  title-sm:
    fontFamily: "Inter, sans-serif"
    fontSize: "18px"
    fontWeight: 700
    lineHeight: 1.33
  list:
    fontFamily: "Inter, sans-serif"
    fontSize: "18px"
    fontWeight: 400
    lineHeight: 1.25
    letterSpacing: "-0.03em"
  body-lg:
    fontFamily: "Open Sans, sans-serif"
    fontSize: "18px"
    fontWeight: 400
    lineHeight: 1.6
  body:
    fontFamily: "Open Sans, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.6
  label:
    fontFamily: "Inter, sans-serif"
    fontSize: "12px"
    fontWeight: 400
    lineHeight: 1.25
    letterSpacing: "4px"
  nav:
    fontFamily: "Inter, sans-serif"
    fontSize: "14px"
    fontWeight: 400
    lineHeight: 1.25
    letterSpacing: "3px"
  button:
    fontFamily: "Inter, sans-serif"
    fontSize: "11px"
    fontWeight: 400
    lineHeight: 1.25
    letterSpacing: "3px"
rounded:
  recto: "0px"
  campo: "2px"
  pildora: "100px"
  circulo: "50%"
spacing:
  "6": "6px"
  "9": "9px"
  "12": "12px"
  "18": "18px"
  "24": "24px"
  "36": "36px"
  "48": "48px"
  "60": "60px"
  "80": "80px"
  "120": "120px"
  "160": "160px"
  "240": "240px"
components:
  button-primary:
    backgroundColor: "{colors.tinta}"
    textColor: "{colors.blanco}"
    typography: "{typography.button}"
    rounded: "{rounded.pildora}"
    padding: "16px 28px"
  button-primary-hover:
    backgroundColor: "{colors.contorno}"
    textColor: "{colors.tinta}"
  button-small:
    typography: "{typography.button}"
    rounded: "{rounded.pildora}"
    padding: "9px 18px"
  button-outline-light:
    backgroundColor: "transparent"
    textColor: "{colors.blanco}"
    rounded: "{rounded.pildora}"
    padding: "16px 28px"
  button-outline-light-hover:
    backgroundColor: "{colors.tinta}"
    textColor: "{colors.blanco}"
  button-outline:
    backgroundColor: "transparent"
    textColor: "{colors.tinta}"
    rounded: "{rounded.pildora}"
    padding: "9px 18px"
  button-outline-hover:
    backgroundColor: "{colors.tinta}"
    textColor: "{colors.blanco}"
  button-solid-white:
    backgroundColor: "{colors.blanco}"
    textColor: "{colors.tinta}"
    rounded: "{rounded.pildora}"
    padding: "16px 28px"
  button-solid-white-hover:
    backgroundColor: "{colors.contorno}"
  submit:
    backgroundColor: "{colors.tinta}"
    textColor: "{colors.blanco}"
    rounded: "{rounded.pildora}"
    padding: "16px 32px"
    width: "160px"
  input-field:
    backgroundColor: "#ffffffa6"
    textColor: "{colors.tinta}"
    typography: "{typography.body}"
    rounded: "{rounded.campo}"
    padding: "18px"
    height: "54px"
  navbar:
    backgroundColor: "{colors.blanco}"
    height: "75px"
  list-item:
    textColor: "{colors.pizarra}"
    typography: "{typography.list}"
    padding: "24px"
  list-item-hover:
    textColor: "{colors.tinta}"
  panel-niebla:
    backgroundColor: "{colors.niebla}"
    padding: "60px 48px"
  card-servicio:
    backgroundColor: "{colors.blanco}"
    rounded: "{rounded.recto}"
    padding: "36px"
  hover-link:
    textColor: "{colors.blanco}"
    rounded: "{rounded.circulo}"
    size: "148px"
  footer:
    backgroundColor: "{colors.tinta}"
    textColor: "{colors.blanco}"
---

# Design System: SADACO Venezuela

## Overview

**Creative North Star: "La Retícula del Puerto"**

SADACO Venezuela es una sede de SADACO International, no una marca aparte. Por eso este sistema copia el lenguaje visual de [sadacointernational.com](https://www.sadacointernational.com/): el mismo sitio Webflow, sus mismas proporciones, curvas de movimiento y reglas de color. Solo cambian el idioma (español), el contenido (soluciones y productos de la sede) y el logo (el globo con laureles de International, con Venezuela en rojo). Si una decisión no está descrita aquí, la respuesta correcta es "lo que haga International".

La metáfora es un plano de muelle. Una retícula de tres columnas queda **visible** como líneas verticales de 1px que recorren toda la página, incluso sobre las fotos. El contenido se amarra a esas líneas: encabezados en la primera columna, botones en la tercera y paneles pálidos que ocupan dos tercios. La interfaz es casi monocromática (tinta casi negra, blanco y un gris azulado muy tenue). Las fotos grandes van en blanco y negro con un velo de tinta, y el único color de marca de toda la página es el logo.

El movimiento es la personalidad del sitio. Casi todo entra "desde debajo de una máscara": el texto sube desde un recorte con una ligera inclinación que se endereza, con curvas exponenciales largas (1,3 a 1,6 s). Los botones y enlaces circulares siguen al cursor como un imán. Las tarjetas se llenan con un círculo que crece desde la esquina. El efecto es sobrio pero caro, como una firma de comercio internacional.

**Key Characteristics:**
- Retícula de 3 columnas con líneas verticales visibles (1px) en toda la página.
- Monocromo: tinta `#090b19`, blanco y niebla `#f3f6fc`. El color vive solo en el logo.
- Fotos de fondo desaturadas con velo de tinta; fotos pequeñas a color y de estudio.
- Títulos Inter semibold con tracking negativo, frases cortas que terminan en punto.
- Etiquetas y botones en mayúsculas con tracking muy abierto (3–4px).
- Formas binarias: rectángulos de esquina viva o píldoras y círculos perfectos. Nada intermedio.
- Plano, sin sombras. La profundidad sale de velos, escalas y cortinas.
- Entradas con máscara, inclinación y curvas `inOutExpo` largas; hovers magnéticos.

## Colors

Paleta de tinta sobre papel frío: un casi negro azulado, blanco y dos grises azulados muy claros. No hay colores de acento en la interfaz.

### Primary
- **Tinta Noche** (`tinta`): texto principal, botón sólido, fondo del footer, fondo del menú al pasar el cursor y color base de todos los velos sobre fotos. Es el "negro" del sistema; nunca se usa `#000`.

### Neutral
- **Blanco Papel** (`blanco`): fondo de página, caja del logo en la barra de navegación, texto sobre fotos y sobre el footer.
- **Niebla** (`niebla`): el color de las líneas de retícula sobre blanco, y el fondo de todos los paneles pálidos (aliados, formulario de contacto, megamenú, cinta informativa). También es el círculo que llena las tarjetas al pasar el cursor.
- **Contorno** (`contorno`): bordes de botones con contorno, líneas horizontales, borde de campos, separadores del megamenú y fondo del botón sólido al pasar el cursor.
- **Pizarra** (`pizarra`): texto de párrafos (`body`), ítems de lista en reposo y logos de aliados. Contraste de 4.7:1 sobre blanco; sobre niebla baja a ~4.4:1, así que ahí se usa solo en 16px o más.
- **Foco de Campo** (`foco-campo`): borde de un campo de formulario con foco.
- **Negro Profundo** (`negro`): reservado; International lo define pero casi no lo usa.

### Colores del logo (solo dentro del logo)
- **Azul Globo** (`logo-azul`), **Verde Continente** (`logo-verde`) y **Rojo Venezuela** (`logo-rojo`) son los colores del emblema: globo azul con continentes verdes, laureles azules y Venezuela en rojo. Aparecen únicamente en el archivo del logo y en el favicon.

### Transparencias de tinta y blanco
Los velos y líneas se construyen siempre con tinta o blanco más una transparencia, nunca con otros colores:
- Velo claro sobre retratos: tinta al 15%.
- Velo normal sobre fotos de portada y banners: tinta al 30%.
- Velo oscuro en portadas internas y en la sección de cita: tinta al 45%.
- Fondo del megamenú y galerías: tinta al 50%.
- Líneas de retícula sobre fotos y sobre el footer: blanco al 12%. Separadores de lista en el footer: blanco al 15%.
- Borde del botón de contorno claro: blanco al 75%. Texto de párrafo sobre oscuro: blanco al 90%.

### Named Rules
**The Logo Is The Only Color Rule.** La interfaz es monocroma. Azul, verde y rojo existen solo dentro del emblema. No hay botones azules, íconos verdes ni acentos rojos. Si algo necesita destacar, se hace con tamaño, con tinta sólida o con un velo, nunca con color.

**The Veil Rule.** Toda foto a sangre lleva encima un velo de tinta (15, 30 o 45%). El texto blanco nunca va directamente sobre una foto sin velo.

## Typography

**Fuente de títulos e interfaz:** Inter (300–700), con respaldo `sans-serif`.
**Fuente de párrafos:** Open Sans (300–800), con respaldo `sans-serif`.

**Character:** Inter en semibold, con el tracking cerrado, da titulares compactos y corporativos. Open Sans en gris pizarra baja la voz en los párrafos. Las etiquetas en mayúsculas espaciadas funcionan como rótulos de embarque.

### Hierarchy
- **Display** (600, 78px, interlineado 1.2, tracking -0.05em): el titular de portada, siempre en dos líneas, cada una en su propia máscara ("SADACO" / "Venezuela"; "Hablemos" / "de su proyecto."). Baja a 64px (≤991), 54px (≤767) y 48px (≤479).
- **Headline** (600, 48px, 1.15, -0.03em): títulos de sección ("Detrás de cada entrega.") y titulares de banner. 42px (≤767), 36px (≤479).
- **Title Large** (700, 32px, 1.25): subtítulos de contenido ("Detalles", "Materiales disponibles", "Nuestra misión"). 28px (≤479).
- **Title** (700, 24px, 1.25, -0.03em): nombres en tarjetas de equipo, "¡Gracias!" en el formulario.
- **Title Small** (700, 18px): títulos de tarjeta de servicio ("Materiales / No ferrosos", en dos líneas) y "Sobre nosotros" en el footer.
- **List** (400, 18px, 1.25, -0.03em): ítems de listas con flecha (menú del footer, enlaces rápidos, megamenú). 16px en el footer y en ≤991.
- **Body Large** (Open Sans 400, 18px, 1.6): párrafos generales.
- **Body** (Open Sans 400, 16px, 1.6, color pizarra): descripciones, textos de tarjeta, texto enriquecido. Ancho máximo de una columna de la retícula (~65ch).
- **Label** (400, 12px, tracking 4px, MAYÚSCULAS): etiquetas sobre títulos ("NUESTRO EQUIPO"), rótulos de campos del formulario, cintas de desplazamiento, cargos, categorías y fechas.
- **Nav** (400, 14px, tracking 3px, MAYÚSCULAS): enlaces de la barra superior. 12px en ≤991.
- **Button** (400, 11px, tracking 3px, MAYÚSCULAS): texto de botones; 9px en botones pequeños y 12px en el botón de envío.

### Named Rules
**The Full Stop Rule.** Los titulares son frases cortas y afirmativas que terminan en punto: "Lo hacemos mejor.", "Detrás de cada entrega.", "Hablemos.". Nada de preguntas, signos de exclamación ni titulares de más de dos líneas en Display.

**The Label Above Rule.** Todo titular de sección lleva encima una etiqueta en mayúsculas espaciadas (Label), a 18px de separación. Es la firma tipográfica de International y aquí es obligatoria, aunque en otros contextos se considere un recurso gastado.

## Layout

**Contenedor.** Ancho máximo de 1400px centrado, con 5vw de margen lateral en todas las secciones. La barra de navegación y el footer usan el mismo margen, así que las líneas de la retícula coinciden de arriba abajo.

**Retícula visible.** Cuatro líneas verticales de 1px dividen el contenedor en tres columnas iguales. Van de arriba abajo en cada sección: en niebla sobre blanco y en blanco al 12% sobre fotos y sobre el footer. En tablet (≤991) desaparece una línea interior y quedan dos columnas; en móvil (≤767) desaparece otra y quedan solo los bordes. La mayoría de las cuadrículas usan columnas sin separación (`gap: 0`), así que el contenido toca las líneas.

**Ritmo vertical.** Las secciones llevan 120px de relleno vertical (80px en ≤991 y 60px en ≤767). Las secciones compactas llevan 60px. La sección de cita con foto usa 240px arriba y 160px abajo. Espaciado interno: 12, 18, 24 y 36px dentro de componentes, y 60, 80 y 160px entre bloques.

**Patrones recurrentes:**
- **Intro de tres columnas.** Etiqueta y titular en la columna 1, columna 2 vacía y botón alineado a la derecha en la columna 3. Lleva 60px de margen inferior.
- **Dos tercios y un tercio.** Los paneles niebla (aliados, cinta con texto en desplazamiento, formulario) ocupan las columnas 1 y 2, y la 3 queda blanca o recibe una lista fija (sticky).
- **Cascada.** En colecciones de tres (equipo, noticias), el segundo ítem baja 80px y el tercero 160px. Así las tarjetas "descienden" siguiendo la retícula.
- **Retícula de filetes.** Tarjetas de servicio en tres columnas separadas por líneas niebla de 1px, sin espacio entre ellas.

**Barra de navegación.** Fija, de 75px de alto (65px en ≤479). A la izquierda hay una caja blanca de un tercio de ancho (mínimo 275px) con el logo y el botón de menú de 80px. A la derecha, 2 o 3 enlaces en mayúsculas sobre fondo transparente.

**Plantillas de página.** Cada página de SADACO Venezuela se arma con una plantilla de International:

| Página Venezuela | Plantilla International |
|---|---|
| Inicio | Home: precarga, portada a pantalla completa, aliados, intro y tarjetas, sección de cita con parallax, footer |
| Nosotros | Team: portada interna, cinta en desplazamiento, misión y cita, tres valores |
| Soluciones y Productos (índices) | Products: portada interna, cinta fija con anclas, un banner por categoría |
| Cada solución y cada producto | Bloque de producto: banner con cortina, cinta en desplazamiento, "Detalles", "Disponible" y lista fija "Qué ofrecemos" |
| ¿Por qué elegirnos? | Valores de Team más la sección de cita con parallax |
| Contacto | Contact: portada interna, cinta, formulario en panel niebla de 2/3 y enlaces rápidos en 1/3 |
| 404 y Gracias | Portada interna reducida (650px) con un botón |

**Portada de inicio.** Ocupa el 100% del alto de pantalla, con un relleno superior de 120px. Arriba a la izquierda va la etiqueta; en el centro, el Display en dos líneas y un botón de contorno claro. Abajo a la derecha va el enlace circular de 148px que baja al contenido.

**Portada interna.** Mínimo de 650px de alto (550px en ≤767 y 450px en ≤479), con una retícula de tres filas: etiqueta arriba, Display en el centro y, abajo, una etiqueta con una línea horizontal que ocupa dos columnas. También lleva el enlace circular abajo a la derecha.

**Móvil.** Todas las cuadrículas pasan de 3 a 2 columnas y luego a 1. La caja blanca de la barra ocupa todo el ancho y los enlaces se mudan al megamenú. Las cascadas se anulan. El enlace circular se oculta, salvo dentro de tarjetas y en la sección de cita.

## Elevation & Depth

El sistema es completamente plano: no hay `box-shadow` en ningún componente. La profundidad se construye de tres maneras:
1. **Velos:** capas de tinta translúcida sobre las fotos.
2. **Escala:** las fotos entran al 120% y se asientan al 100%, y las tarjetas crecen al 105% al pasar el cursor.
3. **Cortinas:** paneles blancos que se retiran, hacia arriba o hacia un lado, para descubrir lo que hay debajo.

Las capas se ordenan con `z-index`: retícula (5), contenido (10), barra de navegación (20–30), megamenú (25) y precarga (10000).

### Named Rules
**The Flat Rule.** Prohibidas las sombras. Una tarjeta se separa del fondo con un filete de 1px en niebla o contorno, o con un cambio de fondo a niebla. Nunca con sombra ni con difuminado.

**The Curtain Rule.** Una sección oscura o fotográfica no aparece por opacidad: la descubre una cortina blanca que se retira mientras la foto baja de escala.

## Shapes

El lenguaje de formas es binario: o rectángulo de esquina viva o curva perfecta.
- **Rectángulos (0px):** fotos, tarjetas, paneles, banners, portadas y la caja del logo. Ninguna imagen lleva esquinas redondeadas.
- **Píldoras (100px):** todos los botones, el buscador del megamenú y las líneas de fondo de los enlaces del menú.
- **Círculos (50%):** el enlace grande de 148px, los íconos sociales (36px, o 30px en el footer), los íconos de lista de verificación (36px con contorno), los íconos de característica (60px, fondo niebla) y el círculo que llena las tarjetas.
- **Campos (2px):** la única excepción: inputs y textarea llevan una esquina de 2px apenas perceptible.
- **Filetes:** todas las líneas miden 1px. La única línea de 2px es el borde izquierdo que marca el crédito de una cita.

## Components

### Buttons
Píldoras discretas con texto diminuto muy espaciado. Se sienten como etiquetas de lujo, no como llamadas a la acción estridentes.
- **Forma:** píldora (100px), con texto Button en mayúsculas.
- **Primario:** fondo tinta, texto blanco y borde de 1px tinta, con relleno de 16px × 28px. Al pasar el cursor, el fondo y el borde pasan a contorno y el texto a tinta, con una transición de 0,4 s en `cubic-bezier(.25,.46,.45,.94)`.
- **Contorno claro** (sobre fotos): fondo transparente, borde blanco al 75% y texto blanco. Al pasar el cursor se rellena de tinta.
- **Contorno** (sobre blanco): fondo transparente, borde contorno y texto tinta. Al pasar el cursor se rellena de tinta con texto blanco. Suele ir en tamaño pequeño.
- **Sólido blanco:** fondo blanco con texto tinta. Al pasar el cursor, fondo contorno.
- **Pequeño:** relleno de 9px × 18px y texto de 9px.
- **Envío de formulario:** tinta, relleno de 16px × 32px, ancho mínimo de 160px y texto de 12px.
- **Magnetismo:** el texto del botón se desplaza hasta ±6px siguiendo la posición del cursor dentro del botón.

### Enlace circular (Hover Link)
La firma interactiva del sitio. Es un círculo de 148px con borde blanco de 1px y el texto o la flecha en blanco.
- **Magnetismo:** se desplaza hasta ±24px siguiendo al cursor.
- **Hover:** se rellena de blanco, el texto pasa a tinta, la flecha se invierte y el círculo escala a 1.1 (0,7 s, `outQuad`). En reposo tiene una opacidad de 0.8.
- **Usos:** bajar al contenido desde la portada (abajo a la derecha, a 5vw del borde), "Ver más" sobre tarjetas de equipo y el enlace de la sección de cita.

### Chips
El sistema no tiene chips.

### Cards / Containers
- **Tarjeta de servicio o producto:** fondo blanco sin borde propio (la separan los filetes de la retícula), relleno de 36px (48px en ≥1440) y 36px entre bloques. Contiene un título Title Small en dos líneas, una foto cuadrada de estudio a color (alto máximo de 25vw) y un botón de contorno pequeño.
  - En reposo, el contenido está 60px más abajo y el botón oculto.
  - Al pasar el cursor, la tarjeta escala a 1.05. Un círculo niebla que nace en la esquina superior derecha (6vw) crece hasta 55vw y la llena. El contenido sube 60px (1,6 s, `outExpo`) y el botón aparece desde abajo con 0,3 s de retraso.
- **Tarjeta de equipo o retrato:** foto a sangre con un velo de tinta al 15%, 30vw de alto (entre 300 y 465px). Arriba lleva el nombre (Title, blanco) a la izquierda y el cargo (Label, blanco) a la derecha. Abajo al centro, el ícono de LinkedIn en un círculo blanco de 36px.
  - Al pasar el cursor, el marco se reduce a 0.95 mientras la foto crece a 1.05 (contra-zoom), un círculo de tinta al 35% llena la tarjeta y aparece el enlace circular "Ver más".
- **Tarjeta de noticia:** imagen arriba (mínimo 225px), relleno de 36/36/24px, título en negrita, extracto en pizarra y un pie con la categoría a la izquierda y la fecha a la derecha, ambas en Label.
- **Panel niebla:** fondo niebla, relleno de 60px × 48px y esquinas vivas. Contiene logos de aliados, formularios o cintas.

### Inputs / Fields
- **Estilo:** borde de 1px contorno, fondo blanco al 65%, esquina de 2px, alto mínimo de 54px y relleno de 18px. El textarea mide 140px de alto.
- **Rótulo:** en estilo Label (mayúsculas, 12px, tracking 4px) sobre el campo.
- **Foco:** el fondo pasa a blanco sólido y el borde a foco-campo, con transición de 0,4 s y sin anillo de color.
- **Variante oscura:** fondo blanco al 8% y borde blanco al 16%; con foco, el borde pasa a blanco.
- **Mensajes:** el de éxito va en un panel con borde contorno sobre blanco al 85%, con "¡Gracias!" en Title. El de error va en un panel contorno con texto tinta.

### Navigation
- **Barra:** fija, de 75px. La caja izquierda blanca contiene el logo (alto máximo de 65px, 24px de relleno izquierdo) y el botón de menú de 80px con filetes niebla a ambos lados. El ícono es una animación Lottie de hamburguesa que se convierte en X.
- **Enlaces derechos:** texto Nav, blanco sobre la portada. Al pasar el cursor, una píldora de contorno de 46px de alto crece desde el centro (escala de 0 a 1, 0,5 s).
- **Al hacer scroll:** en el primer ~5% del recorrido de la página, un panel blanco baja desde arriba y cubre la franja derecha. Los enlaces pasan a tinta y la barra gana un borde niebla. La barra no se desvanece: la cubre un panel.
- **Megamenú:** panel niebla que se despliega hacia abajo (de alto 0 a automático y de -36px a 0, 1,3 s, `inOutExpo`) sobre un velo de tinta al 50%. Arriba lleva un buscador en píldora (en Venezuela, un botón "Solicitar cotización") y los íconos sociales. Debajo, dos columnas de listas, cada una con una etiqueta, un botón de contorno pequeño "Ver todo" e ítems con separador de contorno de 80px de alto.
- **Móvil:** la caja blanca ocupa todo el ancho. Los enlaces pasan al megamenú como desplegables que se abren con la misma curva.
- **Para Venezuela:** a la derecha van 3 enlaces (Soluciones, Productos, Contacto). El megamenú contiene las listas de Soluciones y Productos, más Nosotros y ¿Por qué elegirnos?.

### Ítem de lista con flecha
Es la fila base de todas las listas: footer, enlaces rápidos, megamenú y "Qué ofrecemos".
- Lleva relleno de 24px, texto List en pizarra y un separador inferior de 1px en niebla (o blanco al 15% sobre oscuro).
- Al pasar el cursor, el texto pasa a tinta y se desplaza 12px a la derecha. Una flecha de 18px aparece desde -18px con 0,2 s de retraso. El ítem de la página actual se desplaza 36px.
- Variante con verificación: un círculo de 36px con borde contorno y un check antes del texto.

### Cinta en desplazamiento (Marquee)
Franja niebla de 120px de alto con una frase en Label repetida, separada por puntos de tinta de 4px. Se desplaza horizontalmente (de 0 a -75%) **ligada al scroll**, no por tiempo. Al entrar en pantalla, su alto crece de 0 a 120px. Va siempre inmediatamente debajo de una portada o de un banner.

### Banner de categoría
Bloque de 400px de alto como mínimo (325px en ≤991), con foto desaturada, velo de tinta al 30% y contenido blanco centrado: etiqueta, Headline y botón de contorno claro. Al entrar en pantalla, una cortina blanca que cubre dos tercios se retira hacia un lado, alternando izquierda y derecha en banners consecutivos. La foto baja de 1.2 a 1 y el texto entra con máscara.

### Cinta fija de anclas
En los índices, una franja niebla fija bajo la barra (a 75px del borde superior), de dos tercios de ancho, con 3 a 6 anclas en Label centradas. Se reduce de 120 a 48px de alto al avanzar (1,6 s, `inOutExpo`).

### Sección de cita (parallax)
Relleno de 240px arriba y 160px abajo, con foto desaturada y velo de tinta al 45%. Lleva una etiqueta, una cita en Headline blanco y el crédito en Label con un borde izquierdo blanco de 2px.
- El texto se desplaza de -20% a +20% y la foto de +8% a -8% durante el scroll.
- Al entrar en pantalla, una cortina blanca se retira hacia arriba (2 s, `outExpo`) mientras la foto baja de 1.3 a 1.

### Precarga (Preloader)
Solo en inicio. Paneles blancos cubren la pantalla siguiendo la retícula: dos márgenes laterales y tres columnas con filetes niebla.
- Al terminar la carga, los márgenes suben primero (1,6 s, `inOutQuint`) y luego cada columna, con 300, 400 y 500 ms de retraso.
- A los 700 ms, la foto de portada baja de 1.2 a 1. Las líneas del Display entran a los 700 y 900 ms, y el botón a los 1100 ms.
- La precarga desaparece a los 2,1 s.

### Footer
Fondo tinta, 60px de relleno superior y la retícula en blanco al 12%. Tiene tres columnas:
- La marca: "SADACO" como palabra en Headline blanco, "Sobre nosotros" en Title Small y un párrafo en blanco al 90%.
- Una lista de navegación con flechas.
- "Síguenos", con íconos sociales de 30px.

### Movimiento
Estos son los tokens de movimiento. Los valores de curva son equivalentes CSS de las curvas de Webflow.
- **UI (microinteracciones):** 400ms `cubic-bezier(.25,.46,.45,.94)`. Se usa en botones, ítems de lista y campos.
- **Revelado:** 1300–1600ms `inOutExpo` `cubic-bezier(.87,0,.13,1)`. Se usa en titulares, banners, megamenú y desplegables.
- **Colección:** 800–1300ms `inOutQuint` `cubic-bezier(.83,0,.17,1)`. Se usa en tarjetas que entran en pantalla y en la precarga.
- **Asentamiento:** 1600–2000ms `outExpo` `cubic-bezier(.16,1,.3,1)`. Se usa en cortinas de sección y en el contenido de tarjetas.
- **Hover:** 500–700ms `outQuad`. Se usa en círculos que crecen y en escalas.

Coreografías base:
- **Entrada con máscara:** el elemento está dentro de un contenedor con `overflow: hidden`. Parte de `translateY(100%)`, `skewY(10deg)` y opacidad 0, y llega a su posición natural. En secuencia: etiqueta a 0 ms, titular a 200 ms, botón a 300 ms y extra a 500 ms. Se dispara cuando el bloque entra en pantalla.
- **Entrada de colección:** parte de `translateY(15vh)`, `scale(.9)`, `skewY(5deg)` y opacidad 0. La escala se asienta 500 ms después del movimiento.
- **Entrada de tarjeta:** parte de `translateY(80px)`, `skewY(10deg)` y opacidad 0 (1,6 s, `inOutExpo`).
- **Íconos sociales:** escala 1.15 al pasar el cursor (0,4 s).

### Named Rules
**The Masked Entrance Rule.** Ningún texto aparece desvaneciéndose en su lugar. Todo titular, etiqueta o botón entra subiendo desde una máscara, con la inclinación enderezándose.

**The Magnet Rule.** Lo circular sigue al cursor: el enlace de 148px se mueve ±24px y el texto de los botones ±6px. En pantallas táctiles no hay magnetismo.

## Do's and Don'ts

### Do:
- **Do** mantener la retícula de tres columnas visible en todas las secciones y alinear titulares, botones y paneles a sus líneas.
- **Do** usar solo tinta, blanco, niebla, contorno y pizarra en la interfaz, y dejar el azul, el verde y el rojo dentro del logo.
- **Do** desaturar las fotos de portada, de banners y de la sección de cita, y cubrirlas con un velo de tinta del 30% (45% en portadas internas).
- **Do** usar fotos a color solo en tamaños pequeños: productos de estudio sobre fondo oscuro, retratos del equipo y noticias.
- **Do** poner una etiqueta en Label sobre cada titular de sección y escribir los titulares como frases cortas con punto final.
- **Do** hacer entrar todo texto con la entrada con máscara y las curvas `inOutExpo` de 1,3–1,6 s.
- **Do** respetar `prefers-reduced-motion`: sin precarga, sin parallax ni magnetismo, y entradas reducidas a un fundido corto. International no lo hace; la sede sí.
- **Do** limitar la precarga a la página de inicio y no retrasar el contenido más de ~2 s.
- **Do** usar el logo 08 (globo con laureles y Venezuela en rojo) en la caja blanca de la barra, a 65px de alto como máximo, y "SADACO" como palabra en el footer.

### Don't:
- **Don't** usar sombras, degradados de color, desenfoques ni efectos de vidrio (la barra no lleva `backdrop-filter`).
- **Don't** redondear fotos, tarjetas ni paneles. Solo los botones son píldoras y solo los círculos son círculos.
- **Don't** usar botones de color (verde, azul o rojo). El único botón sólido es tinta, o blanco sobre fotos.
- **Don't** usar Montserrat ni otras familias: solo Inter y Open Sans.
- **Don't** usar mosaicos tipo bento, tarjetas con esquinas redondeadas ni fondos de color saturado. No existen en el sistema.
- **Don't** poner texto blanco sobre una foto sin velo de tinta.
- **Don't** animar texto con simples fundidos, rebotes o curvas elásticas.
- **Don't** usar más de tres enlaces visibles en la barra. El resto va al megamenú.
