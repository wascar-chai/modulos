{
    'name': 'Formato Profesional de Ventas y Facturas',
    'version': '18.0.1.0.0',
    'summary': 'Rediseño visual de los reportes de cotizaciones, pedidos y facturas',
    'category': 'Technical',
    'license': 'LGPL-3',
    'depends': ['sale', 'account'],
    'data': [
        'views/sale_report_templates.xml',
        'views/account_report_templates.xml',
    ],
    'installable': True,
    'application': False,
}
