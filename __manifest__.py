{
    'name': 'Custom Lot Management',
    'version': '1.0',
    'summary': 'Custom Lot Management',
    'description': """
        Custom Lot Management.
    """,
    'author': 'Khondokar Md. Mehedi Hasan',
    'website': 'https://www.github.com/mehedi360272',
    'depends': ['base', 'stock', 'mrp'],
    'data': [
        # security
        'security/ir.model.access.csv',
        # views
        'views/jml_supplier_source_view.xml',
        'views/jml_inherit_stock_lot_view.xml',
        'views/jml_inherit_product_template_view.xml',
        'views/jml_mrp_warning_wizard.xml',
        'views/jml_inherit_product_product_view.xml',
        'views/jml_stock_move_line_view.xml',
        'views/menu.xml',
        # data
        'data/ir_sequence_data.xml',
    ],
    'installable': True,
    'application': False,
}
