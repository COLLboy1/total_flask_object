function getCookie(name){
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined
}

function user_login(){
    // 获取username, pwd
    var username = $("#username").val();
    var password = $("#password").val();

    req_dict = {
        "username": username,
        "password": password,
    };

    var req_json = JSON.stringify(req_dict);

    // 发起请求
    $.ajax({
        url: "/api/v1.0/user/login",
        type: "POST",
        data: req_json,
        contentType: "application/json",
        dataType: "json",
        headers: {
            "X-CSRFToken": getCookie("csrf_token")
        },
        success: function(resp) {
            // 登陆成功
            if (resp.errno == "3"){
                // alert(resp.errmsg)
                location.href = "/index.html"
            }else{
                alert(resp.errmsg)
            }
        }
    })
}
