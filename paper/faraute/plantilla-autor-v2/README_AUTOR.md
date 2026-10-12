# Plantilla FARAUTE para autores

Revista FARAUTE de Ciencias y Tecnología (FACYT, Universidad de Carabobo).

Las normas completas están en `GUIA_PARA_LOS_AUTORES.pdf` (en inglés, `GUIDE_FOR_AUTHORS.pdf`), incluidas en esta carpeta.

Esta carpeta contiene todo lo que necesita para preparar su artículo con el formato final de la revista. **Usted solo escribe su propio contenido.** El volumen, el número, las páginas, el banner, los ISSN y las fechas de recepción y aceptación los coloca el editor.

## Archivos

| Archivo | ¿Lo edita? | Qué contiene |
|---|---|---|
| `articulo.tex` | No | Archivo principal. Es el que se compila. |
| `datos.tex` | **Sí** | Tipo de contribución, títulos, autores, afiliaciones, resumen, abstract, palabras clave, secciones finales y sus macros propias. |
| `contenido.tex` | **Sí** | El cuerpo del artículo, de la Introducción a las Conclusiones. |
| `referencias.bib` | **Sí** | Sus referencias en formato BibTeX. |
| `figuras/` | **Sí** | Sus imágenes. |
| `faraute.cls` | No | Diseño de la revista. |

El archivo de ejemplo que viene en la carpeta está redactado como guía: cada elemento (ecuación, teorema, algoritmo, figura, tabla, cita) aparece con la forma correcta de escribirlo. Reemplace su texto por el suyo.

## Cómo compilar

Necesita una distribución TeX actualizada (TeX Live, MiKTeX o Overleaf) con **pdfLaTeX** y **Biber**.

```
latexmk -pdf articulo.tex
```

Si lo hace a mano o desde TeXstudio: `pdflatex` → `biber` → `pdflatex` → `pdflatex`. En TeXstudio, elija Biber en *Opciones → Configurar → Compilar → Herramienta de bibliografía*. En Overleaf funciona sin cambios.

## Qué va en `datos.tex`

```latex
\tipodecontribucion{Artículo divulgativo de investigación}
\titulo{Título en español}
\tituloingles{Title in English}
\titulocorto{Título corto para el encabezado}

\autor[1]{Nombre A.}{Apellido B.}[correo@uc.edu.ve]  % [correo] = autor de correspondencia (*)
\autor[1,2]{Nombre C.}{Apellido D.}
\afiliacion{1}{Departamento..., Facultad..., Universidad... Ciudad, País}
\afiliacion{2}{...}

\resumen{... máximo 150 palabras, sin referencias ...}
\palabrasclave{alfa; beta; gamma}            % de 3 a 5, en orden alfabético
\resumeningles{...}
\palabrasclaveingles{alpha; beta; gamma}
```

Las secciones finales se imprimen solas, antes de las referencias y en este orden:

| Comando | Sección | ¿Obligatoria? |
|---|---|---|
| `\agradecimientos{}` | Agradecimientos | No |
| `\contribuciones{}` | Contribución de los autores (CRediT) | Sí, si hay más de un autor |
| `\conflictos{}` | Conflicto de intereses | Sí |
| `\disponibilidad{}` | Disponibilidad de datos y código | Sí |
| `\declaracionIA{}` | Declaración sobre el uso de inteligencia artificial | Sí, si se usó IA (guía, sección 7) |
| `\nota{}` | Nota | No |

Al final de `datos.tex` puede agregar sus paquetes y macros (`\newcommand`, `\DeclareMathOperator`, `\usepackage{tikz}`...).

## Controles automáticos

Al compilar, la clase revisa las normas y deja un aviso (en TeXstudio o en Overleaf aparece en la lista de advertencias) si:

- el resumen o el abstract pasan de 150 palabras;
- hay menos de 3 o más de 5 palabras clave;
- falta el título en inglés, el título corto o el tipo de contribución;
- el artículo supera 20 páginas (límite de la revista para artículos; más páginas solo con una justificación en la carta de envío).

Compile sin avisos de la clase `faraute` antes de enviar.

## Elementos del texto

