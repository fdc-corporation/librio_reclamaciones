{
    'name': 'Formulario de Reclamaciones',
    'version': '1.0',
    'summary': 'Módulo para gestionar reclamaciones desde un formulario en el sitio web',
    'description': """
    Este módulo permite a los usuarios realizar reclamaciones a través de un formulario en el sitio web. 
    Las reclamaciones se almacenan en el sistema y se envía un correo de notificación con los detalles.
    """,
    'category': 'Website',
    'author': 'Tu Empresa',
    'website': 'https://www.tuempresa.com',
    'depends': ['website', 'mail'],  # Asegúrate de tener estas dependencias
    'data': [
        'views/ir.sequence.xml',  # Este archivo debe cargarse antes de las vistas
        'security/ir.model.access.csv',  # Añadir la ruta del archivo de permisos
        'views/formulario.xml',  # Vista QWeb para el formulario en la web
        'views/view.xml',  # Plantilla de correo
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
