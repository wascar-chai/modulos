# -*- coding: utf-8 -*-
"""El PDF de la cotizacion siempre sale en espanol.

Poner el idioma en el registro -`doc.with_context(lang=...)`- no basta: los
conversores de QWeb formatean fechas e importes con el idioma del ENTORNO que
esta renderizando, no con el del registro. Por eso la cotizacion salia con
fechas 08/27/2026 y unidades "Units" aunque el contacto estuviera en es_DO.

Aqui se fija el idioma del entorno completo antes de renderizar, que es lo que
arregla de una vez fechas, importes, unidades y etiquetas traducidas.
"""
from odoo import models

INFORMES_PROPIOS = ("chai_ws_wascardev_reports.cotizacion",)
IDIOMAS_ES = ["es_DO", "es_ES", "es_419", "es"]


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    def _chai_idioma_espanol(self):
        """Primer espanol instalado, empezando por el dominicano."""
        idiomas = self.env["res.lang"].sudo().search([("code", "in", IDIOMAS_ES)])
        por_codigo = {i.code: i for i in idiomas}
        for codigo in IDIOMAS_ES:
            if codigo in por_codigo:
                return codigo
        return None

    def _chai_entorno_en_espanol(self, report_ref):
        """Devuelve self con el idioma fijado, o None si no hay que cambiar nada."""
        try:
            informe = self._get_report(report_ref)
        except Exception:
            return None
        if informe.report_name not in INFORMES_PROPIOS:
            return None
        idioma = self._chai_idioma_espanol()
        if not idioma or self.env.context.get("lang") == idioma:
            return None
        return self.with_context(lang=idioma)

    def _render_qweb_pdf(self, report_ref, res_ids=None, data=None):
        en_espanol = self._chai_entorno_en_espanol(report_ref)
        if en_espanol is not None:
            return super(IrActionsReport, en_espanol)._render_qweb_pdf(report_ref, res_ids, data)
        return super()._render_qweb_pdf(report_ref, res_ids, data)

    def _render_qweb_html(self, report_ref, docids, data=None):
        en_espanol = self._chai_entorno_en_espanol(report_ref)
        if en_espanol is not None:
            return super(IrActionsReport, en_espanol)._render_qweb_html(report_ref, docids, data)
        return super()._render_qweb_html(report_ref, docids, data)
