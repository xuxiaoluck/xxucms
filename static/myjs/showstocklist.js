//显示行业列表
function inittable_industry(){
      $("#showstocklist_table").bootstrapTable("destroy");

      $("#showstocklist_table").bootstrapTable({
                 url: '/stock/getindustryinfo/',  //请求后台的URL（*）
                 method: 'get',   //请求方式（*）
                 //toolbar: '#toolbar',  //工具按钮用哪个容器
                 striped: true,   //是否显示行间隔色
                 cache: false,   //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
                 pagination: true,   //是否显示分页（*）
                 sortable: false,   //是否启用排序
                 //sortOrder: "asc",   //排序方式
                 queryParams: function(params){
                     var pa = {limit: params.limit,offset:params.offset,sortfield:$("#sortindustry_select").val()};
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
                     field: 'code',
                     title: '代码'
                 }, {
                     field: 'name',
                     title: '名称'
                 }, {
                     field: 'i_name',
                     title: '行业'
                 }],
                 rowStyle: function (row, index) {
                     //这里有5个取值代表5中颜色['active', 'success', 'info', 'warning', 'danger'];
                     var strclass = "";
                     if (row.code.substring(0,1) == "3") {
                         strclass = 'danger';//还有一个active
                     }
                     else if (row.code.substring(0,3) == "002") {
                         strclass = 'warning';
                     }
                     else if (row.code.substring(0,3) == "000") {
                         strclass = 'info';
                     }
                     else if (row.code.substring(0,2) == "60") {
                         strclass = 'success';
                     }
                     else{
                         return {};
                     }
                     return {classes: strclass};
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
                     $('#showstocklist_table').bootstrapTable('removeAll');
                 }
             });//bootstrapTable
         };

         //显示行业列表
         $(function(){
             $("#industry_btn").click(function(){
                 //alert(111);
                 inittable_industry();
             });
         });


//显示地域列表
function inittable_area(){
      $("#showstocklist_table").bootstrapTable("destroy");

      $("#showstocklist_table").bootstrapTable({
                 url: '/stock/getareainfo/',  //请求后台的URL（*）
                 method: 'get',   //请求方式（*）
                 //toolbar: '#toolbar',  //工具按钮用哪个容器
                 striped: true,   //是否显示行间隔色
                 cache: false,   //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
                 pagination: true,   //是否显示分页（*）
                 sortable: false,   //是否启用排序
                 //sortOrder: "asc",   //排序方式
                 queryParams: function(params){
                     var pa = {limit: params.limit,offset:params.offset,sortfield:$("#sortarea_select").val()};
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
                     field: 'code',
                     title: '代码'
                 }, {
                     field: 'name',
                     title: '名称'
                 }, {
                     field: 'a_name',
                     title: '地域'
                 }],
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
                     $('#showstocklist_table').bootstrapTable('removeAll');
                 }
             });//bootstrapTable
         };

         $(function(){
             $("#area_btn").click(function(){
                 inittable_area();
             });
         });


//显示概念列表
function inittable_concept(){
      $("#showstocklist_table").bootstrapTable("destroy");

      $("#showstocklist_table").bootstrapTable({
                 url: '/stock/getconceptinfo/',  //请求后台的URL（*）
                 method: 'get',   //请求方式（*）
                 //toolbar: '#toolbar',  //工具按钮用哪个容器
                 striped: true,   //是否显示行间隔色
                 cache: false,   //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
                 pagination: true,   //是否显示分页（*）
                 sortable: false,   //是否启用排序
                 //sortOrder: "asc",   //排序方式
                 queryParams: function(params){
                     var pa = {limit: params.limit,offset:params.offset,sortfield:$("#sortconcept_select").val()};
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
                     field: 'code',
                     title: '代码'
                 }, {
                     field: 'name',
                     title: '名称'
                 }, {
                     field: 'c_name',
                     title: '概念'
                 }],
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
                     $('#showstocklist_table').bootstrapTable('removeAll');
                 }
             });//bootstrapTable
         };

         $(function(){
             $("#concept_btn").click(function(){
                 inittable_concept();
             });
         });


