var canvas = document.getElementById('canvas');
var evaluate = document.getElementById("evaluate");
var clear = document.getElementById("clear");
//global variable
var ctx;
var ws;
createWs();
if (canvas.getContext){
    ctx = canvas.getContext('2d');
    ctx.lineWidth = 15
    var mouseIsDown = false;
    canvas.onmousedown = function(e){
        var e = e || event;
        if (e.button == 0){
            ctx.beginPath();
            // 设置鼠标位置
            ctx.moveTo(e.clientX-canvas.offsetLeft,e.clientY-canvas.offsetTop);
            mouseIsDown = true;
        }
    }
    canvas.onmouseup = function(e){
        // if(mouseIsDown) mouseClick(e);
        if (mouseIsDown){
            ctx.closePath();
            mouseIsDown = false;
            return
        }
        // if (e.button == 2){
        //     ctx.clearRect(0,0,canvas.clientWidth,canvas.clientHeight)
        // }
    }
    //bug: 鼠标拖动到canvas之外
    canvas.onmousemove = function(e){
        if(!mouseIsDown) return;
        var e = e || event;
        // ctx.lineTo(e.clientX - canvas.offsetLeft,e.clientY - canvas.offsetTop);
        //此处写的有问题
        ctx.quadraticCurveTo(e.clientX - canvas.offsetLeft,e.clientY - canvas.offsetTop, e.clientX - canvas.offsetLeft,e.clientY - canvas.offsetTop)
        ctx.stroke();    
    }
  } else {
    // canvas-unsupported code here
    alert("您的浏览器不支持canvas!");
  }
clear.onclick=function(){
    ctx.clearRect(0,0,canvas.clientWidth,canvas.clientHeight);
}
//该函数会重复调用
evaluate.onclick=function(){
    var tmp_canvas = document.createElement("canvas");
    tmp_canvas.width = "28";
    tmp_canvas.height = "28";
    document.body.appendChild(tmp_canvas);
    var context = tmp_canvas.getContext('2d');
    // 原canvas左上角坐标
    var sourceX =  0;
    var sourceY =  0;
    //原canvas宽度与高度
    var sourceWidth = canvas.width;
    var sourceHeight = canvas.height;
    //新的canvas
    var destWidth = 28;
    var destHeight = 28;
    var destX = 0;
    var destY = 0;
    //缩放
    context.drawImage(canvas, sourceX, sourceY, sourceWidth, sourceHeight, destX, destY, destWidth, destHeight);
    // 一维，r/g/b/a
    var myImageData = context.getImageData(0, 0, 28, 28);
    sendImage(myImageData.data);
}
function createWs(){
    ws = new WebSocket("ws://127.0.0.1:8000/manager");
    // ws = new WebSocket("ws://10.70.41.12:8000/manager");
    if("WebSocket" in window) {
        openWS();
        reg("");
    }
    else {
        alert("WebSocket暂不支持您的浏览器!");
    }
}
function openWS() {
    //尚不清楚何时调用的onopen函数
    ws.onopen = function(e){    //连接成功后的回调函数
        alert("WebSocket successfully launched!");
    };
    ws.onmessage = function(e) {  //处理服务器传送过来的数据
        var data = JSON.parse(e.data);
        alert(data);
    };
    ws.onclose = function(e) {    //连接关闭的回调函数
        alert("The connection is closed!");
    };
    ws.onerror = function(e) {    //error
        console.log('Error occured: ' + e.data);
    }
}
function reg(){
  // js中传输字符串调用JSON.stringify方法
  var data = { 
               type: "reg",
               };
  sendMsg(JSON.stringify(data));
}
function sendImage(imagedata){
  // js中传输字符串调用JSON.stringify方法
//   alert(imagedata.toString());
  var data = { 
               type: "data",
               imagedata: imagedata.toString(),
               };
  sendMsg(JSON.stringify(data));
}

//解决Tornado WebSockets - InvalidStateError “Still in CONNECTING State”
function sendMsg(msg) {
        waitForSocketConnection(ws, function() {
            ws.send(msg);
        });
    };
function waitForSocketConnection(socket, callback){
        setTimeout(
            function(){
                if (socket.readyState === 1) {
                    if(callback !== undefined){
                        callback();
                    }
                    return;
                } else {
                    waitForSocketConnection(socket,callback);
                }
            }, 50);
};
