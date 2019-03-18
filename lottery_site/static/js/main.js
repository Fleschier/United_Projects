$(document).ready(function(){
  $("#button").click(function(){
    if(document.cookie){
      window.open("result.html")
    }
    else{
      alert("请先输入数据!")
    }
  })

  $("#button1").click(function(){
    window.open("input.html")
  })
})

