{
    'name': 'Comisiones por Facturas Pagadas',
    'version': '18.0.1.0.0',
    'summary': 'Calcula comisiones por porcentaje sobre facturas de cliente pagadas',
    'description': """
Comisiones sobre facturas pagadas
=================================

Genera automáticamente una línea de comisión para el empleado vinculado
al vendedor de cada factura de cliente cuando ésta queda totalmente
pagada, aplicando el porcentaje de comisión configurado en su ficha de
empleado sobre el monto sin impuestos de la factura. También permite
crear comisiones manualmente.

Incluye:
- Porcentaje de comisión configurable por empleado (módulo de Empleados).
- Generación automática de comisiones al cobrar las facturas.
- Creación y edición manual de comisiones.
- Listado, búsqueda y análisis (pivote) de comisiones.
- Marcado de comisiones como pagadas al empleado.
- Botón de acceso directo a las comisiones desde la factura.
""",
    'category': 'Accounting/Accounting',
    'author': 'Anabel Chai Consultoría',
    'license': 'LGPL-3',
    'depends': ['account', 'hr'],
    'data': [
        'security/ir.model.access.csv',
        'report/commission_line_report_actions.xml',
        'report/commission_line_report_templates.xml',
        'data/mail_template_data.xml',
        'views/commission_line_views.xml',
        'views/hr_employee_views.xml',
        'views/account_move_views.xml',
        'views/commission_menus.xml',
    ],
    'installable': True,
    'application': True,
}
