# -*- coding: utf-8 -*-
"""Enganches de instalacion y desinstalacion.

Al instalar:
  * se apaga el formato anterior, que vivia solo dentro de la base de datos
    (modulo `custom_reports`, sin codigo en ningun repositorio);
  * el boton Imprimir, el correo y el portal siguen usando la accion estandar de
    Odoo, a la que el modulo le cambia el informe por el nuestro.

Al desinstalar se devuelve a Odoo su propio informe, para que el boton siga
funcionando aunque este modulo ya no este.
"""
import logging

_logger = logging.getLogger(__name__)

FORMATOS_ANTERIORES = [
    "custom_reports.report_saleorder_document_custom",
]


def post_init_hook(env):
    for xmlid in FORMATOS_ANTERIORES:
        vista = env.ref(xmlid, raise_if_not_found=False)
        if vista and vista.active:
            vista.active = False
            _logger.info("chai_ws_wascardev_reports: apagado el formato anterior %s", xmlid)


def uninstall_hook(env):
    accion = env.ref("sale.action_report_saleorder", raise_if_not_found=False)
    if accion:
        accion.write({
            "report_name": "sale.report_saleorder",
            "report_file": "sale.report_saleorder",
            "paperformat_id": False,
        })
        _logger.info("chai_ws_wascardev_reports: la cotizacion vuelve al informe estandar de Odoo")
