# -*- coding: utf-8 -*-
{
    "name": "WascarDev | Formato de cotizacion",
    "summary": "Cotizacion con el diseno de la marca: cabecera limpia, datos del "
               "cliente, tabla legible, totales destacados y bloque de pago y firma.",
    "description": """
Formato de cotizacion de WascarDev
==================================

Reemplaza el PDF de la cotizacion por uno pensado para enviarse a un cliente:

* Titulo y numero destacados, con la linea azul de la marca.
* Ficha del cliente y ficha de datos del documento, una al lado de la otra.
* Tabla legible: secciones con banda, subtotal por seccion y columnas que solo
  aparecen cuando hacen falta (descuento e impuestos).
* Totales en una caja, con el Total en la banda azul oscura de la marca.
* Bloque final con los datos para el pago -tomados de las cuentas bancarias de
  la compania en Odoo- y la linea de firma.
* Todo en espanol y con fechas dd/mm/aaaa, sin depender del idioma que tenga
  cada contacto.

El diseno anterior vivia solo dentro de la base de datos, en el modulo
`custom_reports`, que no tiene codigo en ningun repositorio. Al instalar este
modulo esa plantilla se desactiva sola, y queda esta, que si esta versionada.
""",
    "version": "18.0.1.1.0",
    "category": "Sales/Sales",
    "author": "CHAI Consultoria y Software",
    "website": "https://chaiconsultoria.com",
    "license": "LGPL-3",
    "depends": ["sale"],
    "data": [
        "views/res_partner_bank_views.xml",
        "views/layout.xml",
        "views/report_cotizacion.xml",
    ],
    "post_init_hook": "post_init_hook",
    "uninstall_hook": "uninstall_hook",
    "installable": True,
    "application": False,
}
