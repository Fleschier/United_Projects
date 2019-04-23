
var ws;

$(window).onload = openWS();

$(document).ready(function(){

    var context = document.getElementById("canvas").getContext('2d');

    $("#submit").click(function(){
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
        //注: var imgData=context.getImageData(x,y,width,height); x:开始复制的左上角位置的 x 坐标。y:开始复制的左上角位置的 y 坐标。
        var myImageData = context.getImageData(0, 0, 28, 28);
        sendIMG(myImageData.data);
    })

    $("#clear").click(function(){
        context.clearRect(0,0,canvas.clientWidth,canvas.clientHeight);
    })
})

function openWS(){
    ws = new WebSocket("ws://127.0.0.1:8888/ws");
    //ws = new WebSocket("ws://10.40.45.137:8888/ws")

    ws.onopen = function(e){
        console.log("Websoeckt Connected!");
    }
    ws.onmessage = function(e){
        var data = JSON.parse(e.data);
        alert("识别结果为: "+data);
    }
    ws.onclose = function(e){
        console.log("Connection closed!")
    }
}


function sendIMG(img){
    var dat = {image:img.toString()}
    sendMsg(JSON.stringify(dat))
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