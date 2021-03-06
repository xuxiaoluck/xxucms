

//定义扩展函数，对输入的金额进行检测
$.fn.extend({
	moneyFormat : function () {
		return this.each(function () {
			$(this).keyup(function () {
				var reg = /^\d*\.?\d{0,2}$/,
				reg2 = /(?:\d*\.\d{0,2}|\d+)/,
				reg3 = /[^.0-9]+/;
				var _val = $(this).val(),
				isPlus = /^-/.test(_val),
				_val = isPlus ? _val.substr(1) : _val;
				if (!reg.test(_val)) {
					_val = _val.replace(reg3, "").match(reg2);
					_val = _val == null ? "" : _val[0];
					$(this).val(isPlus ? ("-" + _val) : _val);
				}
			}).blur(function () {
				var reg1 = /^\d+$/,
				reg2 = /^\.\d{0,2}$/,
				reg3 = /^\d+\.\d{0,2}$/,
				reg4 = /^0+(?:[1-9]\d*|0)\.\d{0,2}$/,
				reg5 = /^0+((?:[1-9]\d*|0)\.\d{0,2})$/;
				var _val = $(this).val(),
				isPlus = /^-/.test(_val),
				_val = isPlus ? _val.substr(1) : _val;
				if (reg1.test(_val)) {
					_val = _val + ".00";
				}
				if (reg4.test(_val)) {
					_val = _val.replace(reg5, "$1");
				}
				if (reg2.test(_val)) {
					_val = "0" + _val;
				}
				if (reg3.test(_val)) {
					var len = _val.length - _val.indexOf(".") - 1,
					str = "";
					for (var i = 0; i < 2 - len; i++) {
						str += "0";
					}
					_val += str;
				}
				$(this).val(isPlus ? ("-" + _val) : _val);
			});
		});
	}
});


/*  用到的一些说明
 在select 中增加一条
  $("#addbookselectpublisher").append("<option>"+$("#addpublishername").val()+"</option>");
 */

$(function(){

   //1  初始化日期控件
   $("#cost_date").parent().datepicker({
           format: 'yyyy-mm-dd',
           //minView:'month',
           language: 'zh-CN',
           autoclose:true,
           startDate:new Date()
   });

   //2  设置浮点录入限制 只有输入两位小数的浮点数
    $("#cost_money").moneyFormat();

    //3 增加分类
    $("#addtype_btn").click(function(){
        var typename = $("#cost_addtype").val();
        if (typename == "")
        {
            alert("类别名不能为空");
            return;
        }
        $.post("/cost/addonetype/",
               {
                   typename: typename
               },
               function(ret){
                   if (ret.exists) //已存在
                       $("#costtypepanelhead").html("增加新的分类" + ret.info);
                   else{
                       $("#costtypepanelhead").html("增加新的分类" + ret.info);
                       $("#cost_type").append("<option value = " + ret.id + ">" +typename + "</option>");
                   }
               }
              );
    });

    //增加科目
 $("#addsubject_btn").click(function(){
        var subjectname = $("#cost_addsubject").val();
        if (subjectname == "")
        {
            alert("科目不能为空");
            return;
        }
        $.post("/cost/addonesubject/",
               {
                   subjectname: subjectname
               },
               function(ret){
                   if (ret.exists) //已存在
                       $("#costsubjectpanelhead").html("增加新的科目" + ret.info);
                   else{
                       $("#costsubjectpanelhead").html("增加新的科目" + ret.info);
                       $("#cost_subject").append("<option value = " + ret.id + ">" + subjectname + "</option>");
                   }
               }
              );
 });


    //5  点击了增加一条收支记录

    $("#inputcost_btn").click(function(){

        var costtypeid = $("#cost_type").val();
        //得到选中的值(设置的 value)而非文本（用find("option:selected").text()得到选中的文本，直接用 text()返回所有文本）
        var costsubjectid = $("#cost_subject").val();
        var costdate = $("#cost_date").val();
        var costmoney = $("#cost_money").val();
        var costmemo = $("#cost_memo").val();


        if (costdate == "" || costmoney == "")
        {
            alert("日期、金额不能为空!");
            return;
        }


         $.post("/cost/addonecost/",
                            {
                                costtypeid:costtypeid,
                                costsubjectid:costsubjectid,
                                costdate:costdate,
                                costmoney:costmoney,
                                costmemo:costmemo
                            },
                            function(ret){
                                $("#showaddcostinforlt").html("录入收支数据" + ret);
                            });
        //post ajax增加数据


    }); //click(fun)


}); //$(fun)

