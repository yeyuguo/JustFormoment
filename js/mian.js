//获取上个连接传过来的参数
//此处注意decodeURI解码参数，否则中午为乱码
function GetQueryString(sProp){
	var re=new RegExp("[&,?]"+sProp+"=([^\\&]*)","i");
	var a=re.exec(decodeURI(document.location.search));
	if(a==null)
		return "";
	return a[1];
}

//JSON日期格式转换
function jsonDateFormat(jsonDate) {
    try {
        var date = new Date(parseInt(jsonDate.replace("/Date(", "").replace(")/", "").replace("+0800",""), 10));
		//return data.Format("yyyy年MM月dd日"); 
		
		//return date.toLocaleString();
        var month = (date.getMonth()+ 1) < 10 ? "0" + (date.getMonth()+ 1) : (date.getMonth()+ 1);
        var day = date.getDate() < 10 ? "0" + date.getDate() : date.getDate();
        //var hours = date.getHours();
        //var minutes = date.getMinutes();
        //var seconds = date.getSeconds();
        //var milliseconds = date.getMilliseconds();
		
		return date.getFullYear() + "年" + month + "月" + day + "日";
        //return date.getFullYear() + "-" + month + "-" + date + " " + hours + ":" + minutes + ":" + seconds + "." + milliseconds;
    } catch (ex) {
        return "----";
    }
}

function ChangeDateFormat(cellval)
	 {
		 var date = new Date(parseInt(cellval.replace("/Date(", "").replace(")/", ""), 10));
		 var month = date.getMonth() + 1 < 10 ? "0" + (date.getMonth() + 1) : date.getMonth() + 1;
		 var currentDate = date.getDate() < 10 ? "0" + date.getDate() : date.getDate();
		 return date.getFullYear() + "-" + month + "-" + currentDate;
	 }
	 
//获取当前日期  昨天数据
function GetDateTimeNow(){
	var todydate=new Date();
	var yesterday_milliseconds=todydate.getTime()-1000*60*60*24;
	var yesterday=new Date();
	yesterday.setTime(yesterday_milliseconds);
	var strYear=yesterday.getFullYear();
	var strDay=yesterday.getDate();
	var strMonth=yesterday.getMonth()+1;
	if(strMonth<10){
		strMonth ="0"+strMonth;
	}
	if(strDay<10){
		strDay = "0"+strDay;
	}
	var strYesterday=strYear + "-" + strMonth + "-" + strDay;
	return strYesterday;
}
//当天数据
function GetDateNow(){
	var todydate=new Date();
	var stryear=todydate.getFullYear();
	var strmonth=todydate.getMonth()+1;
	var strday=todydate.getDate();
	if(strmonth<10){
		strmonth ="0"+strmonth;
	}
	if(strday<10){
		strday = "0"+strday;
	}
	var strTodydate=stryear+"-"+strmonth+"-"+strday;
	return strTodydate;
}
//获取上个月yyyy-MM格式
function GetDateMonthNow(){
	var todydate=new Date();
	var strYear = todydate.getFullYear();
	var strMonth = todydate.getMonth();
	if(strMonth<10){
		strMonth ="0"+strMonth;
	}
	var strUpMonth=strYear+"-"+strMonth;
	return strUpMonth;
}
//获取上个月yyyyMM格式
function GetDateMonthNowNew(){
	var todydate=new Date();
	var strYear = todydate.getFullYear();
	var strMonth = todydate.getMonth();
	if(strMonth<10){
		strMonth ="0"+strMonth;
	}
	var strUpMonth=strYear+strMonth;
	return strUpMonth;
}


/*保留2位小数，千分位显示*/
function format (num) {
    return (num.toFixed(2) + '').replace(/\d{1,3}(?=(\d{3})+(\.\d*)?$)/g, '$&,');
}
/*整数的千分位显示*/
function formatNum (num){
	return (Math.round(num) + '').replace(/\d{1,3}(?=(\d{3})+(\.\d*)?$)/g, '$&,');
}


/*标注3张图片的轮播图加载方法*/
function showlunbo(){
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
			n = n <= (count - 1) ? --n :2;
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
			i=2;
			n=2;
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
			n = n <= (count - 1) ? --n :2;
		}else{
			n = n >= (count - 1) ? 0 : ++n;
		}
			$(".num a").eq(n).trigger('click');
		}, 3000);
	});	
}