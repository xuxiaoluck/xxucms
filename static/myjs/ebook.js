//显示图书列表

//子表的下载按钮点击事件，下载该文件
window.operateEvents1 = {
	'click .RoleOfA': function(e, value, row, index) {
        window.location.href="/ebook/downloadfile?fileid=" + row.id;
			}
};

function operateFormatter(value, row, index) {
		return [
			'<button id="btn_detail" type="button" class="RoleOfA btn-sm btn-link">下载</button>',
		].join('');
};


function inittable_showbooktypelist(){
      $("#showbooktypelist_table").bootstrapTable("destroy");

      $("#showbooktypelist_table").bootstrapTable({
                 url: '/ebook/showbooktypelist/',  //请求后台的URL（*）
                 method: 'get',   //请求方式（*）
                 //toolbar: '#toolbar',  //工具按钮用哪个容器
                 striped: true,   //是否显示行间隔色
                 cache: false,   //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
                 pagination: false,   //是否显示分页（*）
                 sortable:false,   //是否启用排序
                 detailView: false,  //父子表
                 //sortOrder: "asc",   //排序方式
                 queryParams: function(params){
                     return {};
                 },//每页长、页号
                 //queryParamsType: "limit",
                 //sidePagination: "server",  //分页方式：client客户端分页，server服务端分页（*）
                 //pageNumber:1,   //初始化加载第一页，默认第一页
                 //pageSize: 10,   //每页的记录行数（*）
                 //pageList: [10,20, 30], //可供选择的每页的行数（*）
                 strictSearch: true,
                 clickToSelect: true,  //是否启用点击选中行
                 //height: 460,   //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度
                 uniqueId: "id",   //每一行的唯一标识，一般为主键列
                 cardView: false,   //是否显示详细视图
                 //silent:true,
          columns: [{
                     field: 'id',
                     title: '序号',
                     visible: false
                 }, {
                     field: 'name',
                     title: '图书类别'
                 },],
          rowStyle: function (row, index) {
              var style = {};
              if (index % 3 == 0)
                  style={css:{'color':'#775565'}};
              else if (index % 3 == 1)
                  style={css:{'color':'#118865'}};
              else
                  style={css:{'color':'#336665'}};
             return style;
          },
          //行点击事件，row 为行内容 row.id row.name....
          onClickRow: function (row) {
              //点击后加载该分类的图书列表
              if (islogin == 0) //未登录
                  inittable_showbooklist(row.name);
              else
                  inittable_showbooklist1(row.name);
            }
          });//.bootstrapTable
};

//页面加载后加载分类数据
$(function(){
    inittable_showbooktypelist();
});

