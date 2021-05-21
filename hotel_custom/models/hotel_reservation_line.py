# -*- coding: utf-8 -*-

from datetime import datetime

from odoo import models, fields


class HotelReservationLine(models.Model):
    _inherit = 'hotel.reservation.line'

    owner_id = fields.Many2one(related='room_number.owner_id')
    sub_total1 = fields.Float(string='Due Amount', compute=False, readonly=False)


class HotelReservation(models.Model):
    _inherit = 'hotel.reservation'

    def create_folio(self):
        for reservation in self:
            room_his_id_search = self.env['hotel.room.booking.history'].search(
                [('booking_id', '=', reservation.id)])
            room_his_id_search.unlink()
            if not reservation.reservation_line:
                raise Warning("Reservation line Details are missing.")
            for line in reservation.reservation_line:
                room_line_id = self.env['hotel.room'].search(
                    [('product_id', '=', line.room_number.id)])
                ###############################################by pornima######
                housekeeping_room = self.env['hotel.housekeeping'].search(
                    [('room_no', '=', room_line_id.product_id.id), ('state', '=', 'dirty')])
                # "housekeeping_room--------------------------------------------------------------------",housekeeping_room
                if housekeeping_room:
                    for house1 in housekeeping_room:
                        house_brw = self.env[
                            'hotel.housekeeping'].browse(house1)
                        house = house_brw.id
                        house_current_date = (
                            datetime.strptime(str(house.current_date), '%Y-%m-%d')).date()
                        house_end_date = (
                            datetime.strptime(str(house.end_date), '%Y-%m-%d')).date()
                        start_reser = datetime.strptime(
                            str(line.checkin), '%Y-%m-%d %H:%M:%S').date()
                        end_reser = datetime.strptime(
                            str(line.checkout), '%Y-%m-%d %H:%M:%S').date()
                        if (house_current_date <= start_reser <= house_end_date) or (
                                house_current_date <= end_reser <= house_end_date) or (
                                (start_reser < house_current_date) and (end_reser > house_end_date)):
                            # if (((start_reser < house_current_date) and (end_reser > house_end_date)) or (house_current_date <= start_reser < house_end_date) or (house_current_date < end_reser <= house_end_date)) :
                            # print "i am in if loop--------------\n\n\n\n\n"
                            raise Warning("Room  %s is not clean for reservation period !") % (
                                room_line_id.name)

                ###############################################

                if room_line_id.room_folio_ids:
                    for history in room_line_id.room_folio_ids:
                        if history.state == 'done':
                            history_start_date = history.check_in
                            history_end_date = history.check_out
                            reservation_start_date = line.checkin
                            reservation_end_date = line.checkout
                            if (history_start_date <= reservation_start_date < history_end_date) or (
                                    history_start_date < reservation_end_date <= history_end_date) or (
                                    (reservation_start_date < history_start_date) and (
                                    reservation_end_date > history_end_date)):
                                # print "Already Reserved......."
                                if not (reservation.id == history.booking_id.id):
                                    raise Warning("Room  %s is booked in this reservation period !" % (
                                        room_line_id.name,))

            line = reservation.reservation_line
            folio = self.env['hotel.folio'].create({
                'date_order': reservation.date_order,
                'shop_id': reservation.shop_id.id,
                'partner_id': reservation.partner_id.id,
                'pricelist_id': reservation.pricelist_id.id,
                'partner_invoice_id': reservation.partner_id.id,
                'partner_shipping_id': reservation.partner_id.id,

                #                 'checkin_date': line.checkin,
                #                 'checkout_date': line.checkout,
                'reservation_id': reservation.id,
                # 'duration': line1.number_of_days,
                'note': reservation.note,

            })
            for line in reservation.reservation_line:
                room_line_id = self.env['hotel.room'].search(
                    [('product_id', '=', line.room_number.id)])
                room_his_id = self.env['hotel.room.booking.history'].create({

                    'partner_id': reservation.partner_id.id,
                    'check_in': line.checkin,
                    'check_out': line.checkout,
                    'history_id': room_line_id.id,
                    'product_id': line.room_number.id,
                    'booking_id': reservation.id,
                    'state': 'done',
                    'category_id': line.room_number.categ_id.id,  # room_line_id.categ_id.id,
                    'name': line.room_number.name,
                    'check_in_date': line.checkin,
                    'check_out_date': line.checkout,
                })
                tax_ids = []
                for tax_line in line.taxes_id:
                    tax_ids.append(tax_line.id)
                vals = {
                    'folio_id': folio.id,
                    'product_id': line.room_number.id,
                    'name': line.room_number.name,
                    'product_uom': line.room_number.uom_id.id,
                    'price_unit': line.sub_total1,
                    # 'price_subtotal': line.sub_total1,
                    'product_uom_qty': 1,
                    'checkin_date': line.checkin,
                    'checkout_date': line.checkout,
                    'discount': line.discount,
                    'tax_id': [(6, 0, tax_ids)],
                    'categ_id': line.room_number.categ_id.id,  # room_line_id.categ_id.id,
                    'hotel_reservation_line_id': line.id

                }

                self.env["hotel_folio.line"].create(vals)
            for rec_id in reservation.id_line_ids:
                rec_id.write({'folio_id': folio.id})
            for mv in reservation.account_move_ids:
                self._cr.execute('insert into sale_account_move_rel(sale_id,move_id) values (%s,%s)',
                                 (folio.order_id.id, mv.id))

            reservation.write(
                {'state': 'done', 'agent_comm': reservation.total_cost1, })
        return True
