from odoo import http
from werkzeug.exceptions import Forbidden
from odoo.http import request
from datetime import datetime
import logging
from odoo import tools
import time
import werkzeug.urls
from werkzeug.exceptions import NotFound
from dateutil.relativedelta import relativedelta

from odoo.osv import expression
from odoo.tools.translate import _
from odoo import fields, models, api
import hashlib
import json
import ast
from odoo import SUPERUSER_ID
from odoo.exceptions import ValidationError, Warning, UserError
from builtins import int

_logger = logging.getLogger(__name__)


class check(http.Controller):
    #
    @http.route(['/page/hotel_online.product_show', '/page/product_show'], auth="public", website=True)
    def contact(self, **kwargs):
        #         print "*********** contact ***********",self
        values = {}
        #         print "values-",values
        return request.render("hotel_online.product_show", values)

    @http.route('/product_screen/', type='http', auth='public', website=True)
    def get_products(self):
        #         print "*********** get_product ***********",self
        result = {}
        values = {'product': False}
        #         print "values",values
        return http.local_redirect("/page/hotel_online.product_show", values)

    @http.route('/product_search/', auth='public', website=True)
    def search_products(self, **kwargs):
        print("*********** Search Product ***********", self, kwargs)
        lst = []
        res1 = []
        res = []
        room_ids1 = []
        room_res = {}
        cnt = 0
        result_list11 = []
        count = []
        result = {}
        rm_brw = []
        date_values = list(kwargs.values())
        if not (kwargs['from_date'] and kwargs['to_date']):
            raise Warning("Please Enter Checkin Date And Checkout Date")
        self._uid = SUPERUSER_ID
        product_id = request.env['product.product'].sudo().search([]).ids
        room_idsss = request.env['hotel.room_type'].sudo().search([]).ids
        if room_idsss:
            room_res11 = {}
            room_brw = request.env['hotel.room_type'].sudo().browse(room_idsss)
            for rbrw in room_brw:
                room_res11 = {}
                res = []
                res1 = []
                img_lst = []
                img_lst_ids = []
                room_res11['type'] = rbrw.name,
                room_res11['description'] = rbrw.description
                img_lst = rbrw.img_ids
                user = request.env['res.users'].sudo().browse(request.uid)
                company = request.env.user.sudo().company_id
                if kwargs['from_date'] and kwargs['to_date']:
                    room_res11['chkin'] = kwargs['from_date']
                    room_res11['chkout'] = kwargs['to_date']
                for i in img_lst:
                    img_lst_ids.append(i.id)
                if rbrw.img_ids:
                    room_res11['image'] = img_lst_ids
                #                     room_res11['image'] = pool.get('hotel.room.images').browse(cr, SUPERUSER_ID,rbrw.img_ids[0].id, context=context)

                else:
                    room_res11['image'] = ''
                room_ids111 = request.env['hotel.room'].sudo().search([]).ids
                if room_ids111:
                    room_br11 = request.env['hotel.room'].sudo().browse(room_ids111)
                    room_ids1 = []
                    room_res11['room_type_id'] = rbrw.id
                    shop_ids = request.env['sale.shop'].sudo().search(
                        [('company_id', '=', request.env.user.sudo().company_id.id)]).ids
                    shop_brw = request.env['sale.shop'].sudo().browse(shop_ids[0])
                    room_res11['currency'] = shop_brw.pricelist_id.currency_id.symbol
                    for r in room_br11:
                        if r.product_id.product_tmpl_id.categ_id == rbrw.cat_id:
                            room_ids1.append(r.id)
                            print("room_ids1--", room_ids1)
                for rm in room_ids1:
                    rm1 = request.env['hotel.room'].sudo().browse(rm)
                    print("rmmmmmmmmmmm111111", rm1)
                    price1 = shop_brw.sudo().pricelist_id.price_get(
                        rm1.product_id.id, False, {
                            'uom': rm1.product_id.uom_id.id,
                            'date': kwargs['from_date'],
                        })[shop_brw.pricelist_id.id]
                    print("priceee1", price1)
                    room_res11['price'] = round(price1, 2)
                    book_his = request.env['hotel.room.booking.history'].sudo().search([('history_id', '=', rm)]).ids
                    print("boooooook_his", book_his)
                    if book_his:
                        room_book = ''
                        book_brw = request.env['hotel.room.booking.history'].sudo().browse(book_his)
                        print("booooooking browsee", book_brw)
                        for bk_his in book_brw:
                            start_date = datetime.strptime(kwargs['from_date'], '%m/%d/%Y').date()
                            end_date = datetime.strptime(kwargs['to_date'], '%m/%d/%Y').date()
                            chkin_date = datetime.strptime(str(bk_his.check_in), '%Y-%m-%d %H:%M:%S').date()
                            chkout_date = datetime.strptime(str(bk_his.check_out), '%Y-%m-%d %H:%M:%S').date()
                            #                                 if((start_date <= chkin_date and chkout_date <= end_date)or(start_date <= chkin_date and chkout_date >= end_date>chkin_date) or (start_date >= chkin_date and chkout_date >= end_date)or (start_date >= chkin_date and chkout_date >= end_date)):
                            print("start_date--", start_date, "--end_date--", end_date, "--chkin_date--", chkin_date,
                                  "--chkout_date--", chkout_date)
                            if ((start_date <= chkin_date and (
                                    chkout_date <= end_date or chkout_date >= end_date >= chkin_date)) or (
                                    start_date >= chkin_date and chkout_date >= end_date) or (
                                    start_date <= chkout_date <= end_date)):
                                room_book = bk_his.history_id
                                print("room_book = ", room_book)
                                break
                            else:
                                if not bk_his.history_id in lst:
                                    lst.append(bk_his.history_id)
                                    print("------------lst-------", lst)
                        if room_book in lst:
                            lst.remove(room_book)
                            print("----lst---", lst)
                        for l in lst:
                            rm_brw = l
                            housek = request.env['hotel.housekeeping'].sudo().search(
                                [('room_no', '=', rm_brw.product_id.id), ('state', '=', 'dirty')])
                            print("hoooouuuuuuuusssssseeeeeeelllkk", housek)
                            if not housek:
                                if rm_brw.product_id.product_tmpl_id.categ_id == rbrw.cat_id:
                                    if not rm_brw in res1:
                                        res1.append(rm_brw)
                                        print("-----res1------", res1)
                    else:
                        rm_brw = request.env['hotel.room'].sudo().browse(rm)
                        print("room_____broooseeeee----", rm_brw)
                        if rm_brw.product_id.product_tmpl_id.categ_id == rbrw.cat_id:
                            housek = request.env['hotel.housekeeping'].sudo().search(
                                [('room_no', '=', rm_brw.product_id.id), ('state', '=', 'dirty')])
                            print("======housek===", housek)
                            if not housek:
                                res1.append(rm_brw)
                                print("===res1==", res1)
                cnt = 0
                count = []
                adult = []
                child = []

                if rm_brw:

                    for i in range(1, (int(rm_brw[0].max_adult) + 1)):
                        adult.append(i)
                    for i in range(1, (int(rm_brw[0].max_child) + 1)):
                        child.append(i)
                    for r in res1:
                        cnt = cnt + 1
                        count.append(cnt)
                        print("\n\n\ncnt---", cnt, "-------count")
                    #                     print "aduultt--",adult,"--child--",child
                    room_res11['count'] = count,
                    room_res11['adult'] = adult,
                    room_res11['child'] = child,
                    result_list11.append(room_res11)

        print("result_list11:::::::::::::::::", result_list11, count, len(room_idsss))
        values = {

            'length': len(room_idsss),
            'count': count,
            'room_res': result_list11
        }
        # print ("valuesssssssss",values)
        return request.render("hotel_online.product_show", values)

    @http.route(['/page/hotel_online.booking_show', '/page/booking_show'], type='http', auth="public", website=True)
    def contact11(self, **kwargs):
        print("*********** contact11 ***********")
        values = {}
        return request.render("hotel_online.booking_show", values)

    @http.route('/booking_screen/', type='http', auth='pubilc', website=True)
    def get_productsss(self):
        print("*********** get_productsss ***********")
        values = {'product': False}
        return http.local_redirect("/page/hotel_online.booking_show", values)

    @http.route(['/product/reserv/'], type='http', auth="public", website=True)
    def reserv_products(self, **kwargs):
        print("*********** reserv_products ***********", kwargs)
        # cr,  context , pool= request.cr, request.context, request.registry    
        values = {}
        rm_types = []
        room_id123 = []
        room_data = []
        lsttt = []
        cnt = 0
        tot = 0
        tax = 0
        dayss = 0
        res1, lst = [], []
        room_id = ''
        self._uid = SUPERUSER_ID
        user = request.env['res.users'].sudo().browse(request.uid)
        company = request.env.user.sudo().company_id
        part_id = request.env['res.partner'].sudo().search([('name', '=', 'Public user'), ('active', '=', False)])
        shop_ids = request.env['sale.shop'].sudo().search([('company_id', '=', company.id)]).ids
        shop_brw = request.env['sale.shop'].sudo().browse(shop_ids[0])
        if 'chkin_id' in kwargs:
            newdate = kwargs['chkin_id'] + " 00:00:00"
            print("New Date", newdate)
        if 'chkout_id' in kwargs:
            newdate1 = kwargs['chkout_id'] + " 00:00:00"
        dt = datetime.strptime(time.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S').date()
        no = int(kwargs['len']) + 1
        for ll in range(1, int(no)):
            lsttt.append(ll)
        for l1 in lsttt:
            record = {}
            str1 = 'type_' + str(l1)
            str2 = 'child_' + str(l1)
            str3 = 'adult_' + str(l1)
            str4 = 'sel_' + str(l1)
            str5 = 'no_room_' + str(l1)
            if str1 in kwargs:
                record.update({'room_type': int(kwargs[str1])})
            if str2 in kwargs:
                record.update({'child': int(kwargs[str2])})
            if str3 in kwargs:
                record.update({'adult': int(kwargs[str3])})
            if str4 in kwargs:
                record.update({'chk': kwargs[str4]})
            if str5 in kwargs:
                record.update({'no_room': int(kwargs[str5])})
            #             record = {'room_type':int(kwargs[str1]),'child':int(kwargs[str2]),'adult':int(kwargs[str3]),
            #                       'no_room':int(kwargs[str5]),'shk':kwargs[str4]}
            if record:
                rm_types.append(record)
                rm_types
        #         room_idd = request.env['hotel.reservation'].sudo().search([('partner_id', '=', self._uid)])
        #         print request.uid,"rrrrrrrrrrommmmmmmmmmmmmm idddddddddddddd",room_idd
        #         for r in room_idd:
        #
        #             r1 = request.env['hotel.reservation'].sudo().browse(r).id
        #             if datetime.strptime(r1.date_order, '%Y-%m-%d %H:%M:%S').date() == dt:
        #                 room_id123.append(r1.id)
        #             if room_id123:
        #                 room_id = room_id123[0]
        #                 print room_id123[0], "-------------------------room_id123", room_id123
        #         if not room_id:
        room_id = request.env['hotel.reservation'].sudo().create({
            'partner_id': part_id.id,
            'shop_id': shop_ids[0],
            'pricelist_id': shop_brw.pricelist_id.id,
            'source': 'through_web',
            'date_order': time.strftime('%Y-%m-%d %H:%M:%S'),
        })
        print("rooooom_id==================================", room_id.id)
        request.session['reservation_order_id'] = room_id.id
        tot_lines = 0
        for rtype in rm_types:
            room_brwww = request.env['hotel.room_type'].sudo().browse(rtype['room_type'])
            #########################################################################################
            room_ids111 = request.env['hotel.room'].sudo().search([]).ids
            if room_ids111:
                room_br11 = request.env['hotel.room'].sudo().browse(room_ids111)
                room_ids1 = []
                for r in room_br11:
                    housek = request.env['hotel.housekeeping'].sudo().search(
                        [('room_no', '=', r.product_id.id), ('state', '=', 'dirty')]).ids
                    if not housek:
                        if r.product_id.product_tmpl_id.categ_id.id == room_brwww.cat_id.id:
                            room_ids1.append(r.id)
                            print("room_ids1 >>>>>>>>>>>>>>>>>>>>", room_ids1)
            res1 = []
            for rm in room_ids1:
                book_his = request.env['hotel.room.booking.history'].sudo().search([('history_id', '=', rm)]).ids
                if book_his:
                    room_book = ''
                    book_brw = request.env['hotel.room.booking.history'].sudo().browse(book_his)
                    for bk_his in book_brw:

                        if kwargs['chkin_id'] and kwargs['chkout_id']:
                            start_date = datetime.strptime(kwargs['chkin_id'], '%m/%d/%Y').date()
                            print()
                            end_date = datetime.strptime(kwargs['chkout_id'], '%m/%d/%Y').date()
                            chkin_date = datetime.strptime(str(bk_his.check_in), '%Y-%m-%d %H:%M:%S').date()
                            chkout_date = datetime.strptime(str(bk_his.check_out), '%Y-%m-%d %H:%M:%S').date()
                            #                             if not ((start_date <= chkin_date and chkout_date <= end_date)or(start_date <= chkin_date and chkout_date >= end_date) or (start_date >= chkin_date and chkout_date >= end_date)or (start_date >= chkin_date and chkout_date >= end_date)):
                            #                                 lst.append(bk_his.history_id)

                            if ((start_date <= chkin_date and (
                                    chkout_date <= end_date or chkout_date >= end_date >= chkin_date)) or (
                                    start_date >= chkin_date and chkout_date >= end_date) or (
                                    start_date <= chkout_date <= end_date)):
                                room_book = bk_his.history_id
                                break
                            else:
                                if not bk_his.history_id in lst:
                                    lst.append(bk_his.history_id)
                    if room_book in lst:
                        lst.remove(room_book)
                    for l in lst:
                        rm_brw = l
                        if rm_brw.product_id.product_tmpl_id.categ_id == room_brwww.cat_id:
                            if not rm in res1:
                                res1.append(rm_brw)
                else:
                    rm_brw = request.env['hotel.room'].sudo().browse(rm)
                    if rm_brw.product_id.product_tmpl_id.categ_id == room_brwww.cat_id:
                        res1.append(rm_brw)

            if 'no_room' in rtype and 'chk' in rtype:
                if rtype['chk'] == 'on':
                    for lno in range(0, (int(rtype['no_room']))):
                        no_of_days = (datetime.strptime(newdate1, '%m/%d/%Y %H:%M:%S') - datetime.strptime(newdate,
                                                                                                           '%m/%d/%Y %H:%M:%S')).days
                        cin = str(datetime.strptime(newdate, '%m/%d/%Y %H:%M:%S').date())
                        price = shop_brw.sudo().pricelist_id.price_get(
                            res1[lno].product_id.id, no_of_days, {
                                'uom': res1[lno].product_id.uom_id.id,
                                'date': cin,
                            })[shop_brw.pricelist_id.id]
                        print("priceeeeeeeeeeeeeeee, cin  ,no_of_days", price, cin, no_of_days)
                        print("roooOOOOOOOOOOOOOOOOOOOOOOOOoom ", room_id.id)
                        room_line_id = request.env['hotel.reservation.line'].sudo().create({
                            'checkin': datetime.strptime(newdate, '%m/%d/%Y %H:%M:%S'),
                            'checkout': datetime.strptime(newdate1, '%m/%d/%Y %H:%M:%S'),
                            'categ_id': room_brwww.cat_id.id,
                            'room_number': res1[lno].product_id.id,
                            'line_id': room_id.id,
                            'price': price
                        })
                        print("room_line_idddddddd", room_line_id)
            dict = {}
            if 'no_room' in rtype and 'chk' in rtype:
                tot_lines = tot_lines + rtype['no_room']
                print("tot_linesss", tot_lines)
                room_brw = request.env['hotel.room_type'].sudo().browse(rtype['room_type'])
                for lll in range(1, (int(rtype['no_room'] + 1))):
                    dict = {'rm_name': room_brw.name}
                    print("dictionaaaaaaaaaaaaaaary", dict)
                    if room_brw.img_ids:
                        dict.update({'image': room_brw.img_ids[0].id})
                    if 'child' in rtype:
                        dict.update({'child': int(rtype['child'])})
                    if 'adult' in rtype:
                        dict.update({'adult': int(rtype['adult'])})
                    if 'chkin_id' in kwargs:
                        dict.update({'chkin': kwargs['chkin_id']})
                    if 'chkout_id' in kwargs:
                        dict.update({'chkout': kwargs['chkout_id']})
                    delta = (datetime.strptime(newdate1, '%m/%d/%Y %H:%M:%S')) - (
                        datetime.strptime(newdate, '%m/%d/%Y %H:%M:%S'))
                    print("deltaaaaa", delta)
                    dayss = delta.days
                    print("daysssssssss", dayss)
                    if delta:
                        dict.update({'nights': delta.days})
                    dict.update({'img': company.currency_id.symbol})
                    room_search = request.env['hotel.room'].sudo().search([]).ids
                    if room_search:
                        for rm_sear in room_search:
                            rm_brw = request.env['hotel.room'].sudo().browse(rm_sear)
                            if rm_brw.product_id.product_tmpl_id.categ_id.id == room_brw.cat_id.id:
                                price = rm_brw.lst_price
                                tot = tot + rm_brw.lst_price
                                print("tot tot tot tot ", tot)
                                tax = tax + 0.00
                                break
                    dict.update({'price': "%.2f" % price, })
                    room_data.append(dict)
        values = {
            'room_data': room_data,
            'length': tot_lines,
            'tot': "%.2f" % (tot * dayss),
            'tax': "%.2f" % tax,
            'tot_tax': "%.2f" % ((tot * dayss) + tax)}
        print("vaaaaalues", values)
        return request.render("hotel_online.booking_show", values)

    @http.route(['/product_remove/'], type='http', auth="public", website=True)
    def remove_products(self, **kwargs):
        print("*********** remove_products ***********", kwargs)
        values = {}
        i = 0
        tot = 0
        room_data = []
        if 'len' in kwargs:
            data = ast.literal_eval(kwargs['len'])['data']
            for l in data:
                if 'room_type' in kwargs and 'rm_name' in l and str(l['rm_name']) == str(kwargs['room_type']):
                    if 'adult' in kwargs and 'adult' in l and str(l['adult']) == str(kwargs['adult']):
                        if 'child' in kwargs and 'child' in l and str(l['child']) == str(kwargs['child']):
                            data.pop(i)
                            i = i + 1
                            part_id = request.env['res.partner'].sudo().search(
                                [('name', '=', 'Public user'), ('active', '=', False)], limit=1)
                            reserv_se = request.env['hotel.reservation'].sudo().search([('partner_id', '=', part_id)])
                            if reserv_se:
                                for r_sear in reserv_se:
                                    reserv_br = request.env['hotel.reservation'].sudo().browse(r_sear)
                                    if datetime.strptime(reserv_br.date_order,
                                                         '%Y-%m-%d %H:%M:%S').date() == datetime.strptime(
                                            time.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S').date():
                                        if reserv_br.reservation_line:
                                            for rl in reserv_br.reservation_line:
                                                if 'chkin' in kwargs and 'chkout' in kwargs:
                                                    rtse = request.env['hotel.room_type'].sudo().search(
                                                        [('name', '=', kwargs['room_type'])])
                                                    rtypr_br = request.env['hotel.room_type'].sudo().browse(rtse)
                                                    chin = datetime.strptime(rl.checkin, '%Y-%m-%d %H:%M:%S').date()
                                                    kchin = datetime.strptime(kwargs['chkin'], '%Y-%m-%d').date()
                                                    chout = datetime.strptime(rl.checkout, '%Y-%m-%d %H:%M:%S').date()
                                                    kcout = datetime.strptime(kwargs['chkout'], '%Y-%m-%d').date()
                                                    if (chin == kchin and (chout == kcout) and (
                                                            rl.categ_id.id == rtypr_br.cat_id.id)):
                                                        request.env['hotel.reservation.line'].unlink(rl.id)
                                                        break
        for d1 in data:
            tot = tot + d1['price']
        values = {
            'room_data': data,
            'tot': tot}
        return request.render("hotel_online.booking_show", values)

    def checkout_values(self, data=None):
        print("********  checkout valuuuessssss  ********")
        countries = request.env['res.country'].sudo().search([])
        states_ids = request.env['res.country.state'].sudo().search([])
        states = states_ids  # request.env['res.country.state'].sudo().browse([states_ids])
        partner = request.env['res.partner'].sudo().browse(request.uid)
        print("partnerrrrrrrrrrrr", partner)
        order = None

        shipping_id = data and data.get('shipping_id') or None
        shipping_ids = []
        checkout = {}
        if not data:
            if request.uid != request.website.user_id.id:
                checkout.update(self.checkout_parse("billing", partner))
            else:
                order1 = request.website.get_reservation()
                order = request.env['hotel.reservation'].sudo().browse(order1)
                print("order***********", order)
                if order.partner_id:
                    domain = [("partner_id", "=", order.partner_id.id)]
                    print("domainnnnnnnn ", domain)
                    user_ids = request.registry['res.users'].sudo().search(domain)
                    print("user_idssssssssssss", user_ids)
                    if not user_ids or request.website.user_id.id not in user_ids:
                        checkout.update(self.checkout_parse("billing", order.partner_id))
        else:
            checkout = self.checkout_parse('billing', data)
            print("checkouttttttttt ", checkout)

        # Default search by user country
        if not checkout.get('country_id'):
            country_code = request.session['geoip'].get('country_code')
            print("cooooountryy cooode", country_code)
            if country_code:
                country_ids = request.env['res.country'].search([('code', '=', country_code)], limit=1)
                print("country_ids", country_ids)
                if country_ids:
                    checkout['country_id'] = country_ids[0]

        values = {
            'countries': countries,
            'states': states,
            'checkout': checkout,
            'error': {},
            'has_check_vat': hasattr(request.env['res.partner'], 'check_vat'),
            'only_services': order or False
        }
        #         print "valuuuuuuuesssss of checkout_values",values
        return values

    mandatory_billing_fields = ["name", "phone", "email", "street2", "city", "country_id"]
    optional_billing_fields = ["street", "state_id", "vat", "zip"]
    mandatory_shipping_fields = ["name", "phone", "street", "city", "country_id"]
    optional_shipping_fields = ["state_id", "zip"]

    def checkout_parse(self, address_type, data, remove_prefix=False):
        print("________checkout_parse___________", address_type, data)
        """ data is a dict OR a partner browse record
        """
        # set mandatory and optional fields
        assert address_type in ('billing', 'shipping')
        if address_type == 'billing':
            all_fields = self.mandatory_billing_fields + self.optional_billing_fields
            prefix = ''
        else:
            all_fields = self.mandatory_shipping_fields + self.optional_shipping_fields
            prefix = 'shipping_'
        # set data
        if isinstance(data, dict):
            query = dict((prefix + field_name, data[prefix + field_name])
                         for field_name in all_fields if prefix + field_name in data)
        else:
            query = dict((prefix + field_name, getattr(data, field_name))
                         for field_name in all_fields if getattr(data, field_name))
            if address_type == 'billing' and data.parent_id:
                query[prefix + 'street'] = data.parent_id.name

        if query.get(prefix + 'state_id'):
            query[prefix + 'state_id'] = int(query[prefix + 'state_id'])
        if query.get(prefix + 'country_id'):
            query[prefix + 'country_id'] = int(query[prefix + 'country_id'])

        if not remove_prefix:
            return query
        return dict((field_name, data[prefix + field_name]) for field_name in all_fields if prefix + field_name in data)

    #    Validation for billing information
    def checkout_form_validate(self, data):
        print("_____checkout_form_validate______-", data)
        cr, uid, context, registry = request.cr, request.uid, request.context, request.registry

        error = dict()
        error_message = []

        # Validation
        for field_name in self.mandatory_billing_fields:
            if not data.get(field_name):
                error[field_name] = 'missing'

        # email validation
        if data.get('email') and not tools.single_email_re.match(data.get('email')):
            error["email"] = 'error'
            error_message.append(_('Invalid Email! Please enter a valid email address.'))

        # vat validation
        if data.get("vat") and hasattr(registry["res.partner"], "check_vat"):
            if request.website.company_id.vat_check_vies:
                # force full VIES online check
                check_func = registry["res.partner"].vies_vat_check
            else:
                # quick and partial off-line checksum validation
                check_func = registry["res.partner"].simple_vat_check
            vat_country, vat_number = registry["res.partner"]._split_vat(data.get("vat"))
            if not check_func(cr, uid, vat_country, vat_number, context=None):  # simple_vat_check
                error["vat"] = 'error'

        if data.get("shipping_id") == -1:
            for field_name in self.mandatory_shipping_fields:
                field_name = 'shipping_' + field_name
                if not data.get(field_name):
                    error[field_name] = 'missing'
        # error message for empty required fields
        if [err for err in list(error.values()) if err == 'missing']:
            error_message.append(_('Some required fields are empty.'))
        return error, error_message

    def checkout_form_save(self, checkout):
        print("\n\n\n\n\n$$$$$$$$$---checkout_form_save----$$$$$$$$$", checkout)
        #         cr, uid, context, registry = request.cr, request.uid, request.context, request.registry
        order1 = request.website.get_reservation()
        order = request.env['hotel.reservation'].sudo().browse(order1)
        print("Checkout from save Order ID", order)
        #         order = request.website.get_reservation()
        orm_partner = request.env['res.partner']
        orm_user = request.env['res.users']
        order_obj = request.env['hotel.reservation']

        #         partner_lang = request.lang if request.lang in [lang.code for lang in request.website.language_ids] else None
        #         print "partner_lang", partner_lang
        partner_lang = request.lang if request.lang in request.website.mapped('language_ids.code') else None
        print("Languaaaaggee", partner_lang)
        billing_info = {}
        if partner_lang:
            billing_info['lang'] = partner_lang
        billing_info.update(self.checkout_parse('billing', checkout, True))
        print("billing_info00000000000oooo", billing_info)

        # set partner_id
        partner_id = None
        if request.uid != request.website.user_id.id:
            #             partner_id = orm_user.browse(cr, SUPERUSER_ID, uid, context=context).partner_id.id
            partner_id = orm_user.sudo().browse(request.uid).id
            print("\n\nPartnerrrrrr Id of checkout_form_save ", partner_id)
        elif order.partner_id:
            user_ids = request.registry['res.users'].search(
                [("partner_id", "=", order.partner_id.id)])
            print("\nUuuuuserrrr id", user_ids)
            if not user_ids or request.website.user_id.id not in user_ids:
                partner_id = order.partner_id.id
                print("Paaaaaaaaaartneeeeeeeeeer Id", partner_id)

        # save partner informations
        if billing_info.get('country_id'):
            billing_info['property_account_position_id'] = request.env[
                'account.fiscal.position'].sudo()._get_fpos_by_region(
                billing_info['country_id'], billing_info.get('state_id') or False, billing_info.get('zip'),
                                            billing_info.get('vat') and True or False)
            print("billing_infoooooooooooooooooooooooooooooooooo", billing_info)
        if partner_id and request.website.partner_id.id != partner_id:
            partner_id1 = orm_partner.browse(partner_id)
            print("Paaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaartner", partner_id1)
            valiee = partner_id1.write(billing_info)
            print("write valueeeeeeeee billlinggggggggggggggggg", valiee)
        else:
            # create partner
            partner_id = billing_info.sudo().create(billing_info)
            print("creeeeeeeeeeeeeeateee partner ", partner_id)
        order.write({'partner_id': partner_id})
        order_info = {
            'message_partner_ids': [(4, partner_id), (3, request.website.partner_id.id)],
        }
        print("order_infooooooooooo", order_info)
        zz = order_obj.sudo().write(order_info)

        print("write order indoo ", zz)

    @http.route(['/page/hotel_online.booking_show', '/partner/checkout'], type='http', auth="public", website=True)
    def checkout(self, **post):
        print(self, " ^^^^^^^^ checkout ^^^^^^ ", post)
        cr, context = request.cr, request.context

        reservation = request.website.get_reservation()
        print("reservationnnnnnnnnn", reservation)
        redirection = self.checkout_redirection(reservation)
        print("=====redirection ", redirection)
        if redirection:
            return redirection

        values = self.checkout_values()
        print("valueeeessss", values)

        return request.render("hotel_online.res_partner_show", values)

    @http.route('/partner/checkout', type='http', auth='public', website=True)
    def get_product_res(self):
        print("######get_product_res######")
        values = {'product': False}
        return http.local_redirect("/page/hotel_online.res_partner_show", values)

    @http.route(['/partner_add/'], type='http', auth="public", website=True, csrf=False)
    def confirm_order(self, **post):
        print("\n\n\n\n+++++++++++++++++confirm_order++++++++++++++++++++++++++++++++", post)
        order = request.website.get_reservation()
        print("OOOOOOOOOOOrderrr", order)
        if not order:
            return request.redirect("/shop")
        redirection = self.checkout_redirection(order)
        print("redirectionnnnnnnnnnnn-------", redirection)
        if redirection:
            return redirection

        values = self.checkout_values(post)
        print("values-->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>--", values)
        values["error"], values["error_message"] = self.checkout_form_validate(values["checkout"])
        if values["error"]:
            return request.render("hotel_online.res_partner_show", values)

        self.checkout_form_save(values["checkout"])
        return request.redirect("/shop/payment")

    #     @http.route(['/shop/payment'], type='http', auth="public", website=True)
    #     def payment(self, **post):
    #         print("******-------payment------*******",post)
    #         """ Payment step. This page proposes several payment means based on available
    #         payment.acquirer. State at this point :
    #
    #          - a draft sale order with lines; otherwise, clean context / session and
    #            back to the shop
    #          - no transaction in context / session, or only a draft one, if the customer
    #            did go to a payment.acquirer website but closed the tab without
    #            paying / canceling
    #         """
    #
    #         order = request.website.get_reservation()
    #
    #         order_browse = request.env['hotel.reservation'].sudo().browse(order)
    #         redirection = self.checkout_redirection(order)
    #         if redirection:
    #             return redirection
    #
    #         values = {
    #             'order': order,
    #             'order_browse':order_browse
    #         }
    #         context = {}
    #         context.update({'order': order})
    #         print("*******************context",context)
    #         print("values in payment",values)
    #         ord = order
    #         ord = request.env['hotel.reservation'].sudo().browse(order)
    #         acquirers = request.env['payment.acquirer'].sudo().search([('company_id', '=', ord.company_id.id)])
    # #         acquirers = [aquire_ids.id for aquire_ids  in request.env['payment.acquirer'].sudo().search([ ('company_id', '=', ord.company_id.id)])]
    #         print("acquirerssssssssssss",acquirers)
    #         print("@@@@@@@@@@@@@@@@@@@@@@name",ord.reservation_no,"Totaal Cost",ord.total_cost1)
    #         print("partner id",ord.partner_id.id,"currency ID",ord.pricelist_id.currency_id.id)
    #         render_ctx = dict(context=context, submit_class='btn btn-primary', submit_txt=_('Pay Now') )
    #         print("render_ctx.........>>>>>>",render_ctx)
    #         #render_ctx = dict(submit_class='btn btn-primary', submit_txt=_('Pay Now'))
    #         values['acquirers'] = []
    #         for acquirer in acquirers:
    #             print("\n\nacquirer---------",acquirer,">>>>>>>>>>>>>>>>",acquirers.ids)
    #             acquirer.button = acquirer.with_context(render_ctx).sudo().render(
    #                 ord.reservation_no,
    #                 ord.total_cost1,
    #                 ord.pricelist_id.currency_id.id,
    #                 partner_id = ord.partner_id.id,
    #                 values={
    #                     'return_url': '/shop/payment/validate1',
    #                     'order': order,
    #                     'order_browse':order_browse
    #                 })
    # #             acquirer.button = acquirer_button
    #             values['acquirers'].append(acquirer)
    # #         print "*******===",values['tokens']
    #         return request.render("hotel_online.payment123", values)

    @http.route(['/shop/payment'], type='http', auth="public", website=True)
    def payment(self, **post):
        """ Payment step. This page proposes several payment means based on available
        payment.acquirer. State at this point :

         - a draft sales order with lines; otherwise, clean context / session and
           back to the shop
         - no transaction in context / session, or only a draft one, if the customer
           did go to a payment.acquirer website but closed the tab without
           paying / canceling
        """
        order = request.website.get_reservation()
        print("@@@@@@@@@@@@@@@222order::::::::::::::::::::::::::::::::::::::", order)
        order_browse = request.env['hotel.reservation'].sudo().browse(order)
        redirection = self.checkout_redirection(order_browse)
        if redirection:
            return redirection

        render_values = self._get_shop_payment_values(order_browse, **post)

        if render_values['errors']:
            render_values.pop('acquirers', '')
            render_values.pop('tokens', '')

        print("\n\n\n\n renderrrrrrrrr_valuesss===", render_values)

        return request.render("hotel_online.payment123", render_values)

    # added by krishna, copied from base
    def _get_shop_payment_values(self, order, **kwargs):
        shipping_partner_id = False
        if order:
            shipping_partner_id = order.partner_id.id or order.partner_invoice_id.id

        values = dict(
            website_sale_order=order,
            errors=[],
            partner=order.partner_id.id,
            order=order,
            payment_action_id=request.env.ref('payment.action_payment_acquirer').id,
            return_url='/shop/payment/validate',
            bootstrap_formatting=True
        )

        domain = expression.AND([
            ['&', ('state', 'in', ['enabled', 'test']), ('company_id', '=', order.company_id.id)],
            ['|', ('website_id', '=', False), ('website_id', '=', request.website.id)],
            ['|', ('country_ids', '=', False), ('country_ids', 'in', [order.partner_id.country_id.id])]
        ])
        acquirers = request.env['payment.acquirer'].search(domain)

        values['access_token'] = order.access_token
        values['acquirers'] = [acq for acq in acquirers if (acq.payment_flow == 'form' and acq.view_template_id) or
                               (acq.payment_flow == 's2s' and acq.registration_view_template_id)]
        values['tokens'] = request.env['payment.token'].search(
            [('partner_id', '=', order.partner_id.id),
             ('acquirer_id', 'in', acquirers.ids)])

        return values

    #     def _get_shop_payment_values_old(self, order, **kwargs):
    #         print("ORRRRRRRRRRRRRRRRRRRRRR  ",order)
    #         print ("KWARGSSSSS   ",kwargs)
    #         if order:
    #             order = request.env['hotel.reservation'].sudo().browse(order)
    #
    #         values = dict(
    # #             order_browse=order_browse,
    #             website_sale_order=order,
    #             errors=[],
    #             partner=order.partner_id.id,
    #             order=order,
    #             payment_action_id=request.env.ref('payment.action_payment_acquirer').id,
    #             return_url= '/shop/payment/validate1',
    #             bootstrap_formatting= True
    #         )
    #         print("Values of Shop Payment Values  ",values)
    # #         ord = request.env['hotel.reservation'].sudo().browse(order)
    #
    #         acquirers = request.env['payment.acquirer'].sudo().search([('website_published', '=', True),('company_id', '=', order.company_id.id)])
    # #         acquirers = request.env['payment.acquirer'].search(
    # #             [('website_published', '=', True), ('company_id', '=', order.company_id.id)]
    # #         )
    #         print("ACUIOIJOJOJ  IIIIIIIIII ",acquirers)
    # #         values['access_token'] = order.access_token
    #         values['form_acquirers'] = [acq for acq in acquirers if acq.payment_flow == 'form' and acq.view_template_id]
    #         values['s2s_acquirers'] = [acq for acq in acquirers if acq.payment_flow == 's2s' and acq.registration_view_template_id]
    # #         values['tokens'] = request.env['payment.token'].search(
    # #             [('partner_id', '=', order.partner_id.id),
    # #             ('acquirer_id', 'in', [acq.id for acq in values['s2s_acquirers']])])
    #
    #         for acq in values['form_acquirers']:
    #                     acq.form = acq.render('/', order.total_cost1,order.pricelist_id.currency_id.id,
    #                         values={
    #                             'return_url':'/shop/payment/validate1',
    #                             'type': 'form',
    #                             'alias_usage': _('If we store your payment information on our server, subscription payments will be made automatically.'),
    #                             'partner_id': order.partner_id.id,
    #                         })
    #         print("values ================== ",values)
    #         return values

    @http.route('/shop/payment/validate', type='http', auth="public", website=True)
    def payment_validate(self, transaction_id=None, sale_order_id=None, **post):
        """ Method that should be called by the server when receiving an update
        for a transaction. State at this point :

         - UDPATE ME
        """
        print("\n\n\n\n in payment validate,transaction_id,sale_order_id===", transaction_id, sale_order_id)
        if transaction_id is None:
            print("aaaaaaaaa")
            tx = request.website.sale_get_transaction()
            print("txxxxxxxxxxx===", tx)
        else:
            print("elseeeeeeeeeee1111")
            tx = request.env['payment.transaction'].browse(transaction_id)
            print("elseeeeeeeee txxxxxx==", tx)
        if sale_order_id is None:
            print("bbbbbbbbbbbbbb")
            order = request.website.get_reservation()  # sale_get_order()
            order = request.env['hotel.reservation'].sudo().browse(order)
            print("orderrrrrrrrrrrrrr=====", order)
        else:
            print("\n\n\n elsseeeeeeeeeeeee")
            order = request.env['sale.order'].sudo().browse(sale_order_id)
            print("else ordeerrrrrrrrrrr=====", order)
            assert order.id == request.session.get('sale_last_order_id')

        if not order or (order.total_cost1 and not tx):
            print("\n\n\n\ cccccccccccc1234")
            return request.redirect('/shop')

        if (not order.total_cost1 and not tx) or tx.state in ['pending', 'done', 'authorized']:
            print("\n\n\n ddddddddd")
            if (not order.total_cost1 and not tx):
                print("ddddddddd22222222222", order)
                # Orders are confirmed by payment transactions, but there is none for free orders,
                # (e.g. free events), so confirm immediately
                # order.with_context(send_email=True).action_confirm()

        elif tx and tx.state == 'cancel':
            print("\n\n\n\n eeeeeeeeeeee")
            # cancel the quotation
            order.action_cancel()

        # clean context and session, then redirect to the confirmation page
        request.website.sale_reset()
        print("\n\n\n fffffffffffffff")
        if tx and tx.state == 'draft':
            print("\n\n\n gggggggggg")
            return request.redirect('/shop')
        print("\n\n\n\n hhhhhhhhhhhhh")
        return request.redirect('/shop/confirmation1')

    # old method
    #     @http.route('/shop/payment/validate1', type='http', auth="public", website=True)
    #     def payment_validate(self, transaction_id=None, reservation_order_id=None, **post):
    #         print("======payment_validate1========")
    #         """ Method that should be called by the server when receiving an update
    #         for a transaction. State at this point :
    #            - UDPATE ME
    #         """
    #         print("payment validation1111------- ",transaction_id,reservation_order_id)
    #         email_act = None
    #         sale_order_obj = request.env['hotel.reservation']
    #         if transaction_id is None:
    #             tx = request.website.sale_get_transaction()
    #         else:
    #             tx = request.env['payment.transaction'].sudo().browse(transaction_id)
    #         if reservation_order_id is None:
    #             order1 = request.website.get_reservation()
    #             if order1:
    #                 order = request.env['hotel.reservation'].sudo().browse(order1)
    #
    #         else:
    #             order = request.registry['hotel.reservation'].sudo().browse(reservation_order_id)
    #             print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&",order.total_cost1)
    #             assert order.id == request.session.get('sale_last_order_id')
    #         if not order or (order.total_cost1 and not tx):
    #             return request.redirect('/shop')
    #         # clean context and session, then redirect to the confirmation page
    #         request.website.sale_reset()
    #         return request.redirect('/shop/confirmation')

    @http.route(['/shop/confirmation1'], type='http', auth="public", website=True)
    def payment_confirmation(self, **post):
        print("======payment_confirmation========")
        """ End of checkout process controller. Confirmation is basically seing
         the status of a sale.order. State at this point :
          - should not have any context / session info: clean them
          - take a sale.order id, because we request a sale.order and are not
            session dependant anymore
         """
        sale_order_id = request.session.get('reservation_order_id')
        if sale_order_id:
            order = request.env['hotel.reservation'].sudo().browse(sale_order_id)
            return request.render("hotel_online.confirmation1", {'order': order})
        else:
            return request.redirect('/shop')

    @http.route(['/shop/payment/transaction/',
                 '/shop/payment/transaction/<int:so_id>',
                 '/shop/payment/transaction/<int:so_id>/<string:access_token>'], type='json', auth="public",
                website=True)
    def payment_transaction(self, acquirer_id, save_token=False, so_id=None, access_token=None, token=None, **kwargs):
        """ Json method that creates a payment.transaction, used to create a
        transaction when the user clicks on 'pay now' button. After having
        created the transaction, the event continues and the user is redirected
        to the acquirer website.

        :param int acquirer_id: id of a payment.acquirer record. If not set the
                                user is redirected to the checkout page
        """
        print(111111111111111, access_token, so_id)
        tx_type = 'form'
        if save_token:
            tx_type = 'form_save'

        # In case the route is called directly from the JS (as done in Stripe payment method)
        if access_token:
            order = request.env['hotel.reservation'].sudo().search([('access_token', '=', access_token)])
            request.session['sale_order_id'] = order.id
        elif so_id:
            order = request.env['hotel.reservation'].search([('id', '=', so_id)])
            request.session['sale_order_id'] = order.id
        else:
            order = request.website.sale_get_order()
            request.session['sale_order_id'] = order.id

        print(3333333333333333333333333, order, order.reservation_line, acquirer_id)
        if not order or not order.reservation_line or acquirer_id is None:
            return False

        assert order.partner_id.id != request.website.partner_id.id

        print(44444444444444444444)
        # find or create transaction
        tx = request.website.sale_get_transaction() or request.env['payment.transaction'].sudo()
        acquirer = request.env['payment.acquirer'].browse(int(acquirer_id))
        print(555555555555555555555555555555555)
        payment_token = request.env['payment.token'].sudo().browse(int(token)) if token else None
        tx = tx._check_or_create_sale_tx(order, acquirer, payment_token=payment_token, tx_type=tx_type)
        print(666666666666666666666666)
        request.session['sale_transaction_id'] = tx.id

        return tx.render_sale_button(order, '/shop/payment/validate')

    @http.route('/shop/payment/get_status123/<int:sale_order_id>', type='json', auth="public", website=True)
    def payment_get_status(self, sale_order_id, **post):
        print("********payment_get_status**********")
        order = request.env['hotel.reservation'].sudo().browse(sale_order_id)
        assert order.id == request.session.get('reservation_order_id')
        if not order:
            return {
                'state': 'error',
                'message': '<p>%s</p>' % _('There seems to be an error with your request.'),
            }
        tx_ids = request.env['payment.transaction'].sudo().search([
            '|', ('sale_order_id', '=', order.id), ('reference', '=', order.name)
        ])
        if not tx_ids:
            if order.total_cost1:
                return {
                    'state': 'error',
                    'message': '<p>%s</p>' % _('There seems to be an error with your request.'),
                }
            else:
                state = 'done'
                message = ""
                validation = None
        else:
            print("TRansactionsssss   ============    ", tx_ids)
            #             tx = request.env['payment.transaction'].sudo().browse(tx_ids)
            tx = tx_ids
            state = tx.state
            if state == 'done':
                message = '<p>%s</p>' % _('Your payment has been received.')
            elif state == 'cancel':
                message = '<p>%s</p>' % _('The payment seems to have been canceled.')
            elif state == 'pending' and tx.acquirer_id.validation == 'manual':
                message = '<p>%s</p>' % _('Your transaction is waiting confirmation.')
                if tx.acquirer_id.post_msg:
                    message += tx.acquirer_id.post_msg
            else:
                message = '<p>%s</p>' % _('Your transaction is waiting confirmation.')
            print("Acquirereeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee   ", tx.acquirer_id)
        #             validation = tx.acquirer_id.validation
        return {
            'state': state,
            'message': message,
            'validation': None
        }

    def checkout_redirection(self, order):
        print(" ^^^^^^^^ chechout redirect ^^^^^^ ", order)
        if type(order) == int:
            order = request.env['hotel.reservation'].sudo().browse(order)
            print("Browseeeee Order  ", order.state)
        if not order or order.state != 'draft':
            request.session['sale_order_id'] = None
            request.session['sale_transaction_id'] = None
            return request.redirect('/shop')

        # if transaction pending / done: redirect to confirmation
        tx = request.env.context.get('website_sale_transaction')
        print("tttttttxxxxx", tx)
        if tx and tx.state != 'draft':
            return request.redirect('/shop/payment/confirmation/%s' % order)


check()
reserv_list = []


class website(models.Model):
    _inherit = 'website'
    _columns = {}

    def get_image(self, a):
        print("****** get_image *******")
        if 'image' in list(a.keys()):
            return True
        else:
            print('no img')
            return False

    def get_type(self, record1):
        print("*****get tyoe*****", self, record1)
        categ_type = record1['type']
        #         print "\n\ncateg_type",categ_type
        categ_ids = self.env['product.category'].sudo().search([('name', '=', categ_type[0])])
        #         print "categ_idsssssss",categ_ids
        categ_records = categ_ids[0]
        #         print "categ_records",categ_records
        #         if categ_records.type == 'view':
        #             return False
        return True

    def check_next_image(self, main_record, sub_record):
        if len(main_record['image']) > sub_record:
            return 1
        else:
            return 0

    def image_url_new(self, record1, field, size=None):
        #         print "====----image_url_new----===",self,record1,field
        """Returns a local url that points to the image field of a given browse record."""
        lst = []
        record = self.env['hotel.room.images'].sudo().browse(record1)
        cnt = 0
        for r in record:
            cnt = cnt + 1
            model = r._name
            sudo_record = r.sudo()
            id = '%s_%s' % (r.id, hashlib.sha1(
                (str(sudo_record.write_date) or str(sudo_record.create_date) or '').encode('utf-8')).hexdigest()[0:7])

            if cnt == 1:
                size = '' if size is None else '/%s' % size
            else:
                size = '' if size is None else '%s' % size
            lst.append('/website/image/%s/%s/%s%s' % (model, id, field, size))
        return lst

    def get_reservation(self):
        print("------------get_reservation-------------")
        reservation_order_id = request.session.get('reservation_order_id')
        if not reservation_order_id:
            part_id1 = request.env['res.partner'].sudo().search([('name', '=', 'Public user'), ('active', '=', False)])
            print("part_id1-----", part_id1)
            reservation = request.env['hotel.reservation'].sudo().search([('partner_id', '=', part_id1[0])])
            print("reservation", reservation)
            reserv_list = reservation
            if reservation:
                reservation1 = request.env['hotel.reservation'].sudo().browse(reservation[0])
                print("reservation1", reservation1)
                request.session['reservation_order_id'] = reservation1.id
                return reservation1.id
        return reservation_order_id

    def sale_get_transaction(self):
        print("------------sale_get_transaction-------------")
        transaction_obj = self.env['payment.transaction']
        tx_id = request.session.get('sale_transaction_id')
        print("------------tx_id-------------", tx_id)
        if tx_id:
            tx_ids = transaction_obj.sudo().search([('id', '=', tx_id), ('state', 'not in', ['cancel'])])
            print("transactionnnnnnnnnnnn of sale_get_transaction", tx_ids)

            if tx_ids:
                return tx_ids
            #                 return transaction_obj.browse(tx_ids)
            else:
                request.session['sale_transaction_id'] = False
        return False

    #

    def sale_reset(self):
        request.session.update({
            'sale_order_id': False,
            'sale_transaction_id': False,
            'sale_order_code_pricelist_id': False,
        })


website()


class ResCountry(models.Model):
    _inherit = 'res.country'

    def get_website_sale_countries(self, mode='billing'):
        return self.sudo().search([])

    def get_website_sale_states(self, mode='billing'):
        return self.sudo().state_ids