//加载分类下的图书列表
function inittable_showbooklist(booktypename){
      $("#showbooklist_table").bootstrapTable("destroy");

      $("#showbooklist_table").bootstrapTable({
                 url: '/ebook/showbooklist/',  //请求后台的URL（*）
                 method: 'get',   //请求方式（*）
                 //toolbar: '#toolbar',  //工具按钮用哪个容器
                 striped: true,   //是否显示行间隔色
                 cache: false,   //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
                 pagination: true,   //是否显示分页（*）
                 sortable: false,   //是否启用排序
                 detailView: true,  //父子表
                 //sortOrder: "asc",   //排序方式
                 queryParams: function(params){
                     var pa = {limit: params.limit,offset:params.offset,typename:booktypename};
                     return pa;
                 },//每页长、页号
                 queryParamsType: "limit",
                 sidePagination: "server",  //分页方式：client客户端分页，server服务端分页（*）
                 pageNumber:1,   //初始化加载第一页，默认第一页
                 pageSize: 30,   //每页的记录行数（*）
                 pageList: [20, 30,50], //可供选择的每页的行数（*）
                 strictSearch: true,
                 clickToSelect: true,  //是否启用点击选中行
                 //height: 460,   //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度
                 uniqueId: "id",   //每一行的唯一标识，一般为主键列
                 cardView: false,   //是否显示详细视图
                 //silent:true,
          columns: [{
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
                    inittable_showbooksublist(index, row, $detail);
          },
          rowStyle: function (row, index) {
              var style = {};
              if (index % 5 == 0)
                  style={css:{'color':'#775565'}};
              else if (index % 5 == 1)
                  style={css:{'color':'#118865'}};
              else if (index % 5 == 2)
                  style={css:{'color':'#336665'}};
              else if (index % 5 == 3)
                  style={css:{'color':'#33a65'}};
              else
                  style={css:{'color':'#331165'}};
             return style;
          }
          });//bootstrapTableb
};

//带修改标签
window.operateEvents1_modi = {
	'click .RoleOfA': function(e, value, row, index) {
        window.location.href="/ebook/modifybook?bookid=" + row.id;
			}
};

function operateFormatter_modi(value, row, index) {
		return [
			'<button id="btn_detail" type="button" class="RoleOfA btn-sm btn-link">修改</button>',
		].join('');
};

function inittable_showbooklist1(booktypename){
      $("#showbooklist_table").bootstrapTable("destroy");

      $("#showbooklist_table").bootstrapTable({
                 url: '/ebook/showbooklist/',  //请求后台的URL（*）
                 method: 'get',   //请求方式（*）
                 //toolbar: '#toolbar',  //工具按钮用哪个容器
                 striped: true,   //是否显示行间隔色
                 cache: false,   //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
                 pagination: true,   //是否显示分页（*）
                 sortable: false,   //是否启用排序
                 detailView: true,  //父子表
                 //sortOrder: "asc",   //排序方式
                 queryParams: function(params){
                     var pa = {limit: params.limit,offset:params.offset,typename:booktypename};
                     return pa;
                 },//每页长、页号
                 queryParamsType: "limit",
                 sidePagination: "server",  //分页方式：client客户端分页，server服务端分页（*）
                 pageNumber:1,   //初始化加载第一页，默认第一页
                 pageSize: 30,   //每页的记录行数（*）
                 pageList: [20, 30,50], //可供选择的每页的行数（*）
                 strictSearch: true,
                 clickToSelect: true,  //是否启用点击选中行
                 //height: 460,   //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度
                 uniqueId: "id",   //每一行的唯一标识，一般为主键列
                 cardView: false,   //是否显示详细视图
                 //silent:true,
          columns: [{
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
                 },{
                     field:'operate',
                     title:'修改',
                     events: operateEvents1_modi,
			         formatter: operateFormatter_modi
                 }],
          //注册加载子表的事件。注意下这里的三个参数！,row 为上面的一行数据
          onExpandRow: function (index, row, $detail) {
                    inittable_showbooksublist(index, row, $detail);
          },
          rowStyle: function (row, index) {
              var style = {};
              if (index % 5 == 0)
                  style={css:{'color':'#775565'}};
              else if (index % 5 == 1)
                  style={css:{'color':'#118865'}};
              else if (index % 5 == 2)
                  style={css:{'color':'#336665'}};
              else if (index % 5 == 3)
                  style={css:{'color':'#33a65'}};
              else
                  style={css:{'color':'#331165'}};
             return style;
          }
          });//bootstrapTableb
};


//显示书籍下的实际书本（可以是多本）
function inittable_showbooksublist(index, row, $detail){
        var bookid = row.id;
        var cur_table = $detail.html('<table></table>').find('table');
        $(cur_table).bootstrapTable({
                 url: '/ebook/showbooksublist/',  //请求后台的URL（*）
                 method: 'get',   //请求方式（*）
                 //toolbar: '#toolbar',  //工具按钮用哪个容器
                 striped: true,   //是否显示行间隔色
                 cache: false,   //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
                 pagination:false,   //是否显示分页（*）
                 sortable: false,   //是否启用排序
                 detailView: false,  //父子表
                 //sortOrder: "asc",   //排序方式
                 queryParams: function(params){
                     var pa = {bookid:bookid};
                     return pa;
                 },
                 strictSearch: true,
                 clickToSelect: true,  //是否启用点击选中行
                 //height: 460,   //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度
                 uniqueId: "id",   //每一行的唯一标识，一般为主键列
                 cardView: false,   //是否显示详细视图
                 //silent:true,
          columns: [{
                     field: 'id',
                     title: '序号',
                     visible: false
                 }, {
                     field: 'name',
                     title: '名称'
                 },{
                     field: 'size',
                     title: '大小'
                 },{
                     field:'operate',
                     title:'下载',
                     events: operateEvents1,
			         formatter: operateFormatter
                 }],
          //注册加载子表的事件。注意下这里的三个参数！,row 为上面的一行数据
          onExpandRow: function (index, row, $detail) {
                    inittable_showbooksublist(index, row, $detail);
          },
          rowStyle: function (row, index) {
              var style = 'success';
              if (index % 2 == 0)
                  style='warning';
              return {classes:style};
          }
          });//bootstrapTable
};




