# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.http import request
import qrcode
import base64
from io import BytesIO


def generate_product_sku(data):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=20, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image()
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue())
    return img_str


class Product(models.Model):
    _inherit = 'product.template'

    qr_product = fields.Binary('QR Product', readonly=True)

    @api.one
    def action_make_product_qrcode(self):
        base_url = request.env['ir.config_parameter'].get_param('web.base.url')
        base_url += '/shop/product/%s' % self.id
        self.qr_product = generate_product_sku(base_url)


class QRSaleOrder(models.Model):
    _inherit = 'sale.order'

    qr_image = fields.Binary('QR Code', compute='_generate_qr_code')
    qr_in_report = fields.Boolean('Show QR in Report')

    @api.one
    def _generate_qr_code(self):
        base_url = request.env['ir.config_parameter'].get_param('web.base.url')
        base_url += '/shop/product/%s' % self.id
        self.qr_image = generate_product_sku(base_url)






