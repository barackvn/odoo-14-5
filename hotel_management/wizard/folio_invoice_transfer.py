from odoo import fields, models
from odoo.exceptions import ValidationError


class folio_invoice_transfer_wizard(models.TransientModel):
    _name = 'folio.invoice.transfer.wizard'
    _description = 'Folio invoice transfer Wizard'

    folio_id = fields.Many2one(
        'hotel.folio', 'Folio Ref', default=lambda self: self._get_default_rec())
    trans_folio_id = fields.Many2one(
        'hotel.folio', 'Transfer Folio Ref', domain="[('state', 'not in', ['check_out','done','cancel'])]", )

    def _get_default_rec(self):
        print(self._context, 'ffffffffffffffffffffffffffffffffffff')
        res = {}
        if 'by_dashbord' in self._context and self._context.get('by_dashbord'):
            hotel_folio_id = self.env['hotel.folio'].search([('reservation_id', '=', self._context['active_id'])])
            if hotel_folio_id:
                res = hotel_folio_id.id
                return res
        if self._context is None:
            self._context = {}
        if 'active_id' in self._context:
            print(self._context, '=================context=======')
            res = self._context['active_id']
            print(res, "res=====================")
        return res

    def transfer_process(self):
        for obj in self.browse(self._ids):
            if obj.trans_folio_id:
                if obj.trans_folio_id.partner_id.id == obj.folio_id.partner_id.id:
                    raise ValidationError("Error !, Invoice can't be transfer as both folio partner is same !")
            folio = self.env['hotel.folio'].browse(obj.folio_id.id)
            so = self.env['sale.order'].browse(folio.order_id.id)
            data = so._create_invoices()
            for line in so.order_line:
                if line.product_id.owner_id:
                    vals = {
                        'name': 'New',
                        'date_order': so.date_order,
                        'date_planned': so.date_order,
                        'partner_id': line.product_id.owner_id.id,
                        'user_id': so.user_id.id,
                        'company_id': so.company_id.id,
                        'currency_id': so.currency_id.id,
                        'origin': so.name,
                        'order_line': [(0, 0, {
                            'product_id': line.product_id.id,
                            'sequence': line.sequence,
                            'product_qty': line.product_uom_qty,
                            'price_unit': line.price_unit,
                            'product_uom': line.product_uom.id,
                            'display_type': False,
                        })]
                    }

                    purchase_order = self.env['purchase.order'].sudo().create(vals)
                    purchase_order.button_confirm()
                    purchase_order.action_create_invoice()
            for acc_id in data:
                acc_obj = self.env["account.move"].browse(acc_id)
                obj.folio_id.write({'state': 'progress'})
                if obj.trans_folio_id:
                    if obj.trans_folio_id.partner_id.id != obj.folio_id.partner_id.id:
                        acc_obj.write({'partner_id': obj.trans_folio_id.partner_id.id})

                    self._cr.execute(
                        'insert into sale_transfer_account_invoice_rel (sale_id,invoice_id) values (%s,%s)', (
                            obj.trans_folio_id.order_id.id, data[0]))

        return {'type': 'ir.actions.act_window_close'}


class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_post(self):
        sale_order_names = self.mapped('invoice_line_ids.sale_line_ids.order_id.name')
        res = super(AccountMove, self).action_post()
        self.env['purchase.order'].search([('origin', 'in', sale_order_names)]).mapped('invoice_ids')._post(soft=False)
        return res
