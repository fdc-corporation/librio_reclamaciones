import base64
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from odoo import http
from odoo.http import request

class ReclamacionController(http.Controller):

    @http.route(['/reclamacion'], type='http', auth="public", website=True)
    def reclamacion_form(self, **post):
        return request.render('librio_reclamaciones.formulario_reclamacion', {})

    @http.route(['/enviar_reclamacion'], type='http', auth="public", website=True, methods=['POST'])
    def enviar_reclamacion(self, **post):
        archivo = post.get('archivo_adjunto')

        archivo_base64 = None
        archivo_nombre = None
        if archivo:
            archivo_base64 = base64.b64encode(archivo.read()).decode('utf-8')
            archivo_nombre = archivo.filename

        reclamacion = request.env['reclamacion'].sudo().create({
            'name': post.get('name'),
            'name_padre': post.get('name_padre'),
            'tipo_documento': post.get('tipo_documento'),
            'numero_documento': post.get('numero_documento'),
            'telefono': post.get('telefono'),
            'correo': post.get('correo'),
            'domicilio': post.get('domicilio'),
            'tipo_bien': post.get('tipo_bien'),
            'monto_reclamado': post.get('monto_reclamado'),
            'descripcion': post.get('descripcion'),
            'tipo_reclamo': post.get('tipo_reclamo'),
            'detalle_reclamo': post.get('detalle_reclamo'),
            'pedido': post.get('pedido'),
            'acciones': post.get('acciones'),
            'archivo_adjunto': archivo_base64,
            'archivo_adjunto_filename': archivo_nombre,
            'check_1': True if post.get('check_1') == 'on' else False,
            'check_2': True if post.get('check_2') == 'on' else False,
        })


        destino = post.get('correo')

        self.enviar_correo_personalizado(post, reclamacion, destino)

        return request.redirect('/contactus-thank-you')

    def enviar_correo_personalizado(self, post, reclamacion, destino):
        smtp_server = "smtp.hostinger.com"
        smtp_port = 465
        smtp_username = "fdccorp@fdc-corporation.com"
        smtp_password = "Fdc@2024"
        cc_email = "fgutierrez@fdc-corporation.com"
        from_email = smtp_username
        to_email = destino
        subject = f"Reclamación de {reclamacion.name}"
        body = f"""
<html>
<body style="font-family: Arial, sans-serif; color: #333;">
    <div style="background-color: #f7f7f7; padding: 20px; border-radius: 10px;">
        <img src="https://pormayor.pe/web/image/website/1/logo/Pormayor.pe?unique=a2f6206" />
        <h2 style="color: #4CAF50;">Nueva Reclamación Recibida</h2>
        <p>Estimado/a <strong>{reclamacion.name}</strong>,</p>
        <p>Hemos recibido tu reclamación con los siguientes detalles:</p>
        <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
            <tr>
                <td style="padding: 10px; border: 1px solid #ddd;"><strong>Identificador:</strong></td>
                <td style="padding: 10px; border: 1px solid #ddd;">{reclamacion.sequence}</td>
            </tr>
            <tr>
                <td style="padding: 10px; border: 1px solid #ddd;"><strong>Nombre:</strong></td>
                <td style="padding: 10px; border: 1px solid #ddd;">{reclamacion.name}</td>
            </tr>
            <tr>
                <td style="padding: 10px; border: 1px solid #ddd;"><strong>Teléfono:</strong></td>
                <td style="padding: 10px; border: 1px solid #ddd;">{reclamacion.telefono}</td>
            </tr>
            <tr>
                <td style="padding: 10px; border: 1px solid #ddd;"><strong>Correo:</strong></td>
                <td style="padding: 10px; border: 1px solid #ddd;">{reclamacion.correo}</td>
            </tr>
            <tr>
                <td style="padding: 10px; border: 1px solid #ddd;"><strong>Descripción:</strong></td>
                <td style="padding: 10px; border: 1px solid #ddd;">{reclamacion.descripcion}</td>
            </tr>
            <tr>
                <td style="padding: 10px; border: 1px solid #ddd;"><strong>Monto reclamado:</strong></td>
                <td style="padding: 10px; border: 1px solid #ddd;">{reclamacion.monto_reclamado}</td>
            </tr>
        </table>
        <p style="margin-top: 20px;">Nos pondremos en contacto contigo lo antes posible para resolver este asunto.</p>
        <p style="margin-top: 20px;">Atentamente,<br>El equipo de Atención al Cliente</p>
    </div>
</body>
</html>
"""

        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))
        recipients = [to_email] + [cc_email]
        try:
            server = smtplib.SMTP_SSL(smtp_server, smtp_port)
            server.login(smtp_username, smtp_password)

            # Enviar el correo a todos los destinatarios (incluyendo el CC)
            server.sendmail(from_email, recipients, msg.as_string())
            print("Correo enviado exitosamente")
        except Exception as e:
            print(f"Error enviando el correo: {e}")
        finally:
            server.quit()




