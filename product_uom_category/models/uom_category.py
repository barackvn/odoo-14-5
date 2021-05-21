# -*- coding: utf-8 -*-


from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError


class ProductUOMCategory(models.Model):
    _inherit = "product.template"
    
    #get the first category as a default to be assigned to uom_categ_id
    def _get_default_uom_categ_id(self):
        return self.env["uom.category"].search([], limit=1, order='id').id
    
    #Add UOM Category field tp product.template 
    uom_categ_id=fields.Many2one(
        'uom.category', 'UOM Category', required=True,
        default=_get_default_uom_categ_id,help="UOM Category.")

    #add constrains on uom_categ_id 
    @api.constrains('uom_categ_id')
    def _check_uomcategory(self):
        # if the uom_id and uom_po_id not form the same category selected in uom_categ_id fields then raise an error.
        if any(template.uom_categ_id and  template.uom_id.category_id != template.uom_categ_id and template.uom_po_id.category_id != template.uom_categ_id  for template in self):
            raise ValidationError(_('Error: The default Unit of Measure and the purchase Unit of Measure must be in the same category of uom category field.'))
        return True


    @api.onchange('uom_categ_id')
    def onchange_uom_categ_id(self):
        domain = [('category_id', '=', self.uom_categ_id.id)]
        return {'domain': {
            'uom_id': domain, 'uom_po_id': domain
        }}

    @api.model
    def create(self, vals):
        if 'can_be_expensed' in vals:
            uom_id = self.env["uom.uom"].browse(vals.get('uom_id'))
            vals['uom_categ_id'] = uom_id.category_id.id if vals.get('can_be_expensed', False) else vals['uom_categ_id']
        return super(ProductUOMCategory, self).create(vals)


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.onchange('uom_categ_id')
    def onchange_uom_categ(self):
        domain = [('category_id', '=', self.uom_categ_id.id)]
        return {'domain': {
            'uom_id': domain, 'uom_po_id': domain
        }}