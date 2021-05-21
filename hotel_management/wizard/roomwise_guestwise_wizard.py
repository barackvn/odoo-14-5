from odoo import models, fields, api


class room_guestwise_wizard(models.TransientModel):
    _name = 'room.guestwise.wizard'
    _description = 'room guestwise wizard'

    _description = 'Room wise Guest wise Wizard'
    date_start = fields.Date('From Date', required=True)
    date_end = fields.Date('To Date', required=True)

    # @api.multi
    def print_report(self):
        print("print_report=================")
        datas = {}
        # return self.env.ref('hotel_management.roomwise_guestwise_qweb').report_action(self, data=datas, config=False)

    def your_test_method(self):
        print("hiiiiiiiiii")
