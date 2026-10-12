%% =====================================================================
%%  faraute.cls — Clase LaTeX de la Revista FARAUTE de Ciencias y Tecnología
%%  Facultad Experimental de Ciencias y Tecnología, Universidad de Carabobo
%%
%%  Una sola clase para tres usos:
%%    \documentclass{faraute}            -> AUTOR: manuscrito (sin banner,
%%                                          sin volumen, sin fechas)
%%    (definiendo \FarauteID)            -> EDITOR: versión final de un
%%                                          artículo; lee revista-config.tex
%%                                          y faraute-paginas.tex
%%    \documentclass[revista]{faraute}   -> EDITOR: ensamblaje del volumen
%%                                          (carga faraute-editorial.sty)
%%
%%  Opciones para autores:
%%    anonimo    oculta autores, afiliaciones, correo, agradecimientos,
%%               contribuciones y nota (arbitraje doble ciego)
%%    lineas     numera las líneas (facilita el arbitraje)
%%    revision   = anonimo + lineas
%%    ingles     artículo escrito en inglés (textos fijos en inglés, título
%%               y abstract en inglés primero, citas APA con "&")
%%    bibmanual  referencias escritas a mano (thebibliography) en
%%               referencias.tex, en lugar de referencias.bib + biber
%%
%%  El autor NO modifica este archivo. Todo lo que es del autor va en
%%  datos.tex y contenido.tex; todo lo que es del editor va en
%%  revista-config.tex.
%% =====================================================================
\NeedsTeXFormat{LaTeX2e}[2020/10/01]
\ProvidesClass{faraute}[2026/09/29 v1.0 Revista FARAUTE de Ciencias y Tecnologia]

