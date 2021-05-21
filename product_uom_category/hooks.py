# Copyright 2019 CorTex IT Solutions
# License OPL-1


def post_init_hook(cr, registry):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})


    cr.execute('select id,uom_id from product_template')

    for id, uom_id in cr.fetchall():
        if id:
            cr.execute('SELECT category_id FROM uom_uom where id=%s' % uom_id)
            uom_category_id = cr.fetchone()
            cr.execute('UPDATE product_template SET uom_categ_id=%s WHERE id=%s',
                       (uom_category_id, id))
