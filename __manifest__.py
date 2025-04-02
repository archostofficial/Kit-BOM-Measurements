{
    'name': 'Kit BOM Measurements',
    'version': '1.0',
    'summary': 'Automatic calculation of weight and volume for kit BOMs',
    'description': """
        This module automatically calculates and updates the weight and volume 
        of products with kit BOMs (phantom BOMs) based on their components.
    """,
    'category': 'Manufacturing',
    'author': 'Custom',
    'depends': ['mrp', 'stock'],
    'data': [
        'views/product_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
