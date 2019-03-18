var userName;
var roomName;

var ws = new WebSocket("ws://127.0.0.1:8888/chat");

$(window).onload = init();


function init() {
  //document.getElementById('idname').value;//获取input标签里的值，value; 
  //document.getElementById('idname').innerHTML;获取div里的html内容
  //换种写法取值.value = document.getElementById("**").value;              value = document.getElementsByName("**)[0].value; 
  userName = document.getElementById("parameter_user").innerHTML;
  roomName = document.getElementById("parameter_room").innerHTML;

  var messageContainer = document.getElementById("chatbox");
  var userListContainer = document.getElementById("userlist");
  if("WebSocket" in window) {
    openWS(messageContainer, userListContainer);
    reg();
  }
  else {
    messageContainer.appendChild(createChatEntry("SYSTEM", "WebSocket is NOT supported by your browser!"));
  }
}


// function getCookie(cname){    // 获取指定名称的cookie的值
//   var name = cname + "=";
//   var ca = document.cookie.split(';');
//   for(var i=0; i<ca.length; i++) 
//   {
//     var c = ca[i].trim();
//     if (c.indexOf(name)==0) return c.substring(name.length,c.length);
//   }
//   return "";
// }

//消息更新
function createChatEntry(userName, message) {
  var entry = document.createElement("div");
  entry.setAttribute("id","chat_list");
  
  if (userName == "SYSTEM") {
    var dom_uname = document.createElement("span");
    // dom_uname.setAttribute("class","chat_userName"); 
    // dom_uname.innerHTML = userName + ": ";
    entry.appendChild(dom_uname);
    var sys_msg = document.createElement("span");
    sys_msg.setAttribute("class","sys_message"); 
    sys_msg.innerHTML = userName + ": " + message;
    entry.appendChild(sys_msg);
  }
  else {
    var dom_uname = document.createElement("span");
    dom_uname.setAttribute("class","chat_userName"); 
    dom_uname.innerHTML = userName + ": ";
    entry.appendChild(dom_uname);
    
    var dom_msg = document.createElement("span");
    dom_msg.setAttribute("class","chat_message"); 
    dom_msg.innerHTML = message;
    entry.appendChild(dom_msg);
  }

  return entry;
}

//用户列表更新
function createUserlist(total, userlist){
  document.getElementById("userlist").innerHTML="";
  var entry = document.createElement("div");

  var dom_num = document.createElement("span");
  dom_num.setAttribute("class","chat_userName"); 
  dom_num.innerHTML = '当前房间人数(' + total +')';
  entry.appendChild(dom_num);

  var dom_ul = document.createElement("ul");
  for (var i = 0; i < userlist.length; i++){
    var dom_user = document.createElement("li");
    dom_user.innerHTML = userlist[i];
    dom_ul.appendChild(dom_user);
  }
  entry.appendChild(dom_ul);
  return entry
}

//让浏览器滚动条保持在最低部
function scrollToBottom(){
  // w.scrollTo(0, window.getElementById("chatbox").innerHeight);
  var obj = document.getElementById('chatbox');
  obj.scrollTop = obj.scrollHeight;
  //清除消息框
  document.getElementById("message").value="";
}

// key function
function openWS(messageContainer, userListContainer) {
  
  ws.onopen = function(e){    //连接成功后的回调函数
    alert("WebSocket successfully launched!")
  };
  ws.onmessage = function(e) {  //收到服务器数据之后的回调函数
    var data = JSON.parse(e.data);
    if (data.type == 'msg' || data.type == 'sys'){
      messageContainer.appendChild(createChatEntry(data.userName, data.message));
    }
    if (data.type == 'list'){
      userListContainer.appendChild(createUserlist(data.total, data.userlist));
    }
    scrollToBottom();
  };
  ws.onclose = function(e) {
    messageContainer.appendChild(createChatEntry("SYSTEM", "The connection is closed!"));
    window.setTimeout("logout();",5000);
  };
  ws.onerror = function(e) {
    console.log('Error occured: ' + e.data);
  }

}

//ws.send()用于向后端发送数据

//注册
function reg(){
  var data = { 
               type: "reg",
               userName: userName
               };
  sendMsg(JSON.stringify(data));
}

//解决Tornado WebSockets - InvalidStateError “Still in CONNECTING State”
function sendMsg(msg) {
        waitForSocketConnection(ws, function() {
            ws.send(msg);
        });
    };

function waitForSocketConnection(socket, callback){   //等待连接建立再开始发送
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

function sendMessage() {      //发送数据到后端处理
  var data = { 
               type: "msg",
               userName: userName,
               message: document.getElementById("message").value };
  
  if(data.message) {
    sendMsg(JSON.stringify(data));
  }
}
