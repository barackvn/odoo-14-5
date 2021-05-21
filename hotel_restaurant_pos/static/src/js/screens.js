odoo.define('hotel_restaurant_pos.screens', function (require) {
	"use strict";
	console.log("Screens  =======   ");
	var screens = require('point_of_sale.screens');
	var PosBaseWidget = require('point_of_sale.BaseWidget');
	var gui = require('point_of_sale.gui');

	var models = require('point_of_sale.models');
	var core = require('web.core'); 
//	var Model = require('web.DataModel');  not available in odoo 11
	var rpc = require('web.rpc'); 
	var QWeb = core.qweb;
	var _t = core._t;
//	
	screens.PaymentScreenWidget.include({
		
		renderElement: function(){
            this._super();
            var self = this;
            
            this.$('.js_set_room').click(function(){
            	console.log('\n\n\n hi in on click of room button=======');
                self.click_set_room();
                
            });
            
       },
		
//		room_changed: function() {
//	           var room = this.pos.get_room();
//	           this.$('.js_room_name').text( room ? room.name : _t('Room') ); 
//	       },
		
		click_set_room: function(){
			console.log("Set Room Function")
	        this.gui.show_screen('roomlist');
//	        this.$('.js_room_name').text( client ? client.name : _t('Customer') );
	    },
	    
	    
//	    validate_order: function() {
//	    	console.log('\n\n\n validate_order in new screen ===');
//	    	 this._super();
//	    	 var folio_id = this.pos.get_order().get_folio_ids();
//	    	 var room_name = this.pos.get_order().get_room_name();
//	    	 console.log('\\n\n folio_id ===== room_name =======',folio_id,room_name);
//	    	 
////	        if (this.order_is_valid(force_validation)) {
////	            this.finalize_validation();
////	        }
//	    },
	    
	    finalize_validation: function() {
	    	console.log('\n\n\n new method finalize_validation === this =',this);
	        var self = this;
	        var order = this.pos.get_order();
	        console.log('\n\n\n finalize_validation order ====',order);
	        if (order.is_paid_with_cash() && this.pos.config.iface_cashdrawer) { 

	                this.pos.proxy.open_cashbox();
	        }
	        
	        order.initialize_validation_date();
	        if (order.is_to_invoice()) {
	        	console.log('\n\n\n finalize_validation == order after ==',order);
	            var invoiced = this.pos.push_and_invoice_order(order);
	            console.log('\n\n\n finalize_validation == invoiced ==',invoiced);
	            this.invoicing = true;

	            invoiced.fail(function(error){
	                self.invoicing = false;
	                if (error.message === 'Missing Customer') {
	                    self.gui.show_popup('confirm',{
	                        'title': _t('Please select the Customer'),
	                        'body': _t('You need to select the customer before you can invoice an order.'),
	                        confirm: function(){
	                            self.gui.show_screen('clientlist');
	                        },
	                    });
	                } else if (error.code < 0) {        // XmlHttpRequest Errors
	                    self.gui.show_popup('error',{
	                        'title': _t('The order could not be sent'),
	                        'body': _t('Check your internet connection and try again.'),
	                    });
	                } else if (error.code === 200) {    // OpenERP Server Errors
	                    self.gui.show_popup('error-traceback',{
	                        'title': error.data.message || _t("Server Error"),
	                        'body': error.data.debug || _t('The server encountered an error while receiving your order.'),
	                    });
	                } else {                            // ???
	                    self.gui.show_popup('error',{
	                        'title': _t("Unknown Error"),
	                        'body':  _t("The order could not be sent to the server due to an unknown error"),
	                    });
	                }
	            });

	            invoiced.done(function(){
	                self.invoicing = false;
	                if(order.room_name != '' && order.folio_ids != ''){
	                	order.finalize();
	                	self.gui.show_screen('products');
	                }else{
	                	self.gui.show_screen('receipt');
	                }
	            });
	        } else {
	            this.pos.push_order(order);
	            this.gui.show_screen('receipt');
	        }

	    },
	    
	    
	    
	});

	
	
	var RoomListScreenWidget = screens.ScreenWidget.extend({
		
		template:'RoomListScreenWidget', 
		
		init: function(parent, options){
	        this._super(parent, options);
	    },
		
		auto_back: true,
		
		show: function(){
			var self = this;
			this._super();
			this.renderElement();
			this.details_visible = false;
			
			this.$('.back').click(function(){
			    self.gui.back();
			});
			   
			this.$('.next').click(function(){   
				self.save_changes();
				self.gui.back();    // FIXME HUH ?
			});
			
			   var rooms = this.pos.hotel_folio_line;
			   this.render_room_list(rooms);
			   
	        this.$('.room-list-contents').delegate('.room-line','click',function(event){
	        	var line_data;
	        	var room_name;
	        	var customer_name;
	        	var folio_line_id;
	        	var folio_ids;
	        	var partner_id = $($(this).children()[2]).data('cust-id');
	        	self.pos.get_order().set_client(self.pos.db.get_partner_by_id(parseInt(partner_id)));
	        	customer_name = $($(this).children()[2]).text();
	        	room_name = $($(this).children()[0]).text();
	        	folio_ids = $($(this).children()[1]).text();
	        	folio_line_id =  parseInt($(this).data('id'));
	        	self.pos.get_order().set_folio_ids(folio_ids);
	        	self.pos.get_order().set_folio_line_id(folio_line_id);
	        	self.pos.get_order().set_room_name(room_name);
	        	$('.js_room_name').text( room_name ? room_name : _t('Room') );
	            $('.js_customer_name').text( customer_name ? customer_name : _t('Customer') );
	            $('.set-customer').text( customer_name ? customer_name : _t('Customer') );
	            self.gui.back();
	            
	        });

//	        var search_timeout = null;
//
//	        if(this.pos.config.iface_vkeyboard && this.chrome.widget.keyboard){
//	            this.chrome.widget.keyboard.connect(this.$('.searchbox input'));
//	        }
//
//	        this.$('.searchbox input').on('keypress',function(event){
//	        	console.log('\n\n in search ========');
//	            clearTimeout(search_timeout);
//
//	            var query = this.value;
//	            console.log('\n\n\n query ===',query);
//
//	            search_timeout = setTimeout(function(){
//	            	console.log('\n\n in search_timeout ======');
//	                self.perform_search(query,event.which === 13);
//	            },70);
//	        });
//
//	        this.$('.searchbox .search-clear').click(function(){
//	            self.clear_search();
//	        });
	       
		   },
		   
		   
//		   perform_search: function(query, associate_result){
//		        var rooms;
//		        console.log('\n\n\n associate_result ====',associate_result);
//		        console.log('\n\n\n query = after==',query);
//		        if(query){
//		        	console.log('\n\n this ======',this,query);
//		        	console.log('\n\n this.pos ======',this.pos);
//		        	console.log('\n\n this.pos.hotel_folio_line ======',this.pos.hotel_folio_line);
//		            rooms = this.pos.hotel_folio_line;
//		            this.render_room_list(rooms);
//		        }
////		            this.display_client_details('hide');
//		            if ( associate_result && rooms.length === 1){
////		                this.new_client = customers[0];
//		                this.save_changes();
////		                this.gui.back();
//		            }
////		            this.render_list(customers);
////		        }else{
////		            customers = this.pos.db.get_partners_sorted();
////		            this.render_list(customers);
////		        }
//		    },
//		    
//		    clear_search: function(){
//		    	 var rooms = this.pos.hotel_folio_line(query);
//		         this.render_list(rooms);
//		        this.$('.searchbox input')[0].value = '';
//		        this.$('.searchbox input').focus();
//		    },
		   
		   
		   
		   render_room_list: function(rooms){
			   console.log("Rooomssss   ",rooms)
			   var d = new Date();
			    var current_date = new Date(String(d. getFullYear())+"-"+String(d.getMonth()+1)+"-"+String(d.getDate())).setHours(0,0,0,0);
			    var contents = this.$el[0].querySelector('.room-list-contents');
		        contents.innerHTML = "";
		        for(var i = 0, len = Math.min(rooms.length,1000); i < len; i++){
		            var room    = rooms[i];
		            var checkin = room.checkin_date;
		            var checkin_dt = new Date(checkin.split(" ")[0]).setHours(0,0,0,0);
		            var checkout = room.checkout_date;
		            var checkout_dt = new Date(checkout.split(" ")[0]).setHours(0,0,0,0);
		            if(checkin_dt <= current_date && checkout_dt >= current_date){
			        	var hotel_folio = this.pos.hotel_folio;
			        	console.log("Hotel Folioooo    ",hotel_folio)
			        	for (var j=0; j<hotel_folio.length; j++){
			        		if(room.folio_id[0] === hotel_folio[j].id){
			        			room['partner_id'] = hotel_folio[j].partner_id[0];	
			        			room['partner_name'] = hotel_folio[j].partner_id[1];
							}
			        	}
			           
			            if(room){
			            	var roomline_html = QWeb.render('RoomLine',{widget: this, room:rooms[i]});
			            	var roomline = document.createElement('tbody');
			                roomline.innerHTML = roomline_html;
			                roomline = roomline.childNodes[1];
			            }
			            
			            if( room === this.old_room ){
			                roomline.classList.add('highlight');
			            }else{
			                roomline.classList.remove('highlight');
			            }
			            contents.appendChild(roomline);
			        }
		      }
		    },
		
	});



	gui.define_screen({
		name:'roomlist', 
		widget:RoomListScreenWidget
		});
	

});


