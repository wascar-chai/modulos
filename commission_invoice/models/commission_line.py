from odoo import api, fields, models


class CommissionLine(models.Model):
    _name = 'commission.line'
    _description = 'Comisión sobre Factura Pagada'
    _order = 'invoice_date desc, id desc'

    name = fields.Char(string='Referencia', compute='_compute_name', store=True)
    move_id = fields.Many2one(
        'account.move', string='Factura', required=True,
        ondelete='cascade',
        domain=[('move_type', '=', 'out_invoice')],
    )
    partner_id = fields.Many2one(
        related='move_id.partner_id', string='Cliente', store=True, readonly=True,
    )
    invoice_date = fields.Date(
        related='move_id.invoice_date', string='Fecha Factura', store=True, readonly=True,
    )
    employee_id = fields.Many2one(
        'hr.employee', string='Empleado', required=True,
        help='Empleado que recibe la comisión.',
    )
    currency_id = fields.Many2one(
        related='move_id.currency_id', string='Moneda', store=True, readonly=True,
    )
    company_id = fields.Many2one(
        related='move_id.company_id', string='Compañía', store=True, readonly=True,
    )
    base_amount = fields.Monetary(
        string='Base de Cálculo', required=True,
        help='Monto sin impuestos de la factura sobre el que se calcula la comisión.',
    )
    commission_percent = fields.Float(string='% Comisión', required=True)
    commission_amount = fields.Monetary(
        string='Importe Comisión', compute='_compute_commission_amount', store=True,
    )
    state = fields.Selection([
        ('to_pay', 'Pendiente de pago'),
        ('paid', 'Pagada'),
    ], string='Estado', default='to_pay', required=True, copy=False)
    payment_date = fields.Date(string='Fecha de pago al empleado', copy=False)
    payment_proof = fields.Image(
        string='Comprobante de Pago', max_width=1920, max_height=1920,
        attachment=True, copy=False,
        help='Imagen del comprobante de pago de la comisión, para uso interno. '
             'No se incluye en la impresión enviada al empleado.',
    )
    note = fields.Text(string='Nota')

    @api.depends('base_amount', 'commission_percent')
    def _compute_commission_amount(self):
        for line in self:
            line.commission_amount = line.base_amount * line.commission_percent / 100.0

    @api.depends('move_id.name', 'employee_id.name')
    def _compute_name(self):
        for line in self:
            line.name = '%s - %s' % (line.move_id.name or '', line.employee_id.name or '')

    @api.onchange('move_id')
    def _onchange_move_id(self):
        for line in self:
            if line.move_id:
                line.base_amount = line.move_id.amount_untaxed_signed
                salesperson = line.move_id.invoice_user_id
                if salesperson:
                    line.employee_id = self.env['hr.employee'].search(
                        [('user_id', '=', salesperson.id)], limit=1)

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        for line in self:
            if line.employee_id:
                line.commission_percent = line.employee_id.commission_percent

    def action_mark_paid(self):
        self.write({
            'state': 'paid',
            'payment_date': fields.Date.context_today(self),
        })

    def action_reset_to_pay(self):
        self.write({
            'state': 'to_pay',
            'payment_date': False,
        })

    def action_send_commission_email(self):
        self.ensure_one()
        template = self.env.ref(
            'commission_invoice.mail_template_commission_line', raise_if_not_found=False)
        return {
            'type': 'ir.actions.act_window',
            'name': 'Enviar Comisión por Correo',
            'res_model': 'mail.compose.message',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_model': 'commission.line',
                'default_res_ids': [self.id],
                'default_template_id': template.id if template else False,
                'default_composition_mode': 'comment',
                'default_partner_ids': self.employee_id.work_contact_id.ids,
            },
        }