//显示中小板列表
function inittable_sme(){
      $("#showstocklist_table").bootstrapTable("destroy");

      $("#showstocklist_table").bootstrapTable({
                 url: '/stock/getsmeinfo/',  //请求后台的URL（*）
                 method: 'get',   //请求方式（*）
                 //toolbar: '#toolbar',  //工具按钮用哪个容器
                 striped: true,   //是否显示行间隔色
                 cache: false,   //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
                 pagination: true,   //是否显示分页（*）
                 sortable: false,   //是否启用排序
                 //sortOrder: "asc",   //排序方式
                 queryParams: function(params){
                     var pa = {limit: params.limit,offset:params.offset,sortfield:$("#sortsme_select").val()};
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
                     field: 'code',
                     title: '代码'
                 }, {
                     field: 'name',
                     title: '名称'
                 }],
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
                     $('#showstocklist_table').bootstrapTable('removeAll');
                 }
             });//bootstrapTable
         };

         $(function(){
             $("#sme_btn").click(function(){
                 inittable_sme();
             });
         });

//显示创业板列表
function inittable_gem(){
      $("#showstocklist_table").bootstrapTable("destroy");

      $("#showstocklist_table").bootstrapTable({
                 url: '/stock/getgeminfo/',  //请求后台的URL（*）
                 method: 'get',   //请求方式（*）
                 //toolbar: '#toolbar',  //工具按钮用哪个容器
                 striped: true,   //是否显示行间隔色
                 cache: false,   //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
                 pagination: true,   //是否显示分页（*）
                 sortable: false,   //是否启用排序
                 //sortOrder: "asc",   //排序方式
                 queryParams: function(params){
                     var pa = {limit: params.limit,offset:params.offset,sortfield:$("#sortgem_select").val()};
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
                     field: 'code',
                     title: '代码'
                 }, {
                     field: 'name',
                     title: '名称'
                 }],
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
                     $('#showstocklist_table').bootstrapTable('removeAll');
                 }
             });//bootstrapTable
         };

         $(function(){
             $("#gem_btn").click(function(){
                 inittable_gem();
             });
         });


//显示ST列表
function inittable_st(){
      $("#showstocklist_table").bootstrapTable("destroy");

      $("#showstocklist_table").bootstrapTable({
                 url: '/stock/getstinfo/',  //请求后台的URL（*）
                 method: 'get',   //请求方式（*）
                 //toolbar: '#toolbar',  //工具按钮用哪个容器
                 striped: true,   //是否显示行间隔色
                 cache: false,   //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
                 pagination: true,   //是否显示分页（*）
                 sortable: false,   //是否启用排序
                 //sortOrder: "asc",   //排序方式
                 queryParams: function(params){
                     var pa = {limit: params.limit,offset:params.offset,sortfield:$("#sortst_select").val()};
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
                     field: 'code',
                     title: '代码'
                 }, {
                     field: 'name',
                     title: '名称'
                 }],
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
                     $('#showstocklist_table').bootstrapTable('removeAll');
                 }
             });//bootstrapTable
         };

         $(function(){
             $("#st_btn").click(function(){
                 inittable_st();
             });
         });


//显示Sz50列表
function inittable_sz50(){
      $("#showstocklist_table").bootstrapTable("destroy");

      $("#showstocklist_table").bootstrapTable({
                 url: '/stock/getsz50info/',  //请求后台的URL（*）
                 method: 'get',   //请求方式（*）
                 //toolbar: '#toolbar',  //工具按钮用哪个容器
                 striped: true,   //是否显示行间隔色
                 cache: false,   //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
                 pagination: true,   //是否显示分页（*）
                 sortable: false,   //是否启用排序
                 //sortOrder: "asc",   //排序方式
                 queryParams: function(params){
                     var pa = {limit: params.limit,offset:params.offset,sortfield:$("#sortsz50_select").val()};
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
                     field: 'code',
                     title: '代码'
                 }, {
                     field: 'name',
                     title: '名称'
                 }],
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
                     $('#showstocklist_table').bootstrapTable('removeAll');
                 }
             });//bootstrapTable
         };

         $(function(){
             $("#sz50_btn").click(function(){
                 inittable_sz50();
             });
         });


