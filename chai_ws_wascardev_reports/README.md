# Formato de cotización de WascarDev

Reemplaza el PDF de la cotización por uno propio, escrito desde cero: no hereda
la plantilla de Odoo ni la parchea, la sustituye entera. Así el orden de los
bloques, los tamaños y los colores son nuestros y no cambian cuando Odoo cambia
la suya.

## Qué trae

* **Cabecera propia** en todas las páginas: logo a la izquierda y los datos de la
  empresa a la derecha (nombre, RNC, teléfono, correo, web), separados por la
  línea azul de la marca.
* **Título y número** grandes, con el número en el azul del logo.
* **Ficha del cliente** y **ficha del documento** una al lado de la otra: fecha,
  validez, referencia, responsable y forma de pago.
* **Tabla legible**: encabezado en azul noche, secciones con banda, subtotal por
  sección, y columnas que solo aparecen cuando hacen falta (descuento e
  impuestos). Si todo está exento, en vez de repetir "ITBIS Exempt" en cada
  línea aparece una sola nota debajo de la tabla.
* **Totales** en caja, con el TOTAL en la banda azul noche.
* **Datos para el pago en el pie de página**, tomados de las cuentas bancarias
  de la compañía en Odoo, junto al lema y la numeración "Página X de Y". Van en
  el pie y no al final del cuerpo por una razón práctica: puestos en el cuerpo
  quedaban justo debajo de los totales y dejaban media hoja en blanco; en el pie
  se apoyan siempre abajo, salga la cotización de tres líneas o de treinta.
* **Sin línea de firma**: no se usa.
* Todo en **español** y fechas **dd/mm/aaaa**.

## Los dos problemas de fondo que resuelve

**1. El PDF salía en inglés.** Fechas `09/22/2026`, "Untaxed Amount", "Units".
No era el idioma del documento sino el del contacto: la plantilla anterior
forzaba `lang=doc.partner_id.lang` y varios clientes tenían `en_US`.

Poner el idioma en el registro no basta, porque los conversores de QWeb formatean
fechas e importes con el idioma del **entorno que renderiza**, no con el del
registro. Por eso el módulo fija el idioma del entorno completo antes de
renderizar (`models/ir_actions_report.py`), y con eso quedan bien de una vez las
fechas, los importes, las unidades y las etiquetas traducidas.

**2. Los datos bancarios generaban una segunda página casi vacía.** Estaban
escritos dentro del campo *Nota* del pedido, se imprimían después de los totales
y se partían. Ahora salen de **Contabilidad → Configuración → Cuentas
bancarias**, que es donde van, y el PDF los coloca en el pie de página. La nota del pedido se
sigue imprimiendo, salvo que sea el texto viejo de las cuentas, para que las
cotizaciones anteriores no lo muestren dos veces.

## Un campo nuevo

Odoo no distingue entre cuenta corriente y de ahorro, y aquí eso siempre se pone
al lado del número. El módulo añade **Tipo de cuenta** a la cuenta bancaria
(`res.partner.bank.chai_tipo_cuenta`) y lo muestra en el PDF.

## Qué hay que configurar

El módulo no inventa datos: los toma de Odoo. Para que el PDF salga completo:

| Dónde | Qué |
|---|---|
| Ajustes → Compañías | RNC/Cédula, dirección, teléfono y el lema (*Lema de la compañía*, sale en el pie) |
| Contabilidad → Configuración → Cuentas bancarias | Las cuentas, con su tipo |
| Contactos | RNC, dirección y teléfono de cada cliente — es lo que llena la ficha del cliente |

## Instalación y desinstalación

Al instalar, el módulo apaga el formato anterior, que vivía **solo dentro de la
base de datos** (módulo `custom_reports`, sin código en ningún repositorio), y
apunta la acción de imprimir de Odoo a este informe: así el botón Imprimir, el
correo al cliente y el portal usan el diseño nuevo sin tocar nada más.

Al desinstalar se devuelve la acción al informe estándar de Odoo, de modo que el
botón sigue funcionando aunque el módulo ya no esté. Probado: instalar,
desinstalar y volver a instalar deja la cotización funcionando en los tres casos.

## Nota técnica

El PDF lo dibuja wkhtmltopdf, que es un WebKit viejo: no entiende flexbox, grid
ni degradados. Por eso todo el armado va con tablas y colores planos.

Los márgenes del formato de papel no son decorativos: **arriba 44 mm** tiene que
ser mayor que la cabecera (el logo mide 86 px ≈ 23 mm) más su separación, y
**abajo 42 mm** mayor que el pie con los datos de pago. Si se quedan cortos,
wkhtmltopdf recorta: la cabecera desaparece y del pie solo se ve la primera
línea. Si algún día se agranda el logo o se añade otra cuenta bancaria, hay que
subir el margen correspondiente.
