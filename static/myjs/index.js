//主页显示信息
//首页显示图书列表
function inittable_showbook(){
      $("#showbooklist_table").bootstrapTable("destroy");

      $("#showbooklist_table").bootstrapTable({
                 url: '/homeshowbooklist/',  //请求后台的URL（*）
                 method: 'get',   //请求方式（*）
                 //toolbar: '#toolbar',  //工具按钮用哪个容器
                 striped: true,   //是否显示行间隔色
                 cache: false,   //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
                 pagination: true,   //是否显示分页（*）
                 sortable: false,   //是否启用排序
                 detailView: true,  //父子表
                 //sortOrder: "asc",   //排序方式
                 queryParams: function(params){
                     var pa = {limit: params.limit,offset:params.offset};
                     return pa;
                 },//每页长、页号
                 queryParamsType: "limit",
                 sidePagination: "server",  //分页方式：client客户端分页，server服务端分页（*）
                 pageNumber:1,   //初始化加载第一页，默认第一页
                 pageSize: 10,   //每页的记录行数（*）
                 pageList: [10,20, 30], //可供选择的每页的行数（*）
                 strictSearch: true,
                 clickToSelect: true,  //是否启用点击选中行
                 //height: 460,   //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度
                 uniqueId: "id",   //每一行的唯一标识，一般为主键列
                 cardView: false,   //是否显示详细视图
                 //silent:true,
          columns: [{field: 'ck', checkbox: true, visible: false
                    },{
                     field: 'id',
                     title: '序号',
                     visible: false
                 }, {
                     field: 'name',
                     title: '名称'
                 },{
                     field:'booktypes',
                     title:'类别'
                 },{
                     field: 'detial',
                     title: '描述'
                 }],
                 //注册加载子表的事件。注意下这里的三个参数！,row 为上面的一行数据
                onExpandRow: function (index, row, $detail) {
                    initbooksubtable(index, row, $detail);
                }
             });//bootstrapTable
         };
         //初始化子表格(无限循环)
    initbooksubtable = function(index, row, $detail) {
        var parentid = row.id;
        var cur_table = $detail.html('<table></table>').find('table');
        $(cur_table).bootstrapTable({
            url: '/homeshowchildbooklist/',
            method: 'get',
            queryParams:  function(params){
                var pa = {limit: params.limit,offset:params.offset,parentid:parentid};
                return pa;
            },
            clickToSelect: true,
            //detailView: true,//父子表
            queryParamsType: "limit",
            pagination: false,
            uniqueId: "id",
            pageSize: 20,
            pageList: [20,30,50],
            columns: [{
                checkbox: true
            }, {
                field: 'id',
                title: 'ID'
            }, {
                field: 'name',
                title: '名称'
            }],
            //无线循环取子表，直到子表里面没有记录
            onExpandRow: function (index, row, $Subdetail) {
                initbooksubtable(index, row, $Subdetail);
            }
        });
        return initbooksubtable;
    };

         //加载后显示列表
         $(function(){
             inittable_showbook();
         });


//显示软件列表
function inittable_showsoft(){
      $("#showsoftlist_table").bootstrapTable("destroy");

      $("#showsoftlist_table").bootstrapTable({
                 url: '/homeshowsoftlist/',  //请求后台的URL（*）
                 method: 'get',   //请求方式（*）
                 //toolbar: '#toolbar',  //工具按钮用哪个容器
                 striped: true,   //是否显示行间隔色
                 cache: false,   //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
                 pagination: true,   //是否显示分页（*）
                 sortable: false,   //是否启用排序
                  detailView: true,  //父子表
                 //sortOrder: "asc",   //排序方式
                 queryParams: function(params){
                     var pa = {limit: params.limit,offset:params.offset};
                     return pa;
                 },//每页长、页号
                 queryParamsType: "limit",
                 sidePagination: "server",  //分页方式：client客户端分页，server服务端分页（*）
                 pageNumber:1,   //初始化加载第一页，默认第一页
                 pageSize: 10,   //每页的记录行数（*）
                 pageList: [10,20, 30], //可供选择的每页的行数（*）
                 strictSearch: true,
                 clickToSelect: true,  //是否启用点击选中行
                 //height: 460,   //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度
                 uniqueId: "id",   //每一行的唯一标识，一般为主键列
                 cardView: false,   //是否显示详细视图
                 detailView: false,   //是否显示父子表
                 //silent:true,
                 columns: [{
                     field: 'id',
                     title: '序号'
                 }, {
                     field: 'name',
                     title: '名称'
                 },{
                     field:'softtypes',
                     title:'类别'
                 },{
                     field: 'detial',
                     title: '描述'
                 }],
                 rowStyle: function (row, index) {
                     //这里有5个取值代表5中颜色['active', 'success', 'info', 'warning', 'danger'];
                     var strclass = "";
                     /*
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
                     */

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
                     $('#showsoftlist_table').bootstrapTable('removeAll');
                 }
             });//bootstrapTable
         };

         //加载后显示列表
         $(function(){
              inittable_showsoft();
         });




//下面为原来代码，以上为本单元代码

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
     function clicksortstyle(aherf){ //排序
         //alert(111);
         var sortname = $(aherf).attr("sortname");
         var sortid = $(aherf).attr("sortfield");
         $("#showsortstyle").html(sortname);
         $("#showsortstyle").attr('value',sortid);
     }


