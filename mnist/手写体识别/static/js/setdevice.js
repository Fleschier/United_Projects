var script = document.createElement ("script");
script.type = "text/javascript";
var ismobile = isMobile();
alert(ismobile);
if (ismobile){
    script.src = "/static/js/canvas_mobile.js";
    document.getElementsByTagName("head")[0].appendChild(script);
} else{
    script.src = "/static/js/canvas_pc.js";
    document.getElementsByTagName("head")[0].appendChild(script);
}
function isMobile() {
    var userAgentInfo = navigator.userAgent;
    var Agents = ["Android", "iPhone",
                "SymbianOS", "Windows Phone",
                "iPad", "iPod"];
    var flag = false;
    for (var v = 0; v < Agents.length; v++) {
        if (userAgentInfo.indexOf(Agents[v]) > 0) {
            flag = true;
            break;
        }
    }
    return flag;
}