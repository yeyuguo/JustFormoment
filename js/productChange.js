
    var OrderList;
	var NeedPayOrderList = new Array();
	var SendOrderList= new Array();
	var NeedAcceptOrderList= new Array();
    $(document).on("pageshow","#JQM_OrderList",function(){
	 $("#OrderList").find("li").remove(); //清空列表
		$.mobile.loading('show',{text:"请稍后...",textVisible:true,theme:"b"});
		//alert(localStorage.getItem("H_URL")+"yxtws/v1/hxyxt/orders");
		$.ajax({
			url:localStorage.getItem("H_URL")+"yxtws/v1/hxyxt/orders",
			type:"GET",
			data:{access_token:localStorage.getItem("access_token")},
			dataType:"json",
			contentType:"application/x-www-form-urlencoded; charset=utf-8",
			success:function(data){
				$.mobile.loading("hide");
				//alert(JSON.stringify(data));
				if(data.orders.length>0){
					for(var i=0;i<data.orders.length;i++){
			         	var order_state;
			        	var order_price = data.orders[i].total.formattedValue;
				        var order_time = data.orders[i].placed;
				        var date_time = order_time.substr(0, 10) +" "+ order_time.substr(11, 8);
				        if(data.orders[i].statusDisplay == "processing"){
					           order_state = "处理中";
				        }
						var map_state = data.orders[i].status;
						var order_state;
						if(map_state == null || map_state == ""){
							order_state = data.orders[i].statusDisplay;
						}else{
							order_state = data.orders[i].status.code;
						}
						
						//alert(order_state);
						if(order_state == "created"){
							var j = NeedPayOrderList.length;
							NeedPayOrderList[j]=data.orders[i];
						
						}
						if(order_state == "PICKING"){
							var j = SendOrderList.length;
							SendOrderList[j]=data.orders[i];
						}
						if(order_state == "SHIPPED"){
							//alert("shipped");
							var j = NeedAcceptOrderList.length;
							//alert(j);
							NeedAcceptOrderList[j]=data.orders[i];
						}
                       var liItem ='<li> <div class="ListItem"> <a href="#" rel="external" onClick=SelectOrder('+i+')>' +
                      ' <div class="Order_info">'+
                      ' <div class="TotalPrice" id="eamilID"><span>订单号：'+data.orders[i].code+'</span></div>'+
                      ' <div class="OrderState" id="sexID"><span>订单状态：'+order_state+'</span></div>'+
                      ' <div class="OrderTime" id="tellID"><span>下单时间：'+date_time+'</span></div>'+
                      ' <div class="OrderNumber" id="birthdayID"><span>总价：'+order_price+'</span></div>'+
                      ' </div> </a></div></li> ';
				     
					
					
					  $("#OrderList").append(liItem);  //添加到ul中
				}
					OrderList = data;  //赋值
		
				}
				$("#OrderList").listview('refresh');
			},
			error:function(msg){
				//alert(JSON.stringify(msg));
				$.mobile.loading("hide");
				//window.location="Login.html";
				//window.location.load();	
			}
		});
});

       //跳转到对应的详情页
		function SelectOrder(i){
		 // alert("进入跳转"+JSON.stringify(OrderList.orders[i]));
		 
		  localStorage.setItem("OrderObj",JSON.stringify(OrderList.orders[i]));
		  window.location="MyOrderDetails.html";
		  window.location.load();	
	   }
    
		 //点击类别
		function OnclickClass(i){
			var RefreshOrderList;
			if(i == 1){
				RefreshOrderList = OrderList.orders;
			}else if(i == 2){
				RefreshOrderList = NeedPayOrderList;
			}
			else if(i == 3){
				RefreshOrderList = SendOrderList;
			}
			else if(i ==4){
				RefreshOrderList = NeedAcceptOrderList;
			}
			if(RefreshOrderList.length>0){
				$("#OrderList").find("li").remove(); //清空列表
				for(var i=0;i<RefreshOrderList.length;i++){
			         	var order_state;
			        	var order_price = RefreshOrderList[i].total.formattedValue;
				        var order_time = RefreshOrderList[i].placed;
				        var date_time = order_time.substr(0, 10) +" "+ order_time.substr(11, 8);
				        if(RefreshOrderList[i].statusDisplay == "processing"){
					           order_state = "处理中";
				        }
						
                       var liItem ='<li> <div class="ListItem"> <a href="#" rel="external" onClick=SelectOrder('+i+')>' +
                      ' <div class="Order_info">'+
                      ' <div class="TotalPrice" id="eamilID"><span>订单号：'+RefreshOrderList[i].code+'</span></div>'+
                      ' <div class="OrderState" id="sexID"><span>订单状态：'+order_state+'</span></div>'+
                      ' <div class="OrderTime" id="tellID"><span>下单时间：'+date_time+'</span></div>'+
                      ' <div class="OrderNumber" id="birthdayID"><span>总价：'+order_price+'</span></div>'+
                      ' </div> </a></div></li> ';
				     
					
					  $("#OrderList").append(liItem);  //添加到ul中
				}
				$("#OrderList").listview('refresh');
			}else{
				
			}
		}
