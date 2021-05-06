
// 设置全局的登陆状态参数，如果登陆为1，未登陆为0
var login_status = 0;
var next_url = null;

function getCookie(name){
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined
}

function my_blog() {
    if (login_status == 1){
        window.location.href = "http://182.92.235.234/"
    }else {
        next_url = 'http://182.92.235.234/';
        window.location.href = "/login.html"
    }
}

function logout(){
    $.ajax({
        url: "/api/v1.0/user/session",
        type: "DELETE",
        contentType: "application/json",
        dataType: "json",
        headers: {
            "X-CSRFToken": getCookie("csrf_token")
        },
        success: function(resp) {
            // alert(resp.errmsg);
            location.reload();
        }
    })
}

$(function () {
//    检查用户的登陆状态
    $.get('/api/v1.0/user/session', function (resp) {
        if(resp.errno == "0"){
            if(next_url == null){
                login_status = 1;
                $("#login").hide();
                $("#name").html(resp.data.name);
            }else{
                window.location.href(next_url);
                next_url = null
            }
        }else {
            $("#username").hide();
        }
    })
});