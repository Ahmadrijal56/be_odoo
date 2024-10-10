{
    'name': 'User Registration API',
    'version': '1.0',
    'category': 'Authentication',
    'summary': 'API for User Registration from Mobile App and Backend Management',
    'description': 'This module provides an API endpoint for user registration and allows backend management of users.',
    'author': 'Your Name',
    'depends': ['base'],
    'data': [
        'views/user_views.xml',  # Include the view file
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
}
