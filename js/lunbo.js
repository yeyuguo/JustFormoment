// JavaScript Document

$(function(){
		var t = n = 0; count = $(".img_content a").size();
		var st=0;
		var play = ".play";
		var playText = ".play .text";
		var playNum = ".play .num a";
		var playConcent = ".play .img_content a";
		$(playConcent + ":not(:first)").hide();
		$(playText).html($(playConcent + ":first").find("img").attr("alt"));
		$(playNum + ":first").addClass("on");
		$(playNum).click(function() {
		   var i = $(this).text() - 1;
		   n = i;
		   if (i >= count) return;
		   $(playText).html($(playConcent).eq(i).find("img").attr('alt'));
		  // $(playText).unbind().click(function(){window.open($(playConcent).eq(i).attr('href'), "_blank")})
		   $(playConcent).filter(":visible").hide().parent().children().eq(i).fadeIn("fast");
		   $(this).removeClass("on").siblings().removeClass("on");
		   $(this).removeClass("on2").siblings().removeClass("on2");
		   $(this).addClass("on").siblings().addClass("on2");
		   
		});
		t = setInterval(function(){
			if(st==1){
				n = n <= (count - 1) ? --n :3;
			}else{
				n = n >= (count - 1) ? 0 : ++n;
			}
			$(".num a").eq(n).trigger('click');
		},3000);
		$(playConcent).bind("swiperight",function(){clearInterval(t)},function(){
			var i;
			st=0;
			if(n==0){
				i=1;
				n=1;
			}else{
				i=n+1;
				n++;
			}
			if(i>=count){
				i=0;
				n=0;
			}
			$(playText).html($(playConcent).eq(i).find("img").attr('alt'));
			$(playConcent).filter(":visible").hide().parent().children().eq(i).fadeIn(1200);
			$(".num a").eq(n).removeClass("on").siblings().removeClass("on");
			$(".num a").eq(n).removeClass("on2").siblings().removeClass("on2");
			$(".num a").eq(n).addClass("on").siblings().addClass("on2");
		})
		$(playConcent).bind("swipeleft",function(){clearInterval(t)},function(){
			
			var i;
			st=1;
			if(n==0){
				i=3;
				n=3;
			}else{
				i=n-1;
				n--;
			}
			$(playText).html($(playConcent).eq(i).find("img").attr('alt'));
			$(playConcent).filter(":visible").hide().parent().children().eq(i).fadeIn(1200);
			$(".num a").eq(n).removeClass("on").siblings().removeClass("on");
			$(".num a").eq(n).removeClass("on2").siblings().removeClass("on2");
			$(".num a").eq(n).addClass("on").siblings().addClass("on2");
		})
		
		$(play).hover(function(){clearInterval(t)}, function(){t = setInterval(function(){
			if(st==1){
				n = n <= (count - 1) ? --n :3;
			}else{
				n = n >= (count - 1) ? 0 : ++n;
			}
				$(".num a").eq(n).trigger('click');
			}, 3000);});										
	})