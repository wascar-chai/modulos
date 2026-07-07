from odoo import api, fields, models

PAID_STATES = ('paid', 'in_payment')


class AccountMove(models.Model):
    _inherit = 'account.move'

    commission_line_ids = fields.One2many(
        'commission.line', 'move_id', string='Comisiones',
    )
    commission_count = fields.Integer(compute='_compute_commission_count')

    def _compute_commission_count(self):
        for move in self:
            move.commission_count = len(move.commission_line_ids)

    def write(self, vals):
        result = super().write(vals)
        if 'payment_state' in vals:
            for move in self:
                if move.move_type != 'out_invoice':
                    continue
                if move.payment_state in PAID_STATES:
                    move._generate_commission_line()
                else:
                    move.commission_line_ids.filtered(
                        lambda line: line.state == 'to_pay'
                    ).unlink()
        return result

    def _generate_commission_line(self):
        """Crea la línea de comisión del empleado al cobrarse la factura.

        El empleado se determina a partir del vendedor de la factura
        (`invoice_user_id`), buscando el `hr.employee` vinculado a ese usuario.
        """
        self.ensure_one()
        if self.commission_line_ids or self.state != 'posted':
            return
        salesperson = self.invoice_user_id
        if not salesperson:
            return
        employee = self.env['hr.employee'].search(
            [('user_id', '=', salesperson.id)], limit=1)
        if not employee or not employee.commission_percent:
            return
        self.env['commission.line'].create({
            'move_id': self.id,
            'employee_id': employee.id,
            'commission_percent': employee.commission_percent,
            'base_amount': self.amount_untaxed_signed,
        })

    def action_view_commissions(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Comisiones',
            'res_model': 'commission.line',
            'view_mode': 'list,form',
            'domain': [('move_id', '=', self.id)],
            'context': {'default_move_id': self.id},
        }
