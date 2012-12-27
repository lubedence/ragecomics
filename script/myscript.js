$(document).ready(function() {
		
//social-sharing
socialSharing();

//voting		
voting();

//init sidelist
sidelist();

//rageComic fullsize
showImg();
});






//--------------------------------------------------------------------------------------------
//---FUNCTIONS--------------------------------------------------------------------------------
//--------------------------------------------------------------------------------------------



function is_touch_device(){
  return !!('ontouchstart' in window);
}

function showImg(){
	var hidden = false;
	$('.comic_image img').each(function() {
		$(this).click(function() {
			//if(!hidden){	
			
				hidden = true;
				$('#all').hide();
				$('body').css('overflow','auto');
				$('body').append('<div id="just_img"><div id="back_to_content"><p>BACK</p></div></div>');
				$('#just_img').append($(this).clone().css('max-width','none'));
				
				$('#back_to_content').click(function() {
						$('body').css('overflow','hidden');
						$('#just_img').remove();
						$('#all').show();
				});
			//}
			//else{
			//	hidden = false;
			//	$('body').css('overflow','hidden');
			//	$('#all').show();
			//}
		});
	});
}

function socialSharing(){
	 $('.socialshareprivacy').each(function() {
			 var c_uri = window.location.host+window.location.pathname+'#'+$(this).parents('.comic').attr('name');
			 $(this).socialSharePrivacy({uri : c_uri}); 
	 });
}

function voting(){
	
	$('.up-img').each(function() {
		var id = $(this).data('id');
		if(getCookie("vote_"+id)){
			$(this).attr('src','../../static/images/thumbs_up_voted.png');
		}
	});
	
	$(".up-img").click(function() {
		var id = $(this).data('id');
		if(!getCookie("vote_"+id)){
			var that = $(this);
			$.post("/vote_up", { 
				id: id
				},
				function(data) {
					if(data != -1){
						that.next('span').html(data+' - Voted, thanks!');
						that.attr('src','../../static/images/thumbs_up_voted.png');
						setCookie("vote_"+id,"up",365);
					}
				}
			);
		}
		else{
			var msg = ' - You already voted!';
			var loc = $(this).next('span');
			if(loc.html().indexOf(msg) < 0){
				loc.append(msg);
			}
			
		}
	});
}

