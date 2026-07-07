from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    commission_percent = fields.Float(
        string='% Comisión',
        default=0.0,
        help='Porcentaje que se aplica sobre el monto sin impuestos de las '
             'facturas de cliente para calcular la comisión de este empleado.',
    )