| Elemento | Cómo se escribe | Cómo se cita en el texto |
|---|---|---|
| Sección | `\section{...}`, `\subsection{...}` (se numeran solas) | `\refsec{etiqueta}` → Sección 3 |
| Ecuación | `\begin{equation} ... \label{eq:x} \end{equation}` | `\refec{eq:x}` → Ec. (1) |
| Figura | `figure` con `\includegraphics{nombre}` (se busca en `figuras/`) | `\reffig{fig:x}` → Fig. 1 |
| Tabla | `table` con `\caption` **encima** y `booktabs` | `\reftab{tab:x}` → Tabla 1 |
| Algoritmo | `algorithm` + `algorithmic`: título arriba, pseudocódigo con líneas numeradas, `\Require` (Entrada) y `\Ensure` (Salida) | `\refalg{alg:x}` → Algoritmo 1 |
| Teoremas | `teorema`, `lema`, `proposicion`, `corolario`, `definicion`, `ejemplo`, `observacion`, `demostracion` | con `\ref` |
| Cita entre paréntesis | `\citep{clave}` | (Eckart y Young, 1936) |
| Cita narrativa | `\citet{clave}` | Eckart y Young (1936) |
| Cita con localizador | `\citep[cap.~7]{clave}` | (Fessler y Nadakuditi, 2024, cap. 7) |

Una figura o una tabla que ocupe las dos columnas se escribe con `figure*` o `table*`.

**Figuras:** al menos 300 ppp, en PNG, JPG, TIFF o PDF vectorial. Como la revista es digital, se admiten a color; la información no debe depender solo del color: use también marcadores, tipos de línea o etiquetas. Termine cada leyenda con la fuente («Fuente: elaboración propia»).

**Algoritmos:** el código fuente completo no va en el artículo; se deposita en un repositorio y se cita en `\disponibilidad{}`.

**Referencias:** la lista se genera sola en estilo APA 7 (adaptación al español: "y" entre los dos últimos autores, sin coma), en orden alfabético. Escriba en el `.bib` todos los autores, no "and others". Solo aparecen las obras citadas, y cada una indica en qué páginas se cita. Escriba el DOI siempre que exista (campo `doi`, sin `https://doi.org/`). Los datos y el software también se citan.

## Opciones para el arbitraje

En la primera línea de `articulo.tex`:

```latex
\documentclass[revision]{faraute}   % versión anónima y con líneas numeradas
```

| Opción | Efecto |
|---|---|
| `revision` | Equivale a `anonimo` + `lineas`. Úsela para el envío a arbitraje. |
| `anonimo` | Oculta autores, afiliaciones, correo, agradecimientos, contribuciones y nota. |
| `lineas` | Numera las líneas. |
| `ingles` | El artículo está escrito en inglés: textos fijos en inglés, título y abstract en inglés primero y citas APA en inglés ("&"). |
| `bibmanual` | Sus referencias están escritas a mano (`thebibliography`) en `referencias.tex` y no en `referencias.bib`. Es solo para transición: se recomienda `referencias.bib`. |

## Paquetes que la clase ya carga

amsmath, mathtools, amsthm, símbolos AMS, graphicx, xcolor, booktabs, tabularx, multirow, array, colortbl, float, placeins, caption, subcaption, enumitem, xurl, hyperref, algorithm, algpseudocode y biblatex (APA).

No los vuelva a cargar con opciones distintas; eso produce un error de *option clash*. No cargue `natbib`: la clase ya ofrece `\citep` y `\citet`. Puede agregar cualquier otro paquete (tikz, pgfplots, siunitx, listings, algorithm2e...).

## Uso de inteligencia artificial

Si usó herramientas de IA para algo más que corregir ortografía y gramática (redactar, traducir, buscar literatura, programar, analizar datos, verificar demostraciones, hacer figuras explicativas), declárelo en la carta de envío y en `\declaracionIA{}` con el modelo que trae `datos.tex`. La IA no puede ser autora ni citarse como fuente. Usted responde por todo el contenido, y en especial debe verificar que cada referencia exista. No se permite fabricar ni alterar datos o imágenes de resultados. El detalle está en la sección 7 de la guía.

## Qué enviar

**Para el arbitraje:** el PDF compilado con la opción `revision`, con una carta de envío que indique el tipo de contribución, la originalidad del trabajo, la justificación si pasa de 20 páginas y la declaración de uso de IA.

**Versión final aceptada:** la carpeta completa comprimida en un .zip con `articulo.tex`, `datos.tex`, `contenido.tex`, `referencias.bib` y `figuras/`, más cualquier archivo que usen (por ejemplo, `.tikz`). Quite antes la opción `revision`. No incluya archivos auxiliares (`.aux`, `.log`, `.bbl`...).

Envíos y correspondencia: farautecienciauc@gmail.com
