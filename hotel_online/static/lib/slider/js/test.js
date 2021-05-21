$(document).ready(function() {
            $('.image-gallery-cls').lightSlider({
                gallery:true,
                item:1,
                thumbItem:4,
                slideMargin: 0,
                speed:500,
                auto:true,
                loop:true,
                onSliderLoad: function() {
                    $('.image-gallery-cls').removeClass('cS-hidden');
                }  
            });
            
	$("#room_form").submit(function(e){
	        
		var myform = document.getElementById('room_form');
		    var inputTags = myform.getElementsByTagName('input');
		    console.log("inputTags::::::::::::::::::",inputTags)

		    var checkboxCount = 0;
		    var flag = false;
		    for (var i=0, length = inputTags.length; i<length; i++)
		    {
		        if (inputTags[i].type == 'checkbox')
		        {
		            console.log("inputTags[i].type:::::::::::::",inputTags[i].type)

		            var cb = $('.test');
		            if (cb.is(':checked'))
		            {
		                flag = true;
		            }
		            checkboxCount++;
		        }
		    }
		    if(flag == false)
		    {
		        alert("Please Select Atleast One Room!");
				e.preventDefault();
		    }
	
	
	    });
});

		function onchange_tax(val)
            {
            	tot = parseFloat($("#total").val())+parseFloat($("#tax").val())
            	$("#grand_total").val(tot)
            }
           