# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

import json
from odoo import http, SUPERUSER_ID
from odoo.http import request


class OdooWebsiteSearchSuggestion(http.Controller):

    @http.route(['/search/suggestion'], type='http', auth="public", website=True)
    def search_suggestion(self, **post):
    	#print "/search/suggestion calleddddddddddddddddddddddddddddddddddddddddddddddddd",post, post.get('query').split(" ")
        suggestion_list = []
        product=[]
        product_list_name={}    	


        if post:
            for suggestion in post.get('query').split(" "):
                product_list = request.env['product.template'].search(([('website_published', '=', True), ('name', "ilike", suggestion)]))
                #print "====================product_list",product_list
                read_prod = product_list.read(['name','public_categ_ids'])
    	        #print "****************************product_obj",product_list
                suggestion_list = suggestion_list + read_prod
    	        #print "2222222222222222222222222212product_obj",suggestion_list
    	        

        for line in suggestion_list:
            if len(line['public_categ_ids'])==0:
                #print "\n \n =========================line",line
                prod_str=line['name']+ "No category"
                #print "\n \n =========================id",id
                if not prod_str in product_list_name :
                    product.append({'product':line['name'],'category':'No category'})

            for pub_cat_ids in line['public_categ_ids']:
                categ_srch= request.env['product.public.category'].search(([('id','=',pub_cat_ids)]))
                categ_read = categ_srch.read(['name'])
                #print "\n \n ====================categ",categ_read
                prod_str=line['name']+categ_read[0]['name']
                #print "\n \n =========================line",prod_str                
                if not prod_str in product_list_name :
                    product.append({'product':line['name'],'category':categ_read[0]['name']})
        #print "=================product_list_name",product_list_name


        data={}
        #print "================="
        data['status']=True,
        #print "================="
        data['error']=None,
        #print "================="
        data['data']={'product':product}
        #print "================="
        return json.dumps(data)
    	
    	       
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:        