%% ---------------------------------------------------------------------
%% 1. Opciones y modo de trabajo
%% ---------------------------------------------------------------------
\newif\iffar@anonimo
\newif\iffar@lineas
\newif\iffar@bibmanual
\newif\iffar@editor
\newif\iffar@revista
\newif\iffar@ingles
\DeclareOption{anonimo}{\far@anonimotrue}
\DeclareOption{lineas}{\far@lineastrue}
\DeclareOption{revision}{\far@anonimotrue\far@lineastrue}
\DeclareOption{bibmanual}{\far@bibmanualtrue}
\DeclareOption{editor}{\far@editortrue}
\DeclareOption{revista}{\far@revistatrue}
\DeclareOption{ingles}{\far@inglestrue}
\DeclareOption{english}{\far@inglestrue}
\DeclareOption*{\ClassWarningNoLine{faraute}{Opci\string\'on desconocida: \CurrentOption}}
\ProcessOptions\relax
% Textos fijos en el idioma del artículo: \far@t{español}{inglés}
\newcommand\far@t[2]{\iffar@ingles#2\else#1\fi}

% El script del editor define \FarauteID antes de cargar el artículo.
\ifdefined\FarauteID \far@editortrue \fi
\iffar@revista \far@editorfalse \fi
% La versión final nunca es anónima ni lleva números de línea.
\iffar@editor \far@anonimofalse \far@lineasfalse \fi

\iffar@revista
  \LoadClass[10pt,letterpaper,oneside]{article}
\else
  \LoadClass[10pt,letterpaper,twocolumn]{article}
\fi

%% ---------------------------------------------------------------------
%% 2. Idioma, tipografía y página (comunes a los tres modos)
%% ---------------------------------------------------------------------
\RequirePackage[T1]{fontenc}
\RequirePackage[utf8]{inputenc}
\iffar@ingles
  \RequirePackage[spanish,english,es-noshorthands,es-tabla,es-nolists,es-nodecimaldot]{babel}
\else
  \RequirePackage[english,spanish,es-noshorthands,es-tabla,es-nolists,es-nodecimaldot]{babel}
\fi
\RequirePackage{mathtools}   % carga amsmath
\RequirePackage{amsthm}
\IfFileExists{newtxmath.sty}{%
  \RequirePackage{newtxtext}%
  \RequirePackage{newtxmath}%
  % newtxmath ya trae todos los símbolos de amssymb/amsfonts; si el autor
  % los pide, no se vuelven a cargar (evita "\Bbbk already defined").
  \expandafter\def\csname ver@amssymb.sty\endcsname{2013/01/14 v3.01 (provisto por newtxmath)}%
  \expandafter\def\csname ver@amsfonts.sty\endcsname{2013/01/14 v3.01 (provisto por newtxmath)}%
}{%
  \RequirePackage{mathptmx}%
  \RequirePackage{amssymb}%
}
\RequirePackage[scaled=0.92]{helvet}   % títulos en Helvetica
\RequirePackage{microtype}
\RequirePackage[table]{xcolor}
\RequirePackage{graphicx}
\RequirePackage{etoolbox}
\RequirePackage{geometry}
\geometry{letterpaper,left=2.5cm,right=2.5cm,top=2.4cm,bottom=2.2cm,
          headheight=13pt,headsep=0.45cm,footskip=0.95cm,columnsep=0.55cm}
\RequirePackage{fancyhdr}
\RequirePackage[explicit]{titlesec}
\RequirePackage{enumitem}
\RequirePackage{booktabs,tabularx,multirow,array,colortbl}
\RequirePackage{float,placeins}
\RequirePackage[font=small,labelfont={bf,sf},labelsep=period,skip=4pt]{caption}
\RequirePackage{subcaption}
\RequirePackage{xurl}

\definecolor{farazul}{RGB}{0,0,90}       % títulos y enlaces
\definecolor{fargris}{RGB}{229,230,232}  % recuadro de las secciones
\definecolor{farfondo}{RGB}{247,247,249} % fondo del resumen

\setlength{\parindent}{0pt}
\setlength{\parskip}{4pt plus 1pt minus 1pt}
\setlength{\emergencystretch}{1.5em}
\setlist{leftmargin=*,itemsep=1pt,topsep=3pt,parsep=0pt}

%% ---------------------------------------------------------------------
%% 3. Datos de la revista (se fijan en revista-config.tex)
%% ---------------------------------------------------------------------
\ExplSyntaxOn
\tl_new:N \g_far_volumen_tl       \tl_gset:Nn \g_far_volumen_tl {??}
\tl_new:N \g_far_numero_tl        \tl_gset:Nn \g_far_numero_tl {??}
\tl_new:N \g_far_anio_tl          \tl_gset:Nn \g_far_anio_tl {????}
\tl_new:N \g_far_issnimp_tl       \tl_gset:Nn \g_far_issnimp_tl {1698-7418}
\tl_new:N \g_far_issnele_tl       \tl_gset:Nn \g_far_issnele_tl {2542-3061}
\tl_new:N \g_far_deplegal_tl      \tl_gset:Nn \g_far_deplegal_tl {PP200402CA1617}
\tl_new:N \g_far_correo_tl        \tl_gset:Nn \g_far_correo_tl {farautecienciauc@gmail.com}
\tl_new:N \g_far_abrev_tl         \tl_gset:Nn \g_far_abrev_tl {FARAUTE~Ciens.~y~Tec.}
\tl_new:N \g_far_nombrerev_tl     \tl_gset:Nn \g_far_nombrerev_tl {FARAUTE}
\tl_new:N \g_far_especial_tl
\tl_new:N \g_far_banner_tl        \tl_gset:Nn \g_far_banner_tl {imagenes/Banner2023.jpeg}
\tl_new:N \g_far_bannerprel_tl    \tl_gset:Nn \g_far_bannerprel_tl {imagenes/BannerUC.jpg}
\tl_new:N \g_far_portada_tl       \tl_gset:Nn \g_far_portada_tl {imagenes/Portada2023.jpg}
\tl_new:N \g_far_diagramacion_tl
\tl_new:N \g_far_disenio_tl
\int_new:N \g_far_limite_int      \int_gset:Nn \g_far_limite_int {20}

\NewDocumentCommand \volumen            {m} { \tl_gset:Nn \g_far_volumen_tl {#1} }
\NewDocumentCommand \numero             {m} { \tl_gset:Nn \g_far_numero_tl {#1} }
\NewDocumentCommand \anio               {m} { \tl_gset:Nn \g_far_anio_tl {#1} }
\NewDocumentCommand \issnimpreso        {m} { \tl_gset:Nn \g_far_issnimp_tl {#1} }
\NewDocumentCommand \issnelectronico    {m} { \tl_gset:Nn \g_far_issnele_tl {#1} }
\NewDocumentCommand \depositolegal      {m} { \tl_gset:Nn \g_far_deplegal_tl {#1} }
\NewDocumentCommand \correorevista      {m} { \tl_gset:Nn \g_far_correo_tl {#1} }
\NewDocumentCommand \abreviatura        {m} { \tl_gset:Nn \g_far_abrev_tl {#1} }
\NewDocumentCommand \nombrerevista      {m} { \tl_gset:Nn \g_far_nombrerev_tl {#1} }
\NewDocumentCommand \volumenespecial    {m} { \tl_gset:Nn \g_far_especial_tl {#1} }
\NewDocumentCommand \bannerarticulos    {m} { \tl_gset:Nn \g_far_banner_tl {#1} }
\NewDocumentCommand \bannerpreliminares {m} { \tl_gset:Nn \g_far_bannerprel_tl {#1} }
\NewDocumentCommand \portada            {m} { \tl_gset:Nn \g_far_portada_tl {#1} }
\NewDocumentCommand \diagramacion       {m} { \tl_gset:Nn \g_far_diagramacion_tl {#1} }
\NewDocumentCommand \disenografico      {m} { \tl_gset:Nn \g_far_disenio_tl {#1} }
\NewDocumentCommand \limitepaginas      {m} { \int_gset:Nn \g_far_limite_int {#1} }

% Lectura de los datos en preliminares (comite.tex, índice, etc.)
\NewExpandableDocumentCommand \revvolumen        {} { \tl_use:N \g_far_volumen_tl }
\NewExpandableDocumentCommand \revnumero         {} { \tl_use:N \g_far_numero_tl }
\NewExpandableDocumentCommand \revanio           {} { \tl_use:N \g_far_anio_tl }
\NewExpandableDocumentCommand \revissnimpreso    {} { \tl_use:N \g_far_issnimp_tl }
\NewExpandableDocumentCommand \revissnelectronico{} { \tl_use:N \g_far_issnele_tl }
\NewExpandableDocumentCommand \revdepositolegal  {} { \tl_use:N \g_far_deplegal_tl }
\NewExpandableDocumentCommand \revcorreo         {} { \tl_use:N \g_far_correo_tl }
\NewExpandableDocumentCommand \revabreviatura    {} { \tl_use:N \g_far_abrev_tl }
\NewExpandableDocumentCommand \revespecial       {} { \tl_use:N \g_far_especial_tl }
\NewExpandableDocumentCommand \revdiagramacion   {} { \tl_use:N \g_far_diagramacion_tl }
\NewExpandableDocumentCommand \revdisenio        {} { \tl_use:N \g_far_disenio_tl }

% Lista ordenada de artículos del número y sus datos editoriales:
%   \articulo{01-Otto}{recibido=26/07/2026, revisado=03/08/2026,
%                      aceptado=26/09/2026, doi=10.xxxx/yyyy}
\seq_new:N  \g_far_articulos_seq
\prop_new:N \g_far_artdatos_prop
\prop_new:N \g_far_paginas_prop
\NewDocumentCommand \articulo {m m}
  {
    \seq_gput_right:Nn \g_far_articulos_seq {#1}
    \prop_gput:Nnn \g_far_artdatos_prop {#1} {#2}
  }
% Escrito por revista.tex en faraute-paginas.tex: \FarautePaginas{ID}{ini}{fin}
\NewDocumentCommand \FarautePaginas {m m m}
  { \prop_gput:Nnn \g_far_paginas_prop {#1} { {#2}{#3} } }

\tl_new:N \l_far_recibido_tl
\tl_new:N \l_far_revisado_tl
\tl_new:N \l_far_aceptado_tl
\tl_new:N \l_far_doi_tl
\keys_define:nn { faraute / articulo }
  {
    recibido .tl_set:N = \l_far_recibido_tl ,
    revisado .tl_set:N = \l_far_revisado_tl ,
    aceptado .tl_set:N = \l_far_aceptado_tl ,
    doi      .tl_set:N = \l_far_doi_tl ,
    unknown  .code:n   = \ClassWarningNoLine{faraute}{Clave~desconocida~en~\token_to_str:N\articulo}
  }

% Carga los datos editoriales del artículo #1 en \l_far_..._tl
\cs_new_protected:Npn \far_cargar_datos:n #1
  {
    \prop_get:NnNTF \g_far_artdatos_prop {#1} \l_tmpa_tl
      { \keys_set:nV { faraute / articulo } \l_tmpa_tl }
      { \ClassWarningNoLine{faraute}{El~artículo~'#1'~no~figura~en~revista-config.tex} }
  }
\cs_generate_variant:Nn \keys_set:nn { nV }
\ExplSyntaxOff

%% ---------------------------------------------------------------------
%% 4. Modo revista: se delega en faraute-editorial.sty y termina aquí
%% ---------------------------------------------------------------------
\iffar@revista
  \RequirePackage{faraute-editorial}%
  \expandafter\endinput
\fi

%% =====================================================================
%%  A partir de aquí: el artículo (modo autor o modo editor)
%% =====================================================================

%% ---------------------------------------------------------------------
%% 5. Datos del artículo (los escribe el autor en datos.tex)
%% ---------------------------------------------------------------------
\ExplSyntaxOn
\tl_new:N \g_far_tipo_tl
\tl_new:N \g_far_titulo_tl
\tl_new:N \g_far_tituloen_tl
\tl_new:N \g_far_titulocorto_tl
\tl_new:N \g_far_autorescortos_tl
\tl_new:N \g_far_resumen_tl
\tl_new:N \g_far_resumenen_tl
\tl_new:N \g_far_claves_tl
\tl_new:N \g_far_clavesen_tl
\tl_new:N \g_far_agradecimientos_tl
\tl_new:N \g_far_contribuciones_tl
\tl_new:N \g_far_disponibilidad_tl
\tl_new:N \g_far_declaracionia_tl
\tl_new:N \g_far_nota_tl
\tl_new:N \g_far_conflictos_tl
\seq_new:N \g_far_autores_seq
\seq_new:N \g_far_afiliaciones_seq

\NewDocumentCommand \tipodecontribucion {m} { \tl_gset:Nn \g_far_tipo_tl {#1} }
\NewDocumentCommand \titulo             {m} { \tl_gset:Nn \g_far_titulo_tl {#1} }
\NewDocumentCommand \tituloingles       {m} { \tl_gset:Nn \g_far_tituloen_tl {#1} }
\NewDocumentCommand \titulocorto        {m} { \tl_gset:Nn \g_far_titulocorto_tl {#1} }
\NewDocumentCommand \autorescortos      {m} { \tl_gset:Nn \g_far_autorescortos_tl {#1} }
\NewDocumentCommand \resumen            {+m}{ \tl_gset:Nn \g_far_resumen_tl {#1} }
\NewDocumentCommand \resumeningles      {+m}{ \tl_gset:Nn \g_far_resumenen_tl {#1} }
\NewDocumentCommand \palabrasclave      {m} { \tl_gset:Nn \g_far_claves_tl {#1} }
\NewDocumentCommand \palabrasclaveingles{m} { \tl_gset:Nn \g_far_clavesen_tl {#1} }
\NewDocumentCommand \agradecimientos    {+m}{ \tl_gset:Nn \g_far_agradecimientos_tl {#1} }
\NewDocumentCommand \contribuciones     {+m}{ \tl_gset:Nn \g_far_contribuciones_tl {#1} }
\NewDocumentCommand \disponibilidad     {+m}{ \tl_gset:Nn \g_far_disponibilidad_tl {#1} }
\NewDocumentCommand \declaracionIA      {+m}{ \tl_gset:Nn \g_far_declaracionia_tl {#1} }
\NewDocumentCommand \nota               {+m}{ \tl_gset:Nn \g_far_nota_tl {#1} }
\NewDocumentCommand \conflictos         {+m}{ \tl_gset:Nn \g_far_conflictos_tl {#1} }

% \autor[afiliaciones]{Nombre(s)}{Apellido(s)}[correo]
%   con [correo] el autor queda marcado como autor de correspondencia (*)
\NewDocumentCommand \autor { O{} m m o }
  {
    \IfNoValueTF {#4}
      { \seq_gput_right:Nn \g_far_autores_seq { {#2}{#3}{#1}{} } }
      { \seq_gput_right:Nn \g_far_autores_seq { {#2}{#3}{#1}{#4} } }
  }
% \afiliacion{n}{Departamento, Facultad, Universidad. Ciudad, País}
\NewDocumentCommand \afiliacion { m m }
  { \seq_gput_right:Nn \g_far_afiliaciones_seq { \textsuperscript{#1}#2 } }

% --- Composición de la lista de autores ---------------------------------
\seq_new:N \l_far_tmp_seq
\seq_new:N \g_far_correos_seq
\tl_new:N  \l_far_sup_tl
\cs_new_protected:Npn \far_autor_titulo:nnnn #1#2#3#4
  {
    \tl_set:Nn \l_far_sup_tl {#3}
    \tl_if_blank:nF {#4}
      {
        \tl_if_blank:VTF \l_far_sup_tl
          { \tl_set:Nn \l_far_sup_tl {*} }
          { \tl_put_right:Nn \l_far_sup_tl {,*} }
        \seq_gput_right:Nn \g_far_correos_seq { \href{mailto:#4}{#4} }
      }
    \seq_put_right:Nx \l_far_tmp_seq
      {
        \exp_not:n {#1~#2}
        \tl_if_blank:VF \l_far_sup_tl
          { \exp_not:N \textsuperscript { \exp_not:V \l_far_sup_tl } }
      }
  }
\cs_new_protected:Npn \far_autores_titulo:
  {
    \seq_clear:N \l_far_tmp_seq
    \seq_gclear:N \g_far_correos_seq
    \seq_map_inline:Nn \g_far_autores_seq { \far_autor_titulo:nnnn ##1 }
    \seq_use:Nnnn \l_far_tmp_seq { ~y~ } { ,~ } { ~y~ }
  }
\cs_new_protected:Npn \far_correspondencia:
  {
    \int_compare:nNnT { \seq_count:N \g_far_correos_seq } > { 0 }
      {
        \par \textsuperscript{*}
        \textbf{ \int_compare:nNnTF { \seq_count:N \g_far_correos_seq } > { 1 }
                   { \far@t{Autores~de~correspondencia}{Corresponding~authors} } { \far@t{Autor~de~correspondencia}{Corresponding~author} } }:~
        \seq_use:Nn \g_far_correos_seq { ,~ }
      }
  }
% Autores para el índice del volumen: "Apellido Nombre, Apellido Nombre"
\cs_new:Npn \far_autor_indice:nnnn #1#2#3#4 { \exp_not:n {#2~#1} }
\cs_new_protected:Npn \far_autores_indice:N #1
  {
    \seq_clear:N \l_far_tmp_seq
    \seq_map_inline:Nn \g_far_autores_seq
      { \seq_put_right:Nx \l_far_tmp_seq { \far_autor_indice:nnnn ##1 } }
    \tl_set:Nx #1 { \seq_use:Nn \l_far_tmp_seq { ,~ } }
  }
% Autores para el encabezado: 1 -> Apellido; 2 -> A y B; 3+ -> A et al.
\cs_new:Npn \far_apellido:nnnn #1#2#3#4 { \exp_not:n {#2} }
\tl_new:N \g_far_cortos_tl
\cs_new_protected:Npn \far_calcular_cortos:
  {
    \tl_if_blank:VTF \g_far_autorescortos_tl
      {
        \seq_clear:N \l_far_tmp_seq
        \seq_map_inline:Nn \g_far_autores_seq
          { \seq_put_right:Nx \l_far_tmp_seq { \far_apellido:nnnn ##1 } }
        \int_compare:nNnTF { \seq_count:N \l_far_tmp_seq } > {2}
          { \tl_gset:Nx \g_far_cortos_tl { \seq_item:Nn \l_far_tmp_seq {1} ~et~al. } }
          { \tl_gset:Nx \g_far_cortos_tl { \seq_use:Nn \l_far_tmp_seq { ~y~ } } }
      }
      { \tl_gset_eq:NN \g_far_cortos_tl \g_far_autorescortos_tl }
  }

% --- Controles de normas (avisos en el registro de compilación) -------
\int_new:N \l_far_n_int
\seq_new:N \l_far_pal_seq
\cs_new_protected:Npn \far_contar_palabras:NN #1#2
  {
    \seq_set_split:NnV \l_far_pal_seq { ~ } #1
    \seq_remove_all:Nn \l_far_pal_seq { }
    \int_set:Nn #2 { \seq_count:N \l_far_pal_seq }
  }
\cs_generate_variant:Nn \seq_set_split:Nnn { NnV }
\cs_new_protected:Npn \far_contar_claves:NN #1#2
  {
    \tl_if_in:NnTF #1 {;}
      { \seq_set_split:NnV \l_far_pal_seq { ; } #1 }
      { \seq_set_split:NnV \l_far_pal_seq { , } #1 }
    \seq_remove_all:Nn \l_far_pal_seq { }
    \int_set:Nn #2 { \seq_count:N \l_far_pal_seq }
  }
\cs_new_protected:Npn \far_verificar_preambulo:
  {
    \tl_if_blank:VT \g_far_titulo_tl
      { \ClassWarningNoLine{faraute}{Falta~\token_to_str:N\titulo} }
    \tl_if_blank:VT \g_far_tituloen_tl
      { \ClassWarningNoLine{faraute}{Falta~el~título~en~inglés~(\token_to_str:N\tituloingles)} }
    \tl_if_blank:VT \g_far_titulocorto_tl
      { \ClassWarningNoLine{faraute}{Falta~\token_to_str:N\titulocorto;~se~usa~el~título~completo~en~el~encabezado} }
    \tl_if_blank:VT \g_far_tipo_tl
      { \ClassWarningNoLine{faraute}{Declare~el~tipo~de~contribución~con~\token_to_str:N\tipodecontribucion} }
    \seq_if_empty:NT \g_far_autores_seq
      { \ClassWarningNoLine{faraute}{No~hay~autores~(\token_to_str:N\autor)} }
    \far_contar_palabras:NN \g_far_resumen_tl \l_far_n_int
    \int_compare:nNnT \l_far_n_int > {150}
      { \ClassWarningNoLine{faraute}{El~resumen~tiene~unas~\int_use:N\l_far_n_int\space~palabras~(máximo~150)} }
    \far_contar_palabras:NN \g_far_resumenen_tl \l_far_n_int
    \int_compare:nNnT \l_far_n_int > {150}
      { \ClassWarningNoLine{faraute}{El~abstract~tiene~unas~\int_use:N\l_far_n_int\space~palabras~(máximo~150)} }
    \far_contar_claves:NN \g_far_claves_tl \l_far_n_int
    \bool_lazy_or:nnT { \int_compare_p:nNn \l_far_n_int < 3 } { \int_compare_p:nNn \l_far_n_int > 5 }
      { \ClassWarningNoLine{faraute}{Hay~\int_use:N\l_far_n_int\space~palabras~clave~(se~piden~de~3~a~5,~en~orden~alfabético)} }
    \far_contar_claves:NN \g_far_clavesen_tl \l_far_n_int
    \bool_lazy_or:nnT { \int_compare_p:nNn \l_far_n_int < 3 } { \int_compare_p:nNn \l_far_n_int > 5 }
      { \ClassWarningNoLine{faraute}{Hay~\int_use:N\l_far_n_int\space~keywords~(se~piden~de~3~a~5)} }
  }
\int_new:N \g_far_inicio_int
\int_gset:Nn \g_far_inicio_int {1}
\cs_new_protected:Npn \far_verificar_final:
  {
    \int_set:Nn \l_far_n_int { \value{page} - \g_far_inicio_int + 1 }
    \int_compare:nNnT \l_far_n_int > \g_far_limite_int
      { \ClassWarningNoLine{faraute}{El~artículo~ocupa~\int_use:N\l_far_n_int\space~páginas~(límite~\int_use:N\g_far_limite_int)} }
    \typeout{}
    \typeout{FARAUTE:~artículo~de~\int_use:N\l_far_n_int\space~página(s)~
      \iffar@editor [modo~editor,~ID~\FarauteID] \else [modo~autor] \fi}
    \typeout{}
  }

% --- Accesos de uso interno en LaTeX2e ---------------------------------
\cs_new_eq:NN \far@autorestitulo   \far_autores_titulo:
\cs_new_eq:NN \far@correspondencia \far_correspondencia:
\cs_new:Npn \far@autorescortos { \tl_use:N \g_far_cortos_tl }
\cs_new:Npn \far@usar #1 { \tl_use:c { g_far_#1_tl } }
\cs_new_protected:Npn \far@siexiste #1#2 { \tl_if_empty:cF { g_far_#1_tl } {#2} }
\cs_new_protected:Npn \far@afiliaciones
  { \seq_use:Nn \g_far_afiliaciones_seq { \par } }
\cs_new_eq:NN \far@verificarpreambulo \far_verificar_preambulo:
\cs_new_eq:NN \far@verificarfinal     \far_verificar_final:
\cs_new_protected:Npn \far@textocorto
  { \tl_if_blank:VTF \g_far_titulocorto_tl { \tl_use:N \g_far_titulo_tl } { \tl_use:N \g_far_titulocorto_tl } }
\ExplSyntaxOff

%% ---------------------------------------------------------------------
%% 6. Modo editor: datos del volumen y paginación
%% ---------------------------------------------------------------------
% Los artículos viven en EDITOR/articulos/NN-Nombre/, de modo que la raíz
% del editor está dos niveles arriba (puede redefinirse con \FarauteRaiz).
\ifdefined\FarauteRaiz \else \def\FarauteRaiz{../../}\fi
\newcommand\far@lineasuperior{}
\newcommand\far@pie{}
\newcommand\far@fechas{}
% Los datos se leen con la sintaxis normal (espacios significativos).
\iffar@editor
  \InputIfFileExists{\FarauteRaiz revista-config.tex}{}
    {\ClassError{faraute}{No se encuentra \FarauteRaiz revista-config.tex}
        {El articulo debe estar en EDITOR/articulos/<ID>/}}
  \InputIfFileExists{\FarauteRaiz faraute-paginas.tex}{}
    {\ClassWarningNoLine{faraute}{Aun no existe faraute-paginas.tex:
        compile revista.tex (o use construir\string_revista.py)}}
\fi
\ExplSyntaxOn
\iffar@editor
  \exp_args:No \far_cargar_datos:n { \FarauteID }
  \tl_new:N \l_far_ini_tl
  \tl_new:N \l_far_fin_tl
  \prop_get:NVNTF \g_far_paginas_prop \FarauteID \l_tmpa_tl
    {
      \tl_set:Nx \l_far_ini_tl { \tl_item:Nn \l_tmpa_tl {1} }
      \tl_set:Nx \l_far_fin_tl { \tl_item:Nn \l_tmpa_tl {2} }
      \int_gset:Nn \g_far_inicio_int { \l_far_ini_tl }
    }
    {
      \tl_set:Nn \l_far_ini_tl {?}
      \tl_set:Nn \l_far_fin_tl {?}
      \ClassWarningNoLine{faraute}{Sin~paginación~para~'\FarauteID';~se~empieza~en~la~página~1}
    }
  \cs_set:Npx \far@lineasuperior
    {
      \exp_not:V \g_far_nombrerev_tl ,~Vol.~\exp_not:V \g_far_volumen_tl ,~
      No.~\exp_not:V \g_far_numero_tl ,~
      \exp_not:V \l_far_ini_tl \exp_not:N \textendash \exp_not:V \l_far_fin_tl ,~
      \exp_not:V \g_far_anio_tl
    }
  \cs_set:Npx \far@pie
    { \exp_not:V \g_far_abrev_tl ,~ \exp_not:V \g_far_volumen_tl (\exp_not:V \g_far_numero_tl ),~\exp_not:V \g_far_anio_tl }
  \cs_set:Npx \far@fechas
    {
      \far@t{Recibido}{Received}:~\tl_if_blank:VTF \l_far_recibido_tl {\exp_not:N\textemdash} {\exp_not:V \l_far_recibido_tl},~
      \far@t{Revisado}{Revised}:~\tl_if_blank:VTF \l_far_revisado_tl {\exp_not:N\textemdash} {\exp_not:V \l_far_revisado_tl},~
      \far@t{Aceptado}{Accepted}:~\tl_if_blank:VTF \l_far_aceptado_tl {\exp_not:N\textemdash} {\exp_not:V \l_far_aceptado_tl}
    }
  \cs_set:Npx \far@doi { \exp_not:V \l_far_doi_tl }
\else
  \cs_set:Npn \far@lineasuperior
    { \textbf{FARAUTE}~de~Ciencias~y~Tecnología~\textperiodcentered{}~
      \iffar@anonimo \far@t{Manuscrito~anónimo~para~arbitraje}{Anonymous~manuscript~for~peer~review}
      \else \far@t{Manuscrito~del~autor}{Author's~manuscript} \fi }
  \cs_set:Npn \far@pie { FARAUTE~Ciens.~y~Tec.~\textperiodcentered{}~\far@t{manuscrito}{manuscript} }
  \cs_set:Npn \far@doi {}
\fi
\ExplSyntaxOff
\AtBeginDocument{\setcounter{page}{\numexpr\csname g_far_inicio_int\endcsname\relax}}

%% ---------------------------------------------------------------------
%% 7. Encabezados y pies de página
%% ---------------------------------------------------------------------
\fancypagestyle{faraute}{%
  \fancyhf{}%
  \fancyhead[L]{\bfseries\far@textocorto}%
  \fancyhead[R]{\bfseries\iffar@anonimo\far@t{Manuscrito an\'onimo}{Anonymous manuscript}\else\far@autorescortos\fi}%
  \fancyfoot[C]{\bfseries\far@pie}%
  \fancyfoot[R]{\thepage}%
  \renewcommand\headrulewidth{0.5pt}%
  \renewcommand\footrulewidth{0.5pt}}
\fancypagestyle{far@primera}{%
  \fancyhf{}\fancyfoot[C]{\thepage}%
  \renewcommand\headrulewidth{0pt}\renewcommand\footrulewidth{0pt}}
\pagestyle{faraute}

%% ---------------------------------------------------------------------
%% 8. Títulos de sección
%% ---------------------------------------------------------------------
\newcommand\far@caja[1]{%
  \colorbox{fargris}{\parbox{\dimexpr\linewidth-2\fboxsep\relax}{%
    \centering\sffamily\bfseries\large\color{farazul}\strut#1\strut}}}
\titleformat{\section}[block]{\normalfont}{}{0pt}{\far@caja{\thesection.\enspace#1}}
\titleformat{name=\section,numberless}[block]{\normalfont}{}{0pt}{\far@caja{#1}}
\titleformat{\subsection}[hang]{\sffamily\bfseries\color{farazul}\raggedright}{\thesubsection}{0.5em}{#1}
\titleformat{name=\subsection,numberless}[hang]{\sffamily\bfseries\color{farazul}\raggedright}{}{0pt}{#1}
\titleformat{\subsubsection}[hang]{\sffamily\bfseries\small\raggedright}{\thesubsubsection}{0.5em}{#1}
\titleformat{name=\subsubsection,numberless}[hang]{\sffamily\bfseries\small\raggedright}{}{0pt}{#1}
\titleformat{\paragraph}[runin]{\normalfont\bfseries}{}{0pt}{#1.}
\titlespacing*{\section}{0pt}{16pt plus 4pt minus 2pt}{8pt plus 2pt}
\titlespacing*{\subsection}{0pt}{12pt plus 3pt minus 2pt}{4pt plus 1pt}
\titlespacing*{\subsubsection}{0pt}{9pt plus 2pt minus 2pt}{3pt}
\titlespacing*{\paragraph}{0pt}{6pt plus 2pt}{0.5em}
\setcounter{secnumdepth}{3}

%% ---------------------------------------------------------------------
%% 9. Figuras, tablas, ecuaciones, algoritmos, teoremas
%% ---------------------------------------------------------------------
\captionsetup[table]{position=top}
\addto\captionsspanish{%
  \renewcommand\figurename{Fig.}%
  \renewcommand\tablename{Tabla}%
  \renewcommand\refname{Referencias}%
  \renewcommand\proofname{Demostraci\'on}}
\addto\captionsenglish{%
  \renewcommand\figurename{Fig.}%
  \renewcommand\tablename{Table}%
  \renewcommand\refname{References}%
  \renewcommand\proofname{Proof}}
\graphicspath{{figuras/}{images/}{imagenes/}{./}}
\renewcommand\topfraction{0.9}
\renewcommand\dbltopfraction{0.9}
\renewcommand\textfraction{0.1}
\renewcommand\floatpagefraction{0.8}
\renewcommand\dblfloatpagefraction{0.8}

% Referencias cruzadas con la denominación de las normas
\newcommand\refec[1]{\far@t{Ec.}{Eq.}~(\ref{#1})}
\newcommand\reffig[1]{Fig.~\ref{#1}}
\newcommand\reftab[1]{\far@t{Tabla}{Table}~\ref{#1}}
\newcommand\refalg[1]{\far@t{Algoritmo}{Algorithm}~\ref{#1}}
\newcommand\refsec[1]{\far@t{Secci\'on}{Section}~\ref{#1}}

% Teoremas en español (numeración compartida)
\theoremstyle{plain}
\newtheorem{teorema}{\far@t{Teorema}{Theorem}}
\newtheorem{lema}[teorema]{\far@t{Lema}{Lemma}}
\newtheorem{proposicion}[teorema]{\far@t{Proposici\'on}{Proposition}}
\newtheorem{corolario}[teorema]{\far@t{Corolario}{Corollary}}
\theoremstyle{definition}
\newtheorem{definicion}[teorema]{\far@t{Definici\'on}{Definition}}
\newtheorem{ejemplo}[teorema]{\far@t{Ejemplo}{Example}}
\theoremstyle{remark}
\newtheorem{observacion}[teorema]{\far@t{Observaci\'on}{Remark}}
\newenvironment{demostracion}{\begin{proof}}{\end{proof}}

%% ---------------------------------------------------------------------
%% 10. Referencias bibliográficas
%% ---------------------------------------------------------------------
\iffar@bibmanual
  % Referencias escritas a mano (thebibliography) en referencias.tex
  \RequirePackage[round,authoryear]{natbib}
  \setlength{\bibsep}{2pt plus 1pt}
  \renewcommand\bibfont{\small}
  \newcommand\bibliografia[1]{}
\else
  % APA 7 en español, cita autor-año enlazada y "citado en las págs."
  \RequirePackage{csquotes}
  \RequirePackage[style=apa,backend=biber,natbib=true,backref=true]{biblatex}
  \DefineBibliographyStrings{spanish}{%
    backrefpage  = {citado en la p\'ag\adddot},
    backrefpages = {citado en las p\'ags\adddot}}
  % APA 7 en español: "y" (no "&") entre los dos últimos autores, en las
  % citas y en la lista de referencias, y sin coma antes de "y".
  \iffar@ingles\else
    \DeclareDelimFormat[parencite]{finalnamedelim}{\addspace\bibstring{and}\space}%
    \DeclareDelimFormat[fullcite,fullcitebib]{finalnamedelim}{\addspace\bibstring{and}\space}%
    \DeclareDelimFormat[bib,biblist]{finalnamedelim}{%
      \ifthenelse{\value{listcount}>\maxprtauth}{}{\addspace\bibstring{and}\space}}%
    % sin coma detrás del penúltimo autor ("Candès, E. J. y Recht, B.")
    \renewcommand*{\apablx@ifnotfinalname}{%
      \ifboolexpr{test {\ifnumless{\value{listcount}}{\value{liststop}-1}}
                  or test \ifmorenames}}%
  \fi
  \renewcommand*{\bibfont}{\small}
  \setlength{\bibitemsep}{2pt}
  \defbibheading{faraute}[\refname]{\section*{#1}}
  \IfFileExists{referencias.bib}{\addbibresource{referencias.bib}}{}
  \newcommand\bibliografia[1]{\addbibresource{#1}}
\fi

%% ---------------------------------------------------------------------
%% 11. Paquetes que se cargan al final del preámbulo
%%     (así no chocan con las opciones que ponga el autor)
%% ---------------------------------------------------------------------
\AtEndPreamble{%
  \@ifpackageloaded{algorithm2e}{%
    \SetAlgorithmName{\far@t{Algoritmo}{Algorithm}}{\far@t{algoritmo}{algorithm}}{\far@t{Lista de algoritmos}{List of algorithms}}%
  }{%
    \RequirePackage{algorithm}%
    \RequirePackage{algpseudocode}%
    \floatname{algorithm}{\far@t{Algoritmo}{Algorithm}}%
    \captionsetup[algorithm]{labelsep=period,labelfont={bf,sf}}%
    \renewcommand{\algorithmicrequire}{\textbf{\far@t{Entrada}{Input}:}}%
    \renewcommand{\algorithmicensure}{\textbf{\far@t{Salida}{Output}:}}%
  }%
  \@ifpackageloaded{listings}{%
    \lstset{basicstyle=\ttfamily\footnotesize,numbers=left,numberstyle=\tiny,
            breaklines=true,columns=fullflexible,frame=lines}%
    \renewcommand\lstlistingname{C\'odigo}%
  }{}%
  \iffar@lineas
    \RequirePackage[switch]{lineno}%
    \AtBeginDocument{\linenumbers}%
  \fi
  \RequirePackage{hyperref}%
  \hypersetup{colorlinks=true,linkcolor=farazul,citecolor=farazul,
              urlcolor=farazul,breaklinks=true,bookmarksopen=false,
              pdfcreator={faraute.cls}}%
}
\AtBeginDocument{%
  \far@verificarpreambulo
  \csname far_calcular_cortos:\endcsname
  \pdfstringdefDisableCommands{\let\textsuperscript\@gobble\let\\\space}%
  \iffar@anonimo\else\hypersetup{pdfauthor={\far@autorescortos}}\fi
  \hypersetup{pdftitle={\far@usar{titulo}}}%
}
\AtEndDocument{\far@verificarfinal}

%% ---------------------------------------------------------------------
%% 12. Metadatos para el índice del volumen (solo en modo editor)
%% ---------------------------------------------------------------------
\ExplSyntaxOn
\iow_new:N \g_far_meta_iow
\tl_new:N \l_far_indice_tl
\iffar@editor
  \AtBeginDocument
    {
      \far_autores_indice:N \l_far_indice_tl
      \iow_open:Nn \g_far_meta_iow { faraute-meta.tex }
      \iow_now:Nx \g_far_meta_iow
        {
          \token_to_str:N \FarauteMeta
          { \FarauteID }
          { \exp_not:V \g_far_titulo_tl }
          { \exp_not:V \g_far_tituloen_tl }
          { \exp_not:V \l_far_indice_tl }
          { \exp_not:V \g_far_tipo_tl }
        }
      \iow_close:N \g_far_meta_iow
    }
\fi
\ExplSyntaxOff

%% ---------------------------------------------------------------------
%% 13. Página de título
%% ---------------------------------------------------------------------
\newcommand\far@bloquetitulo{%
  \vspace*{-1.0cm}%
  {\sffamily\small
   \begin{minipage}[t]{0.64\textwidth}\raggedright\far@lineasuperior\end{minipage}\hfill
   \begin{minipage}[t]{0.34\textwidth}\raggedleft
     \iffar@editor Online ISSN \revissnelectronico\\Print ISSN \revissnimpreso
     \else\far@t{versi\'on del}{version of} \today\fi
   \end{minipage}\par}%
  \iffar@editor
    \vspace{2pt}%
    {\centering\includegraphics[width=\textwidth]{\FarauteRaiz\csname g_far_banner_tl\endcsname}\par}%
    \vspace{6pt}%
  \else
    \vspace{2pt}{\color{farazul}\rule{\textwidth}{0.8pt}}\par\vspace{10pt}%
  \fi
  \far@siexiste{tipo}{{\sffamily\small\scshape\color{farazul}\far@usar{tipo}\par}\vspace{3pt}}%
  {\raggedright\sffamily\bfseries\fontsize{15}{18.5}\selectfont\color{farazul}%
   \iffar@ingles\far@usar{tituloen}\else\far@usar{titulo}\fi\par}%
  \vspace{7pt}%
  \iffar@anonimo
    {\sffamily\small\itshape [\far@t{Autores, afiliaciones y correo omitidos para el arbitraje doble ciego}{Authors, affiliations and e-mail omitted for double-blind review}]\par}%
  \else
    {\sffamily\raggedright\far@autorestitulo\par}%
    \vspace{1pt}%
    {\sffamily\footnotesize\raggedright\itshape\far@afiliaciones\par}%
    {\sffamily\footnotesize\raggedright\far@correspondencia\par}%
  \fi
  \iffar@editor
    \vspace{9pt}%
    {\sffamily\small\bfseries\itshape\color{farazul}\far@fechas\par}%
    \if\relax\detokenize\expandafter{\far@doi}\relax\else
      {\sffamily\footnotesize DOI: \href{https://doi.org/\far@doi}{https://doi.org/\far@doi}\par}%
    \fi
  \fi
  \vspace{9pt}%
  \noindent\setlength{\fboxsep}{7pt}%
  \colorbox{farfondo}{\parbox{\dimexpr\textwidth-2\fboxsep\relax}{%
    \sffamily\small\setlength{\parskip}{0pt}%
    \iffar@ingles
      \far@bloqueEN\vspace{9pt}\far@bloqueES[\far@usar{titulo}]%
    \else
      \far@bloqueES\vspace{9pt}\far@bloqueEN[\far@usar{tituloen}]%
    \fi}}%
  \par\vspace{14pt}}
% Resumen en español y abstract en inglés; [título] se imprime cuando el
% bloque va en segundo lugar (título en el otro idioma).
\newcommand\far@bloqueES[1][]{%
  \begin{otherlanguage}{spanish}%
  \if\relax\detokenize{#1}\relax\else
    {\raggedright\bfseries\normalsize\color{farazul}#1\par}\vspace{5pt}\fi
  {\bfseries Resumen}\par
  \far@usar{resumen}\par\vspace{3pt}%
  {\bfseries Palabras clave:} \far@usar{claves}\par
  \end{otherlanguage}}
\newcommand\far@bloqueEN[1][]{%
  \begin{otherlanguage}{english}%
  \if\relax\detokenize{#1}\relax\else
    {\raggedright\bfseries\normalsize\color{farazul}#1\par}\vspace{5pt}\fi
  {\bfseries Abstract}\par
  \far@usar{resumenen}\par\vspace{3pt}%
  {\bfseries Keywords:} \far@usar{clavesen}\par
  \end{otherlanguage}}

\renewcommand\maketitle{%
  \twocolumn[\far@bloquetitulo]%
  \thispagestyle{far@primera}}

%% ---------------------------------------------------------------------
%% 14. Secciones finales y referencias: \finaldelarticulo
%% ---------------------------------------------------------------------
\newcommand\far@final[3]{% #1 clave, #2 título, #3 ¿se oculta al anonimizar?
  \far@siexiste{#1}{%
    \par\medskip
    \ifnum#3=1 \iffar@anonimo
      \textbf{#2.} [\far@t{Omitido para el arbitraje doble ciego}{Omitted for double-blind review}.]\par
    \else
      \textbf{#2.} \far@usar{#1}\par
    \fi\else
      \textbf{#2.} \far@usar{#1}\par
    \fi}}
\newcommand\finaldelarticulo{%
  \far@final{agradecimientos}{\far@t{Agradecimientos}{Acknowledgments}}{1}%
  \far@final{contribuciones}{\far@t{Contribuci\'on de los autores}{Author contributions}}{1}%
  \far@final{conflictos}{\far@t{Conflicto de intereses}{Conflicts of interest}}{0}%
  \far@final{disponibilidad}{\far@t{Disponibilidad de datos y c\'odigo}{Data and code availability}}{0}%
  \far@final{declaracionia}{\far@t{Declaraci\'on sobre el uso de inteligencia artificial}{Declaration on the use of artificial intelligence}}{0}%
  \far@final{nota}{\far@t{Nota}{Note}}{1}%
  \iffar@bibmanual
    \InputIfFileExists{referencias.tex}{}{}%
  \else
    \printbibliography[heading=faraute]%
  \fi}

\endinput
