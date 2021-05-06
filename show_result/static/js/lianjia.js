function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined
}

var next_url = null;

function show_data() {
    $('.show-data').show();
    $('.configure').hide();
}
//
function show_configure() {
    $('.show-data').hide();
    $('.configure').show();
}

// t退出功能
function logout() {
    $.ajax({
        url: "/api/v1.0/user/session",
        type: "DELETE",
        contentType: "application/json",
        dataType: "json",
        headers: {
            "X-CSRFToken": getCookie("csrf_token")
        },
        success: function (resp) {
            // alert(resp.errmsg);
            location.reload();
        }
    })
}

function upload_data() {
    var ofiles = document.getElementById("exampleFormControlFile1").files;

    var params = new FormData();
    params.append('file', ofiles[0]);

    // 发送ajax请求
    $.ajax({
        url: "/api/v1.0/lianjia/save_data",
        type: "POST",
        data: params,
        cache: false,
        contentType: false,
        processData: false,
        headers: {
            "X-CSRFToken": getCookie("csrf_token")
        },
        success: function (resp) {
            if(resp.errno=2){
                //数据导入成功
                // 清除input标签中的file值
                $("#exampleFormControlFile1").val("");
                alert(resp.errmsg)
            }else {
                alert(resp.errmsg)
            }
        }
    })
}

function update_village(url){
    $.get(url, function (resp) {
        if(resp.errno==3) {
            // 数据获取成功
            var lianjia_village_lists = resp.data;
            $(".village_lists").empty();
            $.each(lianjia_village_lists, function (i, item) {
                $(".village_lists").append(
                    "<tr>\n" +
                    "                                <td>"+ item.village_id +"</td>\n" +
                    "                                <td>" + item.village_name + "</td>\n" +
                    "                                <td>" + item.village_sale_num + "</td>\n" +
                    "                                <td>" + item.village_building_type +"</td>\n" +
                    "                                <td>" + item.village_developer +"</td>\n" +
                    "                            </tr>"
                )
            })
        }else{
            //
            alert(resp.errmsg)
        }
    })
}

function chaxun_village() {
    var city_id = $('#chaxun_city').val();
    var year = $('#daochu_year').val();
    var month = $('#daochu_month').val();

    var url = "/api/v1.0/lianjia/lianjia_village?page=1&city_id=" + city_id + "&year=" + year + "&month=" + month;
    update_village(url);
}

function download_village_data(){
    var city_id = $('#daochu_city').val();
    var year = $('#daochu_year').val();
    var month = $('#daochu_month').val();

    var url = "/api/v1.0/lianjia/download_data?city_id="+city_id + "&year=" + year + "&month=" + month;

    window.location.href = url
}

$(function () {
    // 根据标签,改变做工具css高度属性值
    var height = $(document).height() - 50;
    $('.left-tools').css('height', height + "px");

    // 链家标签说明置于底部
    var lianjia_data_explain_height = $(document).height() - 260;
    $('.lianjia_data_explain').css('margin-top', lianjia_data_explain_height + "px");

    // 改变右工具框的大小
    var right_height = $(document).height() - 70;
    $('.right-tools').css('height', right_height + "px");

    // 数据显示表单的数据
    var data_height = $(document).height() - 230;
    $('.show-data-tabel').css('height', data_height + "px");

    //    检查用户的登陆状态
    $.get('/api/v1.0/user/session', function (resp) {
        if (resp.errno == "0") {
            if (next_url == null) {
                $("#name").html(resp.data.name);
            } else {
                window.location.href = next_url;
                next_url = null
            }
        } else {
            $("#username").hide();
            window.location.href = '/login.html'
        }
    });

    // 获取城市信息
    $.get('/api/v1.0/lianjia/lianjia_city', function (resp) {
        // 数据反回成功
        if(resp.errno==1){
            var city_lists = resp.city_data;

            $.each(city_lists, function (i, item) {
                $("#daochu_city, #chaxun_city").append(
                    "<option value='" + item.city_id + "'" + ">" + item.city_name + "</option>"
                )
            })
        }else {
            console.log(resp.errno)
        }
    });

    // 获取日期
    $.get('/api/v1.0/lianjia/lianjia_data', function (resp) {
        if(resp.errno=1){
            // 请求成功
            var year_lists = resp.year_lists;
            var month_lists = resp.month_lists;

            // 遍历
            $.each(year_lists, function (i, item) {
                $("#chaxun_year, #daochu_year").append(
                   "<option value='" + item + "'" + ">" + item + "</option>"
                )
            });

            $.each(month_lists, function (i, item) {
                $("#chaxun_month, #daochu_month").append(
                   "<option value='" + item + "'" + ">" + item + "</option>"
                )
            })
        }else{
            alert(resp.errmsg);
        }
    });

    // 获取小区信息
    update_village("/api/v1.0/lianjia/lianjia_village?page=1&city_id=1")
});