//显示Sz50列表
function inittable_zz500(){
      $("#showstocklist_table").bootstrapTable("destroy");

      $("#showstocklist_table").bootstrapTable({
                 url: '/stock/getzz500info/',  //请求后台的URL（*）
                 method: 'get',   //请求方式（*）
                 //toolbar: '#toolbar',  //工具按钮用哪个容器
                 striped: true,   //是否显示行间隔色
                 cache: false,   //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
                 pagination: true,   //是否显示分页（*）
                 sortable: false,   //是否启用排序
                 //sortOrder: "asc",   //排序方式
                 queryParams: function(params){
                     var pa = {limit: params.limit,offset:params.offset,sortfield:$("#sortzz500_select").val()};
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
                     field: 'code',
                     title: '代码'
                 }, {
                     field: 'name',
                     title: '名称'
                 }],
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
                     $('#showstocklist_table').bootstrapTable('removeAll');
                 }
             });//bootstrapTable
         };

         $(function(){
             $("#zz500_btn").click(function(){
                 inittable_zz500();
             });
         });


//显示hs3000列表
function inittable_hs300(){
      $("#showstocklist_table").bootstrapTable("destroy");

      $("#showstocklist_table").bootstrapTable({
                 url: '/stock/geths300info/',  //请求后台的URL（*）
                 method: 'get',   //请求方式（*）
                 //toolbar: '#toolbar',  //工具按钮用哪个容器
                 striped: true,   //是否显示行间隔色
                 cache: false,   //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
                 pagination: true,   //是否显示分页（*）
                 sortable: false,   //是否启用排序
                 //sortOrder: "asc",   //排序方式
                 queryParams: function(params){
                     var pa = {limit: params.limit,offset:params.offset,sortfield:$("#sorths300_select").val()};
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
                     field: 'code',
                     title: '代码'
                 }, {
                     field: 'name',
                     title: '名称'
                 },{
                     field:'date',
                     title:'日期'
                 },{
                     field:'weight',
                     title:'权重'
                 }],
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
                     $('#showstocklist_table').bootstrapTable('removeAll');
                 }
             });//bootstrapTable
         };

         $(function(){
             $("#hs300_btn").click(function(){
                 inittable_hs300();
             });
         });



//显示暂停列表
function inittable_suspend(){
      $("#showstocklist_table").bootstrapTable("destroy");

      $("#showstocklist_table").bootstrapTable({
                 url: '/stock/getsuspendinfo/',  //请求后台的URL（*）
                 method: 'get',   //请求方式（*）
                 //toolbar: '#toolbar',  //工具按钮用哪个容器
                 striped: true,   //是否显示行间隔色
                 cache: false,   //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
                 pagination: true,   //是否显示分页（*）
                 sortable: false,   //是否启用排序
                 //sortOrder: "asc",   //排序方式
                 queryParams: function(params){
                     var pa = {limit: params.limit,offset:params.offset,sortfield:$("#sortsuspend_select").val()};
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
                     field: 'code',
                     title: '代码'
                 }, {
                     field: 'name',
                     title: '名称'
                 },{
                     field:'s_date',
                     title:'上市日期'
                 },{
                     field:'e_date',
                     title:'暂停日期'
                 }],
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
                     $('#showstocklist_table').bootstrapTable('removeAll');
                 }
             });//bootstrapTable
         };

         $(function(){
             $("#suspend_btn").click(function(){
                 inittable_suspend();
             });
         });


//显示终止上市列表
function inittable_terminate(){
      $("#showstocklist_table").bootstrapTable("destroy");

      $("#showstocklist_table").bootstrapTable({
                 url: '/stock/getterminateinfo/',  //请求后台的URL（*）
                 method: 'get',   //请求方式（*）
                 //toolbar: '#toolbar',  //工具按钮用哪个容器
                 striped: true,   //是否显示行间隔色
                 cache: false,   //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
                 pagination: true,   //是否显示分页（*）
                 sortable: false,   //是否启用排序
                 //sortOrder: "asc",   //排序方式
                 queryParams: function(params){
                     var pa = {limit: params.limit,offset:params.offset,sortfield:$("#sortterminate_select").val()};
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
                     field: 'code',
                     title: '代码'
                 }, {
                     field: 'name',
                     title: '名称'
                 },{
                     field:'s_date',
                     title:'上市日期'
                 },{
                     field:'e_date',
                     title:'中止日期'
                 }],
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
                     $('#showstocklist_table').bootstrapTable('removeAll');
                 }
             });//bootstrapTable
         };

         $(function(){
             $("#terminate_btn").click(function(){
                 inittable_terminate();
             });
         });
