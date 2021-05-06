function getCookie(name){
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined
}

$(function () {
//    检查用户的登陆状态
    $.get('/api/v1.0/user/session', function (resp) {
        if(resp.errno == "0"){
            console.log("登陆成功")
        }else {
            window.location.href = '/login.html?next_url=/resume.html'
        }
    })

});