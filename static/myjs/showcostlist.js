//主页显示信息
function inittable_showcost(){
      $("#showcostlist_table").bootstrapTable("destroy");

      $("#showcostlist_table").bootstrapTable({
                 url: '/cost/getcostinfo/',  //请求后台的URL（*）
                 method: 'get',   //请求方式（*）
                 //toolbar: '#toolbar',  //工具按钮用哪个容器
                 striped: true,   //是否显示行间隔色
                 cache: false,   //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
                 pagination: true,   //是否显示分页（*）
                 sortable: false,   //是否启用排序
                 //sortOrder: "asc",   //排序方式
                 queryParams: function(params){
                     var pa = {limit: params.limit,offset:params.offset,sortfield:"date",
                               year:$("#showselectedyear").attr("value"),
                               month:$("#showselectedmonth").attr("value"),
                               costtype: $("#showselectedtype").attr("value"),
                               costsubject:$("#showselectedsubject").attr("value"),
                              };
                     return pa;
                 },//每页长、页号
                 queryParamsType: "limit",
                 sidePagination: "server",  //分页方式：client客户端分页，server服务端分页（*）
                 pageNumber:1,   //初始化加载第一页，默认第一页
                 pageSize: 20,   //每页的记录行数（*）
                 pageList: [20, 30, 50, 100], //可供选择的每页的行数（*）
                 strictSearch: true,
                 clickToSelect: true,  //是否启用点击选中行
                 //height: 460,   //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度
                 uniqueId: "code",   //每一行的唯一标识，一般为主键列
                 cardView: false,   //是否显示详细视图
                 detailView: false,   //是否显示父子表
                 //silent:true,
                 columns: [{
                     field: 'date',
                     title: '日期'
                 }, {
                     field: 'costtype',
                     title: '类别'
                 },{
                     field:'costsubject',
                     title:'科目'
                 },{
                     field: 'money',
                     title: '金额'
                 },{
                     field:'name',
                     title:'明细'
                 }],
                 rowStyle: function (row, index) {
                     //这里有5个取值代表5中颜色['active', 'success', 'info', 'warning', 'danger'];
                     var strclass = "";
                     if (row.costtype == "支出") {
                         strclass = 'warning';//还有一个active danger
                     }
                     else if (row.costtype == "借出") {
                         strclass = 'danger';
                     }
                     else if (row.costtype.substring(0,1) == "还回") {
                         strclass = 'info';
                     }
                     else if (row.costtype == "收入") {
                         strclass = 'success';
                     }
                     else{
                         return {};
                     }

                     return {classes: strclass}
                     //return {}
                 },
                 responseHandler: function(res) {   //处理 从后端 返回的数据
                     //console.log(res);
                     if (res == 0) {
                         alert('无数据！');
                     } else {
                         //var orderListData = res['rows'];  //##### 重要！！#####
                         return res;//orderListData;
                     }
                 },
                 onLoadError: function (status) {
                     //console.log(status);
                     $('#showcostlist_table').bootstrapTable('removeAll');
                 }
             });//bootstrapTable
         };

         //点击显示列表
         $(function(){
             $("#showcost_btn").click(function(){
                 inittable_showcost();
             });
         });


//下拦菜单击事件事件，得到选择的分类（ID\名称），并设置到 showbutton的 HTML、ATTR (value)中
     function clickselecttype(aherf){
         var typename = $(aherf).attr("typename");
         var typeid = $(aherf).attr("typeid");
         $("#showselectedtype").html($(aherf).attr("typename"));
         $("#showselectedtype").attr('value',typeid);
     }
     function clickselectyear(aherf){
         var year = $(aherf).attr("year");
         $("#showselectedyear").html(year);
         $("#showselectedyear").attr("value",year);
     }
     function clickselectmonth(aherf){
         var month = $(aherf).attr("month");
         $("#showselectedmonth").html(month);
         $("#showselectedmonth").attr("value",month);
     }
     function clickselectsubject(aherf){
         var subjectname = $(aherf).attr("subjectname");
         var subjectid = $(aherf).attr("subjectid");
         $("#showselectedsubject").html(subjectname);
         $("#showselectedsubject").attr('value',subjectid);
     }