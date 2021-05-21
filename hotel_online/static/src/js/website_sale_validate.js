odoo.define('hotel_online.validate', function(require) {
	"use strict";
//
//	var ajax = require('web.ajax');
//
//	$(document).ready(function () {
//	    var _poll_nbr = 0;
//	
//	    function payment_transaction_poll_status() {
//	    	console.log("innnnn payment transaction");
//	        var order_node = $('div.oe_website_sale_tx_status');
//	        console.log(order_node);
//	        if (! order_node || order_node.data('orderId') === undefined) {
//	            return;
//	        }
//	        var order_id = order_node.data('orderId');
//	        console.log(order_id);
//	        return ajax.jsonRpc('/shop/payment/get_status123/' + order_id, 'call', {
//	        }).then(function (result) {
//	            var tx_node = $('div.oe_website_sale_tx_status');
//	            console.log(tx_node);
//	            _poll_nbr += 1;
//	            if (result.state == 'pending' && result.validation == 'automatic' && _poll_nbr <= 5) {
//	                var txt = result.mesage;
//	                setTimeout(function () { payment_transaction_poll_status();   }, 1000);
//	            }
//	            else {
//	                var txt = result.message;
//	            }
//	            tx_node.html(txt);
//	        });
//	    }
//	    console.log("ouuuuuuttt payment transaction");
//		//alert("hiih1111111111111111111");
//	    payment_transaction_poll_status();
//	});
//


	$(document).ready(function () {
		if ($(".checkout_autoformat").length) {
	        $('.oe_website_sale').on('change', "select[name='country_id']", function () {
//	            clickwatch(function() {
//	            	alert("Comingggggg");
//	                if ($("#country_id").val()) {
//	                    ajax.jsonRpc("/shop/country_infos/" + $("#country_id").val(), 'call', {mode: 'shipping'}).then(
//	                        function(data) {
//	                            // placeholder phone_code
//	                            //$("input[name='phone']").attr('placeholder', data.phone_code !== 0 ? '+'+ data.phone_code : '');
//
//	                            // populate states and display
//	                            var selectStates = $("select[name='state_id']");
//	                            // dont reload state at first loading (done in qweb)
//	                            if (selectStates.data('init')===0 || selectStates.find('option').length===1) {
//	                                if (data.states.length) {
//	                                    selectStates.html('');
//	                                    _.each(data.states, function(x) {
//	                                        var opt = $('<option>').text(x[1])
//	                                            .attr('value', x[0])
//	                                            .attr('data-code', x[2]);
//	                                        selectStates.append(opt);
//	                                    });
//	                                    selectStates.parent('div').show();
//	                                }
//	                                else {
//	                                    selectStates.val('').parent('div').hide();
//	                                }
//	                                selectStates.data('init', 0);
//	                            }
//	                            else {
//	                                selectStates.data('init', 0);
//	                            }
//
//	                            // manage fields order / visibility
//	                            if (data.fields) {
//	                                if ($.inArray('zip', data.fields) > $.inArray('city', data.fields)){
//	                                    $(".div_zip").before($(".div_city"));
//	                                }
//	                                else {
//	                                    $(".div_zip").after($(".div_city"));
//	                                }
//	                                var all_fields = ["street", "zip", "city", "country_name"]; // "state_code"];
//	                                _.each(all_fields, function(field) {
//	                                    $(".checkout_autoformat .div_" + field.split('_')[0]).toggle($.inArray(field, data.fields)>=0);
//	                                });
//	                            }
//	                        }
//	                    );
//	                }
//	            }, 500);
	        });
	    }
	    $("select[name='country_id']").change();
	});
});