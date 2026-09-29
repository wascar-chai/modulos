# -*- coding: utf-8 -*-
"""Tipo de cuenta bancaria.

Odoo no distingue entre cuenta corriente y de ahorro, y en el pais eso siempre
se pone al lado del numero. Antes se resolvia escribiendolo a mano dentro de la
nota de la cotizacion; asi se guarda donde va y el PDF lo toma solo.
"""
from odoo import fields, models


class ResPartnerBank(models.Model):
    _inherit = "res.partner.bank"

    chai_tipo_cuenta = fields.Selection(
        [("corriente", "Cuenta Corriente"), ("ahorro", "Cuenta de Ahorro")],
        string="Tipo de cuenta",
        help="Se muestra junto al numero en el PDF de la cotizacion.")
