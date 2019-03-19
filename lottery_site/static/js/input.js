$(document).ready(function(){
    $("#input").click(function(){
        var first = $("#first").val();      //通过id获取value的值
        var second = $("#second").val();
        var third = $("#third").val();
        var names = $("#names").val();

        //将数据做成json以便传给后端
        var values = {"first1":first,
                    "second1":second,
                    "third1":third,
                    "names1":names 
                    };

        $.ajax({
            type:"post",
            url:"/input",
            data:values,
            cache:false,
            success:function(data){
                alert(data);
                history.back(-1);
            },
            error:function(){
                alert("error!");
            },
        });
    });
});