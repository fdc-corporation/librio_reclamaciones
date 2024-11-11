from odoo import models, fields, api

class Reclamacion(models.Model):
    _name = 'reclamacion'
    _description = 'Reclamaciones'

    
    name = fields.Char(string="Nombre(s) y Apellidos", required=True)
    name_padre = fields.Char(string="Nombre de padre, madre o apoderado")
    tipo_documento = fields.Selection([('dni', 'DNI'), ('ce', 'CE')], string="Tipo de documento", required=True)
    numero_documento = fields.Char(string="Número de documento", required=True)
    telefono = fields.Char(string="Número de teléfono", required=True)
    correo = fields.Char(string="Correo electrónico", required=True)
    domicilio = fields.Text(string="Domicilio", required=True)
    tipo_bien = fields.Selection([('producto', 'Producto'), ('servicio', 'Servicio')], string="Tipo de bien", required=True)
    monto_reclamado = fields.Float(string="Monto reclamado S/", required=True)
    descripcion = fields.Text(string="Descripción", required=True)
    tipo_reclamo = fields.Selection([('reclamo', 'Reclamo'), ('queja', 'Queja')], string="Tipo de Reclamo", required=True)
    detalle_reclamo = fields.Text(string="Detalle del Reclamo o Queja")
    pedido = fields.Text(string="Pedido (¿Qué es lo que nos solicitas?)")
    acciones = fields.Text(string="Acciones del proveedor")
    archivo_adjunto = fields.Binary(string="Archivo adjunto")
    archivo_adjunto_filename = fields.Char(string="Nombre del archivo adjunto")
    check_1 = fields.Boolean(string="Confirmo que soy el titular del servicio", required=True)
    check_2 = fields.Boolean(string="Confirmo que conozco mis derechos", required=True)
    sequence = fields.Char(string="Número de Reclamación", required=True, copy=False, readonly=True, index=True, default=lambda self: 'Nuevo')
    
    @api.model
    def create(self, vals):
        if vals.get('sequence', 'Nuevo') == 'Nuevo':
            vals['sequence'] = self.env['ir.sequence'].next_by_code('reclamacion.sequence') or 'Nuevo'
        return super(Reclamacion, self).create(vals)