function sidelist() {
	
	
	//filter part
		
	$('#event_search').click(function() {
		$('#user_search').removeClass('darker-bg');
		
		if($('#event_form').is(":visible")){
			$('#event_form').addClass('not-visible');
			$('#event_search').removeClass('darker-bg');
		}
		else{
			$('#user_form').addClass('not-visible');
			$('#event_form').removeClass('not-visible');
			$('#event_search').addClass('darker-bg');
		}
	});
	
	$('#user_search').click(function() {
		$('#event_search').removeClass('darker-bg');
		
		if($('#user_form').is(":visible")){
			$('#user_form').addClass('not-visible');
			$('#user_search').removeClass('darker-bg');
		}
		else{
			$('#event_form').addClass('not-visible');
			$('#user_form').removeClass('not-visible');
			$('#user_search').addClass('darker-bg');
		}
	});
	
	//end filter
	
	if($("#wrapper_sidelist").length == 0){
		$("#wrapper_main").width("100%");
	}
	else{
		var c_width = getCookie('sidelist_width');
		if (c_width!=null && c_width!=""){
			$("#wrapper_sidelist").width(c_width+"%");
			$("#wrapper_main").width((100-c_width)+"%");
		}
	}
	
	//scroll to selected element
	var selected = $('.event-element.selected');
	if(selected.length){
		var wrapper = $('#wrapper_listelements');
		wrapper.scrollTop(selected.position().top - wrapper.position().top);
	}
	
	var resize = false;
	var sidelist_width = $("#wrapper_sidelist").width();
	var main_width = $("#wrapper_main").width();
	var percent = (sidelist_width / (main_width+sidelist_width))*100;
	
	if(!is_touch_device()){
		
		//resize sidelist with NO-TOUCH devices---------------------------------------------------------------------------------------------------	
		$("#sidelist_slider").mousedown(function(event)
		{
			resize = event.pageX;	
			$("body").addClass('not-selectable cursor-move');
			$("#sidelist_slider").addClass('resize-big');
		});
			
		$(document).mouseup(function(event)
		{
			if(resize){
				resize = false;
				sidelist_width = $("#wrapper_sidelist").width();
				main_width = $("#wrapper_main").width();
				percent = (sidelist_width / (main_width+sidelist_width))*100;
				
				$("body").removeClass('not-selectable cursor-move');
				$("#sidelist_slider").removeClass('resize-big');
				
				//cookie save sidelist-width 
				setCookie('sidelist_width',percent,365);
			}
		});
		
		$(document).mousemove(function(event)
		{
			if (resize)
			{
				var move = ((resize - event.pageX) / (main_width+sidelist_width))*100;
				resizing(move);
			}
		});
		//end resize sidelist NO-TOUCH---------------------------------------------------------------------------------------------------------------------
	}
	else{
		//bigger margin for bigger sidelist-slider (for people with large fingers)
		$("#wrapper_content").removeClass('small-horizontal-margin').addClass('big-horizontal-margin');
		$("#sidelist_slider").removeClass('resize-sidelist').addClass('resize-sidelist-big');
		
		//resize sidelist TOUCH-------------------------------------------------------------------------------------------------------------------------
		$("#sidelist_slider").bind('touchstart', function(event)
		{
			var e = event.originalEvent;
			//android bug: http://code.google.com/p/android/issues/detail?id=19827
			if( navigator.userAgent.match(/Android/i) ) {
				e.preventDefault();
			}
			
			resize = e.touches[0].pageX;				
			$("body").addClass('not-selectable');
		});
				
		$(document).bind('touchend', function(event)
		{
			if(resize){
				resize = false;
				sidelist_width = $("#wrapper_sidelist").width();
				main_width = $("#wrapper_main").width();
				percent = (sidelist_width / (main_width+sidelist_width))*100;
	
				$("body").removeClass('not-selectable');
				
				//cookie save sidelist-width 
				setCookie('sidelist_width',percent,365);
			}
		});
			
		$(document).bind('touchmove', function(event)	
		{
			if (resize)
			{
				var e = event.originalEvent;
				//android bug: http://code.google.com/p/android/issues/detail?id=19827
				if( navigator.userAgent.match(/Android/i) ) {
					e.preventDefault();
				}
						
				var move = ((resize - e.touches[0].pageX) / (main_width+sidelist_width))*100;
				resizing(move);
			}
		});
	//end resize sidelist TOUCH---------------------------------------------------------------------------------------------------------------------
	}
	
	
	function resizing(move){
		if(percent + move >= 10 && $("#content_sidelist").hasClass('not-visible'))
		{
			$("#content_sidelist").removeClass('not-visible');
		}
				
		if (percent + move > 20 && percent + move < 30)
		{
			$("#wrapper_main").width('75%');
			$("#wrapper_sidelist").width('25%');
		}
		else if (percent + move > 50)
		{
			$("#wrapper_main").width('50%');
			$("#wrapper_sidelist").width('50%');
		}
		else if (percent + move < 10)
		{
			$("#wrapper_main").width('100%');
			$("#wrapper_sidelist").width('0');
			$("#content_sidelist").addClass('not-visible');
		}
		else
		{
			$("#wrapper_sidelist").width(percent + move+'%');
			$("#wrapper_main").width(100 - (percent + move)+'%');
		}
	}
	
}



//w3schools.com
function setCookie(c_name,value,exdays)
{
	var exdate=new Date();
	exdate.setDate(exdate.getDate() + exdays);
	var c_value=escape(value) + ((exdays==null) ? "" : "; expires="+exdate.toUTCString())+ ";path=/";
	document.cookie=c_name + "=" + c_value;
}

//w3schools.com
function getCookie(c_name)
{
	var i,x,y,ARRcookies=document.cookie.split(";");
	for (i=0;i<ARRcookies.length;i++)
	{
	  x=ARRcookies[i].substr(0,ARRcookies[i].indexOf("="));
	  y=ARRcookies[i].substr(ARRcookies[i].indexOf("=")+1);
	  x=x.replace(/^\s+|\s+$/g,"");
	  if (x==c_name)
	    {
	    return unescape(y);
	    }
	  }
}

