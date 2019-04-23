var canvas=document.getElementById('canvas');
var context=canvas.getContext('2d');


var using=false;
var lastPoint={
    x:undefined,
    y:undefined
}

/*画板逻辑 */

autoSetSize(canvas);

listenToUser(canvas);

//记录是否在画
var eraserEnabled=false;

//drawLine
function drawLine(x1,y1,x2,y2){
    context.beginPath();
    context.moveTo(x1,y1);
    context.lineTo(x2,y2);
    // 线宽设置，必须放在绘制之前
    context.lineWidth = 18;
    context.stroke();
    context.closePath();  
  }

//drawCir
function drawCir(x,y){
context.beginPath()
context.arc(x,y,8,0,Math.PI*2);
context.fill();
}

//重置canvas画板宽高
function setCanvasSize(){
    var pageWidth=document.documentElement.clientWidth;
    var pageHeight=document.documentElement.clientHeight;
   
    if(pageWidth >= 500){
        canvas.width = 500;
    }
    else{
        canvas.width = pageWidth;
    }
    if(pageHeight >= 500){
        canvas.height = 500;
    }
    else{
        canvas.height = pageHeight;
    }

 }

//自动设置canvas画板宽高
function autoSetSize(){
    setCanvasSize();    
    window.onresize =function(){
        setCanvasSize();
    }    
}
function preventBehavior(e) {
    e.preventDefault()
}
    
document.addEventListener("touchmove", preventBehavior, false)
    

function listenToUser(){
    //特性检测
    if(document.body.ontouchstart!== undefined ){                    
        //是触屏设备
        canvas.ontouchstart =function(aaa){
            var x=aaa.touches[0].clientX;
            var y=aaa.touches[0].clientY;
            using=true;
            lastPoint={x:x,y:y};
            if(eraserEnabled){
                context.clearRect(x-10,y-10,20,20);
            }else{
                drawCir(x,y);
            }
        }
        //
        canvas.ontouchmove = function(aaa){
            var x=aaa.touches[0].clientX;
            var y=aaa.touches[0].clientY;
            var newPoint={x:x,y:y}
            if(using){
                if(eraserEnabled){
                    context.clearRect(x-10,y-10,20,20);
              }else{
                    drawCir(x,y);
                    drawLine(lastPoint.x,lastPoint.y,newPoint.x,newPoint.y)
                    lastPoint=newPoint;      
                }
            }
        }
        canvas.ontouchend = function(aaa){
            using=false;
        }

    }else{
        //不是触屏设备
        canvas.onmousedown=function(aaa){
            var x=aaa.clientX;
            var y=aaa.clientY;
            using=true;
            lastPoint={x:x,y:y};
            if(eraserEnabled){
                context.clearRect(x-10,y-10,20,20);
            }else{
                drawCir(x,y);
            }
        }
        
        //鼠标移动监听
        canvas.onmousemove=function(aaa){
            var x=aaa.clientX;
            var y=aaa.clientY;
            var newPoint={x:x,y:y}
            if(using){
                if(eraserEnabled){
                    context.clearRect(x-10,y-10,20,20);
              }else{
                    drawCir(x,y);
                    drawLine(lastPoint.x,lastPoint.y,newPoint.x,newPoint.y)
                    lastPoint=newPoint;      
                }
            }
        }       
        //鼠标松开监听
        canvas.onmouseup=function(aaa){
            using=false;
        }
    }
}


