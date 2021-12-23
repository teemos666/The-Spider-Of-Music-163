$(function(){
    $("#start").click(function() {
        var para={
            song:$("#song").val()
        }
		var res = $("#res");

        $.ajax({
            url:"http://192.168.160.137:5000/search",
            type:"Post",
            data:para,
            datatype:"html",
            success:function(data){
                // eval(data);
            }
        });
		res.attr("src", "m_song/search_res.html");
		swiper.slideTo(1, 600, false);
    });
});



layui.use(['table', 'layer', 'form', 'laypage'], function () {
	var table = layui.table;
	var form = layui.form;
	table.render({
		elem: '#goods_table'
		, id: 'goodsReload'
		, even: true //开启隔行背景
		, width: 1060
		, request: {
			pageName: 'pageNum',
			limitName: 'pageSize'
		}
		, title:
			'汇总表'
		, limit: 10
		, limits: [1, 5, 10, 20, 50, 100]
		, url: 'http://192.168.160.137:5000/search_result'
		, cols: [
			[
				{field: 'id', width: 150, title: 'ID', align: 'center'}
				, {field: 'name', width: 350, title: '歌名', align: 'center'}
				, {field: 'author', width: 150, title: '作者', align: 'center'}
				, {field: 'source', width: 250, title: '歌单来源', align: 'center'}
				, {
				// fixed: 'right',
				title: '操作',
				toolbar: '#goods_lineBar',
				width: 150,
				align: 'center'
			}
			]
		]
		, page: true
	});

	
	
	 //查看评论，搜索评论并切换下一页
	  table.on('tool(goods_bar)', function(obj){
	    var data = obj.data;
	    if(obj.event === 'detail'){
	      layer.msg('ID：'+ data.id + ' 的查看操作');
		  
		  var para={
		      id:data.id
		  }
		  $.ajax({
		      url:"http://192.168.160.137:5000/comments",
		      type:"Post",
		      data:para,
		      datatype:"html",
		      success:function(data){
		          // eval(data);
		      }
		  });
		  
		  var com = $("#com",parent.document);
		  com.attr("src", "m_song/comments.html");
		  window.top.swiper.slideTo(2, 600, false);
		  
	    }
	  });
});
