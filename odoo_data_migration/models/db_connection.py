from odoo import models, fields, api
import logging
from odoo.exceptions import ValidationError
import pyodbc

logger = logging.getLogger(__name__)


class DbConnection(models.Model):
    _name = 'dbconnection'
    _rec_name = 'name'
    _description = 'Database connectivity setup'

    name = fields.Char(string="Connection Name", required=True, size=100)
    connection_status = fields.Char(string="Connection Status", required=False, )
    connection_driver = fields.Char(string="ODBC Driver", required=False, default='{ODBC Driver 17 for SQL Server}')
    connection_server = fields.Char(string="Server", required=False, default='localhost')
    connection_db = fields.Char(string="Database", required=False, default='tempdb')
    connection_port = fields.Char(string="Port", required=False, default='1433')
    connection_user = fields.Char(string="User Name", required=False, default='sa')
    connection_password = fields.Char(string="Password", required=False, default='sa')
    loading_process_ids = fields.One2many(comodel_name="loading_process", inverse_name="dbconnection", string="Logs")
    # ------------------------------vendor----------------
    vendor_id_map = fields.Char(string="Vendor ID", required=False, help="Vendor ID map filed to integer field.")
    vendor_name_map = fields.Char(string="Vendor Name", required=False, help="Vendor Name map filed to string field.")
    vendor_description_map = fields.Char(string="Vendor Description", required=False,
                                         help="Vendor Description map filed to string field.")
    vendor_email_map = fields.Char(string="Vendor Email", required=False,
                                   help="Vendor Email map filed to string field.")
    vendor_phone_map = fields.Char(string="Vendor Phone", required=False, help="Vendor phone filed to string field.")
    vendor_contact_map = fields.Char(string="Vendor contact", required=False,
                                     help="Vendor contact name map filed to string field.")
    vendor_table_name = fields.Char(string="Vendor Table", required=False,
                                    help="Vendor table name \ View name.")
    vendor_table_where = fields.Text(string="Vendor Table Where", required=False,
                                     help="Vendor table where conditions (Do not add WHERE word).")
    # ------------------------------customer----------------
    customer_id_map = fields.Char(string="Customer ID", required=False, help="Customer ID map filed to integer field.")
    customer_name_map = fields.Char(string="Customer Name", required=False,
                                    help="Customer Name map filed to string field.")
    customer_email_map = fields.Char(string="Customer Email", required=False,
                                     help="Customer Email map filed to string field.")
    customer_phone_map = fields.Char(string="Customer Phone", required=False,
                                     help="Customer phone filed to string field.")
    customer_table_name = fields.Char(string="Customer Table", required=False,
                                      help="Customer table name \ View name.")
    customer_table_where = fields.Text(string="Customer Table Where", required=False,
                                       help="Customer table where conditions (Do not add WHERE word).")
    # ------------------------------Product category----------------
    product_category_id_map = fields.Char(string="Product Category ID", required=False,
                                          help="Product Category ID map filed to integer field.")
    product_category_name_map = fields.Char(string="Product Category Name", required=False,
                                            help="Product Category Name map filed to string field.")
    product_category_parent_id_map = fields.Char(string="Product Parent ID", required=False,
                                                 help="Product Parent ID map filed to integer field.")
    product_category_table_name = fields.Char(string="Product Category Table", required=False,
                                              help="Product Category table name \ View name.")
    product_category_table_where = fields.Text(string="Product Category Table Where", required=False,
                                               help="Product Category table where conditions (Do not add WHERE word).")
    # ------------------------------Product----------------
    product_id_map = fields.Char(string="Product ID", required=False,
                                 help="Product ID map filed to integer field.")
    product_name_map = fields.Char(string="Product Name", required=False,
                                   help="Product Name map filed to string field.")
    product_description_map = fields.Char(string="Product Description", required=False,
                                          help="Product description map filed to string field.")
    product_price_map = fields.Char(string="Product Price", required=False,
                                    help="Product price map filed to decimal field.")
    product_cost_map = fields.Char(string="Product Price", required=False,
                                   help="Product cost map filed to decimal field.")
    category_id_map = fields.Char(string="Category ID", required=False,
                                  help="Category ID map filed to integer field.")
    product_table_name = fields.Char(string="Product Table", required=False,
                                     help="Product Category table name \ View name.")
    product_table_where = fields.Text(string="Product Table Where", required=False,
                                      help="Product Category table where conditions (Do not add WHERE word).")
    # ------------------------------Invoices----------------
    order_id_map = fields.Char(string="Order ID", required=False,
                               help="Order ID map filed to integer field.")
    order_date_map = fields.Char(string="Order Date", required=False,
                                 help="Order Date map filed to date field.")
    order_customer_id_map = fields.Char(string="Order Customer", required=False,
                                        help="Order Customer ID map filed to integer field.")
    order_product_id_map = fields.Char(string="Order Product", required=False,
                                       help="Order product id map filed to integer field.")
    order_product_price_map = fields.Char(string="Product Price", required=False,
                                          help="Product Price map filed to decimal field.")
    order_product_quantity_map = fields.Char(string="Product Quantity", required=False,
                                             help="Product Quantity map filed to integer field.")
    order_table_name = fields.Char(string="Order Table", required=False,
                                   help="Order table name \ View name.")
    order_table_where = fields.Text(string="Order Table Where", required=False,
                                    help="Order table where conditions (Do not add WHERE word).")

    # =================================Main functions=====================
    def _open_connection(self):
        try:
            driver_str = 'DRIVER=' + self.connection_driver + ';' if self.connection_driver else ''
            SERVER_str = 'SERVER=' + self.connection_server + ';' if self.connection_server else ''
            DATABASE_str = 'DATABASE=' + self.connection_db + ';' if self.connection_db else ''
            UID_str = 'UID=' + self.connection_user + ';' if self.connection_user else ''
            PWD_str = 'PWD=' + self.connection_password + ';' if self.connection_password else ''
            port_str = 'port=' + self.connection_port + ';' if self.connection_port else ''

            conn = pyodbc.connect(driver_str + SERVER_str + DATABASE_str + UID_str + PWD_str + port_str)
            return conn
        except Exception as e:
            logger.exception("Open Connection.")
            raise ValidationError(e)

    def test_connection(self):
        try:
            driver_str = 'DRIVER=' + self.connection_driver + ';' if self.connection_driver else ''
            SERVER_str = 'SERVER=' + self.connection_server + ';' if self.connection_server else ''
            DATABASE_str = 'DATABASE=' + self.connection_db + ';' if self.connection_db else ''
            UID_str = 'UID=' + self.connection_user + ';' if self.connection_user else ''
            PWD_str = 'PWD=' + self.connection_password + ';' if self.connection_password else ''
            port_str = 'port=' + self.connection_port + ';' if self.connection_port else ''

            conn = pyodbc.connect(driver_str + SERVER_str + DATABASE_str + UID_str + PWD_str + port_str)
            cursor = conn.cursor()
            if cursor:
                self.log_actions('database_connection', 'Connection to DB established.')
                self.connection_status = "Connected"
                conn.close()
            else:
                self.log_actions('database_connection', 'Connection to DB failed.')
                self.connection_status = "Not Connected"
                conn.close()
        except Exception as e:
            logger.exception("Test Connection")
            raise ValidationError(e)

    def log_actions(self, action_type, msg):
        try:
            # sql = ("""INSERT INTO loading_process (dbconnection, tran_date_time, action_type, description)
            # values (%i, '%s', '%s', '%s')""" % (self.id, fields.datetime.now(), action_type, msg))
            # self.env.cr.execute(sql)

            self.env['loading_process'].create(
                {'dbconnection': self.id, 'tran_date_time': fields.datetime.now(), 'action_type': action_type,
                 'description': msg})
        except Exception as e:
            logger.exception("log_actions")
            raise ValidationError(e)

    # =================================Vendors functions=====================
    def _load_vendor_cron(self, connection_name):
        self.env['dbconnection'].search([('name', '=', connection_name)], limit=1).load_vendor_process()

    def load_vendor_process(self):
        try:
            self.log_actions('vendor_upload', 'Load vendors Started.')
            conn = self._open_connection()
            if conn:
                query_str = "SELECT "
                query_str += self.vendor_id_map + ', ' if self.vendor_id_map else ''
                query_str += self.vendor_name_map + ', ' if self.vendor_name_map else ''
                query_str += self.vendor_description_map + ', ' if self.vendor_description_map else ''
                query_str += self.vendor_email_map + ', ' if self.vendor_email_map else ''
                query_str += self.vendor_phone_map + ', ' if self.vendor_phone_map else ''
                query_str += self.vendor_contact_map + ' ' if self.vendor_contact_map else ''
                query_str += 'FROM ' + self.vendor_table_name + ' ' if self.vendor_table_name else ''
                query_str += 'WHERE ' + self.vendor_table_where.replace('where', ''). \
                    replace('Where', '').replace('WHERE', '') + ' ' if self.vendor_table_where else ''

                cursor = conn.cursor()
                if cursor:
                    self.log_actions('database_connection', 'Connection to DB established.')
                else:
                    self.log_actions('database_connection', 'Connection to DB failed.')

                cursor.execute(query_str)
                rows = cursor.fetchall()
                conn.close()
                self.log_actions('database_connection', 'Connection to DB closed.')

                if len(rows) > 0:
                    self.log_actions('vendor_upload', 'Vendors records = %i' % len(rows))
                    for row in rows:
                        self.create_vendor(row[0], row[1], row[2], row[3], row[4], row[5])

                self.log_actions('vendor_upload', 'Load vendors completed.')
        except Exception as e:
            self.log_actions('error', e)
            logger.exception("_cron_vendor_process")
            raise ValidationError(e)

    def create_vendor(self, vendor_id, name, description, email, phone, contact):
        try:
            vendor_obj = self.env['res.partner'].search([('vend_old_id', '=', vendor_id)], limit=1)
            if not vendor_obj:
                res = {
                    'vend_old_id': vendor_id,
                    'name': name,
                    'comment': description,
                    'email': email,
                    'phone': phone,
                    'is_company': 'true',
                    'supplier_rank': 1,
                }

                vendor_obj = self.env['res.partner'].create(res)
                # Add linked contact
                if contact and vendor_obj:
                    res_child = {'type': 'contact',
                                 'name': contact,
                                 'supplier_rank': 1,
                                 'parent_id': vendor_obj.id,
                                 'vend_old_id': vendor_obj.id}
                    self.env['res.partner'].create(res_child)
            return vendor_obj.id
        except Exception as e:
            logger.exception("upload_vendor_record")
            raise ValidationError(e)

    # =================================Customers functions=====================
    def _load_customer_cron(self, connection_name):
        self.env['dbconnection'].search([('name', '=', connection_name)], limit=1).load_customer_process()

    def load_customer_process(self):
        try:
            self.log_actions('customer_upload', 'Load customers Started.')
            conn = self._open_connection()
            if conn:
                query_str = "SELECT "
                query_str += self.customer_id_map + ', ' if self.customer_id_map else ''
                query_str += self.customer_name_map + ', ' if self.customer_name_map else ''
                query_str += self.customer_email_map + ', ' if self.customer_email_map else ''
                query_str += self.customer_phone_map + ' ' if self.customer_phone_map else ''
                query_str += 'FROM ' + self.customer_table_name + ' ' if self.customer_table_name else ''
                query_str += 'WHERE ' + self.customer_table_where.replace('where', ''). \
                    replace('Where', '').replace('WHERE', '') + ' ' if self.customer_table_where else ''
                print(query_str)
                cursor = conn.cursor()
                if cursor:
                    self.log_actions('database_connection', 'Connection to DB established.')
                else:
                    self.log_actions('database_connection', 'Connection to DB failed.')

                cursor.execute(query_str)
                rows = cursor.fetchall()
                conn.close()
                self.log_actions('database_connection', 'Connection to DB closed.')

                if len(rows) > 0:
                    self.log_actions('customer_upload', 'Customers records = %i' % len(rows))
                    for row in rows:
                        self.create_customer(row[0], row[1], row[2], row[3])

                self.log_actions('customer_upload', 'Load customers completed.')
        except Exception as e:
            self.log_actions('error', e)
            logger.exception("_cron_vendor_process")
            raise ValidationError(e)

    def create_customer(self, user_id, name, email, mobile):
        try:
            customer_obj = self.env['res.partner'].search([('cust_old_id', '=', user_id)], limit=1)
            if not customer_obj:
                customer_obj = self.env['res.partner'].create({
                    'name': name,
                    'mobile': mobile,
                    'email': email,
                    'is_company': 'false',
                    'customer_rank': 1,
                    'cust_old_id': user_id
                })
            return customer_obj.id
        except Exception as e:
            logger.exception("create_customer")
            raise ValidationError(e)

    # =================================Product Category functions=====================
    def _load_product_categ_cron(self, connection_name):
        self.env['dbconnection'].search([('name', '=', connection_name)], limit=1).load_product_categ_process()

    def load_product_categ_process(self):
        try:
            self.log_actions('product_categ_upload', 'Load Product Category Started.')
            conn = self._open_connection()
            if conn:
                query_str = "SELECT "
                query_str += self.product_category_id_map + ', ' if self.product_category_id_map else ''
                query_str += self.product_category_name_map + ', ' if self.product_category_name_map else ''
                query_str += self.product_category_parent_id_map + ' ' if self.product_category_parent_id_map else 0
                query_str += 'FROM ' + self.product_category_table_name + ' ' if self.product_category_table_name else ''
                query_str += 'WHERE ' + self.product_category_table_where.replace('where', ''). \
                    replace('Where', '').replace('WHERE', '') + ' ' if self.product_category_table_where else ''

                print(query_str)
                cursor = conn.cursor()
                if cursor:
                    self.log_actions('database_connection', 'Connection to DB established.')
                else:
                    self.log_actions('database_connection', 'Connection to DB failed.')

                cursor.execute(query_str)
                rows = cursor.fetchall()
                conn.close()
                self.log_actions('database_connection', 'Connection to DB closed.')

                if len(rows) > 0:
                    self.log_actions('product_categ_upload', 'Product Category records = %i' % len(rows))
                    for row in rows:
                        self.create_product_categ(row[0], row[1], row[2])

                self.log_actions('product_categ_upload', 'Load Product Category completed.')
        except Exception as e:
            self.log_actions('error', e)
            logger.exception("load_product_categ_process")
            raise ValidationError(e)

    def create_product_categ(self, old_id, name, old_parent_id):
        try:
            current_product_category_obj = self.env['product.category'].search([('old_id', '=', old_id)], limit=1)

            product_cat_saleable = self.env['product.category'].search([('name', '=', 'Saleable')], limit=1)
            if not product_cat_saleable:
                raise ValidationError("Parent Category Saleable is not found.")
            else:
                product_cat_saleable_id = product_cat_saleable.id

            if not current_product_category_obj:
                res = {
                    'old_id': old_id,
                    'name': name,
                    'old_parent_id': old_parent_id,
                    'parent_id': product_cat_saleable_id
                }

                self.env['product.category'].create(res)

                product_cat_list = self.env['product.category'].search([('old_parent_id', '>', 0)])

                for product_cat in product_cat_list:
                    product_cat_obj = self.env['product.category'].search([('old_id', '=', product_cat.old_parent_id)],
                                                                          limit=1)
                    product_cat_mod = self.env['product.category'].search([('id', '=', product_cat.id)],
                                                                          limit=1)
                    product_cat_mod.write({'parent_id': product_cat_obj.id})

            return current_product_category_obj.id
        except Exception as e:
            logger.exception("get_create_product_categ")
            raise ValidationError(e)

    # =================================Product functions=====================
    def _load_product_cron(self, connection_name):
        self.env['dbconnection'].search([('name', '=', connection_name)], limit=1).load_product_process()

    def load_product_process(self):
        try:
            self.log_actions('product_upload', 'Load Product Started.')
            conn = self._open_connection()
            if conn:
                query_str = "SELECT "
                query_str += self.product_id_map + ', ' if self.product_id_map else ''
                query_str += self.product_name_map + ', ' if self.product_name_map else ''
                query_str += self.product_description_map + ', ' if self.product_description_map else ''
                query_str += self.product_price_map + ', ' if self.product_price_map else 0
                query_str += self.product_cost_map + ', ' if self.product_cost_map else 0
                query_str += self.category_id_map + ' ' if self.category_id_map else 0
                query_str += 'FROM ' + self.product_table_name + ' ' if self.product_table_name else ''
                query_str += 'WHERE ' + self.product_table_where.replace('where', ''). \
                    replace('Where', '').replace('WHERE', '') + ' ' if self.product_table_where else ''

                print(query_str)
                cursor = conn.cursor()
                if cursor:
                    self.log_actions('database_connection', 'Connection to DB established.')
                else:
                    self.log_actions('database_connection', 'Connection to DB failed.')

                cursor.execute(query_str)
                rows = cursor.fetchall()
                conn.close()
                self.log_actions('database_connection', 'Connection to DB closed.')

                if len(rows) > 0:
                    self.log_actions('product_upload', 'Product records = %i' % len(rows))
                    for row in rows:
                        self.create_product(row[0], row[1], row[2], row[3], row[4], row[5])

                self.log_actions('product_upload', 'Load Product completed.')
        except Exception as e:
            self.log_actions('error', e)
            logger.exception("load_product_process")
            raise ValidationError(e)

    def create_product(self, product_id, product_name, product_description, product_price, product_cost, category_id):
        try:
            product_obj = self.env['product.template'].search([('old_id', '=', product_id)], limit=1)
            if not product_obj:
                product_category_obj = self.env['product.category'].search([('old_id', '=', category_id)], limit=1)
                res = {
                    'old_id': product_id,
                    'name': product_name,
                    'categ_id': product_category_obj.id if product_category_obj else 0,
                    'description': product_description,
                    'list_price': product_price,
                    'standard_price': product_cost,
                    'sale_ok': 'true',
                    'purchase_ok': 'true',
                }

                product_obj = self.env['product.template'].create(res)

            return product_obj.id
        except Exception as e:
            logger.exception("upload_product_record")
            raise ValidationError(e)

    # =================================Product functions=====================
    def _load_invoices_cron(self, connection_name):
        self.env['dbconnection'].search([('name', '=', connection_name)], limit=1).load_invoices_process()

    def load_invoices_process(self):
        try:
            self.log_actions('product_invoices', 'Load Invoices Started.')
            conn = self._open_connection()
            if conn:
                query_str = "SELECT "
                query_str += self.order_id_map + ', ' if self.order_id_map else 0
                query_str += self.order_date_map + ', ' if self.order_date_map else ''
                query_str += self.order_customer_id_map + ', ' if self.order_customer_id_map else 0
                query_str += self.order_product_id_map + ', ' if self.order_product_id_map else 0
                query_str += self.order_product_price_map + ', ' if self.order_product_price_map else 0
                query_str += self.order_product_quantity_map + ' ' if self.order_product_quantity_map else 0
                query_str += 'FROM ' + self.order_table_name + ' ' if self.order_table_name else ''
                query_str += 'WHERE ' + self.order_table_where.replace('where', ''). \
                    replace('Where', '').replace('WHERE', '') + ' ' if self.order_table_where else ''

                print(query_str)
                cursor = conn.cursor()
                if cursor:
                    self.log_actions('database_connection', 'Connection to DB established.')
                else:
                    self.log_actions('database_connection', 'Connection to DB failed.')

                cursor.execute(query_str)
                rows = cursor.fetchall()
                conn.close()
                self.log_actions('database_connection', 'Connection to DB closed.')

                order_id = 0
                customer_id = 0
                order_details = []
                if len(rows) > 0:
                    self.log_actions('product_invoices', 'Invoices records = %i' % len(rows))
                    for row in rows:
                        # self.create_invoice(row[0], row[1], row[2], row[3], row[4], row[5])
                        if (row[0] != order_id) and (order_id == 0):
                            # customer_id = get_create_customer(self, row.user_id, row.cust_name, row.mobile, row.email)
                            customer_id = self.env['res.partner'].search([('cust_old_id', '=', row[2])], limit=1)
                            order_id = row[0]

                        if (row[0] != order_id) and (order_id != 0):
                            # customer_id = get_create_customer(self, row.user_id, row.cust_name, row.mobile, row.email)
                            customer_id = self.env['res.partner'].search([('cust_old_id', '=', row[2])], limit=1)
                            order_id = row[0]
                            self.create_invoice(order_details)
                            order_details = []

                        order_details.append({'customer_id': customer_id, 'order_date': row[1],
                                              'order_id': row[0], 'product_id': row[3],
                                              'quantity': row[5], 'price_per': row[4]})


                self.log_actions('product_invoices', 'Load Invoices completed.')
        except Exception as e:
            self.log_actions('error', e)
            logger.exception("load_product_process")
            raise ValidationError(e)

    def create_invoice(self, order_details):
        try:
            to_continue = True
            invoice_line_ids = []
            for order_data in order_details:
                product_obj = self.env['product.template'].search([('old_id', '=', order_data['product_id'])], limit=1)
                product_id = product_obj.id
                if not product_obj:
                    to_continue = False
                    break
                else:
                    invoice_line_ids.append({'product_id': product_id,
                                             'quantity': order_data['quantity'],
                                             'price_unit': order_data['price_per']})
            if to_continue == False:
                return None
            else:

                # invoice_line_ids.append({'product_id': delivery_service_product,
                #                          'quantity': 1,
                #                          'price_unit': delivery_charges})
                res = {
                    'old_id': str(order_details[0]['order_id']),
                    'type': 'out_invoice',
                    'ref': str(order_details[0]['order_id']),
                    'partner_id': order_details[0]['customer_id'],
                    'invoice_date': order_details[0]['order_date'],
                    'invoice_line_ids': [(0, 0, line) for line in invoice_line_ids]
                }
                move = self.env['account.move'].create(res)
                move.action_post()
                self.post_payment(move)
                return move
        except Exception as e:
            logger.exception("create_invoice")
            raise ValidationError(e)

    def post_payment(self, move):
        try:
            cash_journal_obj = self.env['account.journal'].search([('name', '=', 'Cash')], limit=1)

            res = {
                'payment_type': 'inbound',
                'partner_type': 'customer',
                'amount': move.amount_total,
                'payment_reference': move.ref,
                'currency_id': move.currency_id.id,
                'journal_id': cash_journal_obj.id,
                'payment_method_id': self.env.ref('account.account_payment_method_manual_in').id,
                'partner_id': move.partner_id.id,
            }
            payment_obj = self.env['account.payment'].create(res)
            payment_obj.post()

            credit_line_a = payment_obj.move_line_ids.filtered(
                lambda l: l.credit)
            move.js_assign_outstanding_line(credit_line_a.id)

            return payment_obj
        except Exception as e:
            logger.exception("post_payment Method")
            raise ValidationError(e)

    def create_ir_cron(self, job_name):
        try:
            cron_name = "Data Integration: %s - %s" %(self.name, job_name)
            function_name = ''
            if job_name == 'Customers':
                function_name = "model._load_customer_cron('%s')" % self.name
            if job_name == 'Vendors':
                function_name = "model._load_vendor_cron('%s')" % self.name
            if job_name == 'Products Category':
                function_name = "model._load_product_categ_cron('%s')" % self.name
            if job_name == 'Products':
                function_name = "model._load_product_cron('%s')" % self.name
            if job_name == 'Invoices':
                function_name = "model._load_invoices_cron('%s')" % self.name

            cron_obj = self.env['ir.cron'].search([('name', '=', cron_name)], limit=1)
            if not cron_obj:
                self.env['ir.cron'].create(
                    {'name': cron_name,
                     'model_id': self.env.ref('odoo_data_migration.model_dbconnection').id,
                     'state': 'code',
                     'code': function_name,
                     'interval_number': 1,
                     'interval_type': 'days',
                     'numbercall': -1,
                     'doall': False,
                     'active': False
                     })

        except Exception as e:
            logger.exception("create_ir_cron")
            raise ValidationError(e)

    # =================================Model Methods=====================
    @api.model
    def create(self, vals):
        try:
            obj = super(DbConnection, self).create(vals)
            # ir.cron
            self.create_ir_cron('Customers')
            self.create_ir_cron('Vendors')
            self.create_ir_cron('Products Category')
            self.create_ir_cron('Products')
            self.create_ir_cron('Invoices')



        except Exception as e:
            logger.exception("create Method")
            raise ValidationError(e)
        return obj

    def write(self, vals):
        try:
            obj = super(DbConnection, self).write(vals)
            # ir.cron
            self.create_ir_cron('Customers')
            self.create_ir_cron('Vendors')
            self.create_ir_cron('Products Category')
            self.create_ir_cron('Products')
            self.create_ir_cron('Invoices')
        except Exception as e:
            logger.exception("Write Method")
            raise ValidationError(e)
        return obj

    def unlink(self):
        try:
            return super(DbConnection, self).unlink()
        except Exception as e:
            logger.exception("unlink Method")
            raise ValidationError(e)
