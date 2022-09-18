
{
    'name': 'Access Restriction By IP and MAC',
    'summary': """User Can Access His Account Only From Specified IP Address AND MAC""",
    'version': '14.0.1.0.0',
    'description': """User Can Access His Account Only From Specified IP Address AND MAC """,
    "live_test_url": 'https://youtu.be/t4jwndbdAMc',
    'author': 'Enzapps Private Limited',
    'company': 'Enzapps Private Limited',
    'website': 'https://www.enzapps.com',
    'category': 'Tools',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/allowed_ips_view.xml',
    ],
    'images': ['static/description/banner.png','static/description/icon.png'],
    'installable': True,
    'auto_install': False,
    "price": '200',
    "currency": 'USD',
}

