var source;	//成员变量，用来判断用户是加入购物车还是立即购买
var flag;
$(document).ready(function() {
		
		/*  点击加入购物车.立即购买弹出选项窗口 */
		$(".select").click(function() {
			source=$(this).html();
			show();
		});
		
		/* 请选择颜色和尺寸 */
		$(".div_item_type").click(function() {
			source=$(this).html();
			showadd();	
		});
		/* 点击close按钮 */
		$("#close").click(function() {
			var selects=$("dd.Classify").html();
			ShoppingOrClose();
			$(".div_item_type").html(selects);
			$(".div_item_type").css("font-size","10px");
		});
		
		/* 增加购买数量 */
		$("#jia").click(function(){
		  var number=parseInt( $("#num").val());
		  number+=1;
		  $("#num").val(number);
		  var num=$("#num").val();
		  $(".numbers").html("×&nbsp;"+num);
		});
		
		/* 减少购买数量 */
		$("#jian").click(function(){
		  var number=parseInt( $("#num").val());
		  number-=1;
		  if(number<1){
		    return false;
		  }
		  $("#num").val(number);
		  var num=$("#num").val();
		  $(".numbers").html("×&nbsp;"+num);
		});
		
		/*单击--移除原有样式，添加新样式
		     再次单击--移除新添加的样式，还原原有样式
		*/
		$(".sizeselect").click(function(){
			if($(this).hasClass("selected")){
				$(this).removeClass("selected");
				$(this).addClass("sizeselect");
				$("dd.Classify").html("请选择规格、分类");
			}else{
				if($(".size>div").hasClass("selected")){
					$(".size>div").removeClass("selected");
					$(".size>div").addClass("sizeselect");
				};
				$(this).removeClass("sizeselect");
				$(this).toggleClass("selected");
				var selects=$(this).html();
				 var num=$("#num").val();
				 $("dd.Classify").html("\""+selects+"\"");
				 $("dd.Classify").append("<span class='numbers'></span>");
				 $(".numbers").html("&nbsp;×"+num);
				
			}
		});
		
		//确定订单
		$("#confirm").click(function(){			
			sure();	
		 
		});
		
		//加入购物车
		$("#AddCar").click(function(){
			source=$(this).html();
			if($(this).parents().hasClass("btn_AddCar")){
				flag="true";
			}
			
			alert("jinru");
			
			
			$.mobile.loading('show',{text:"正在提交...",textVisible:true,theme:"b"});
		//alert(localStorage.getItem("Register_Url")+"SS_AddCart?access_token="+localStorage.getItem("access_token")+"&ACookieID="+localStorage.getItem("CookieID"));
		$.ajax({
			url:localStorage.getItem("Register_Url")+"SS_AddCart",
			type:"GET",
			data:{AAccess_token:localStorage.getItem("access_token"),ACookieID:localStorage.getItem("CookieID"),AMatnr:"100004524",ACount:3},
			dataType:"jsonp",
			jsonp:"BaseCallback",
			contentType:"application/json; charset=utf-8",
			success:function(data){
				$.mobile.loading("hide");
				alert(JSON.stringify(data));
				sure();
			},
			error:function(msg){
				$.mobile.loading("hide");
				alert(JSON.stringify(msg));
				//window.location="Login.html";
				//window.location.load();	
			}
		});
			
			
			
			
			
			
		});
		
		//立即购买
		$("#sell").click(function(){
			source=$(this).html();
			if($(this).parents().hasClass("btn_AddCar")){
				flag="true";
			}
			sure();
		});
		
		
		//继续购物
		$(".Shopping").click(function(){
		   ShoppingOrClose();
		});
		
		//关闭提示框
		$("#closeConfirm").click(function(){
		  ShoppingOrClose();
		});
		
		
		//到购物车结算
		$(".GoToPay").click(function(){
		  window.location.href="ShoppingCart.html";
		});
		
	});
	
	//显示可选择的模块
	//已经选择加入购物车或者立即购买
	function show(){
		$(".WindowShow").css("display", "block");
		$(".btn_AddCar").css("display", "none");
		$(".btn_Confirm").css("display", "block");
		$(".jqm-hxyy").css("opacity", "0.2");
	}
	//隐藏可选择的模块
	function notshow(){
		 $("#AddOK").css("display","block");
		 $(".WindowShow").css("display", "none");
		 $(".jqm-hxyy").css("opacity", "0.05");
	}
	
	//显示可选择的模块
	//已经选择加入购物车或者立即购买
	function showadd(){
		$(".WindowShow").css("display", "block");
		$(".btn_Confirm").css("display", "none");
		$(".btn_AddCar").css("display", "block");
		$(".jqm-hxyy").css("opacity", "0.2");
		
	}
	
	function notshowadd(){
		$(".btn_AddCar").css("display", "block");
		$(".btn_Confirm").css("display", "none");
	}
	
	//选择继续购物或者关闭提示框
	function ShoppingOrClose(){
	  $(".WindowShow").css("display", "none");
	  $("#AddOK").css("display","none");
	  $(".jqm-hxyy").css("opacity", "1");
	}
	
	
	//确定
	function sure(){
		//确定订单
		var selects=$("dd.Classify").html();
		if(selects!="请选择规格、分类"){
			if(source=="立即购买"){//立即购买
				alert("跳转到付款页面！");
				window.location.href="OrderPay.html";
			}else if(source=="加入购物车"){//加入购物车
				alert("加入购物车！");
				notshow();
				$(".div_item_type").html(selects);
			}else{//确定按钮
				notshow();
				$(".div_item_type").html(selects);
			}
			$(".div_item_type").css("font-size","10px");
		}else{
			if(flag=="true"){
				$(".WindowShow").css("display", "block");
				$(".btn_AddCar").css("display", "block");
				$(".btn_Confirm").css("display", "none");
			}
			alert("请选择规格、分类");
			
		}
		
	}
