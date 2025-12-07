{
    'name': 'Workshop',
    'version': '18.0',
    'author': 'varoESP',
    'category': 'Education',
    'depends': ['base','product', 'hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/workshop_customer_views.xml',
        'views/workshop_employee_views.xml',
        'views/workshop_product_views.xml',
        'views/workshop_vehicle_views.xml',
        'views/workshop_maintenance_views.xml',
        'views/workshop_menus.xml'
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'license': 'LGPL-3'
}
