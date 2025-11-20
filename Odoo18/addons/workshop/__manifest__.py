{
    'name': 'Workshop',
    'module_name': 'workshop',
    'version': '18.0',
    'author': 'varoESP',
    'category': 'Education',
    'depends': ['base','product'],
    'data': [
        'security/ir.model.access.csv',
        'views/workshop_customer_views.xml',
        'views/workshop_employee_views.xml',
        'views/workshop_product_views.xml',
        'views/workshop_vehicle_views.xml',
        'views/workshop_menus.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
