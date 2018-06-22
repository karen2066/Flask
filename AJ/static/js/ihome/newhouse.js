function hrefBack() {
    history.go(-1);
};

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    // $('.popup_con').fadeIn('fast');
    // $('.popup_con').fadeOut('fast');
});

// 将接口中获取到的数据库中的区域和设备动态添加到页面中
$.get('/house/area_facility/', function (msg) {
// 如果请求是成功的
    if(msg.code == '200'){
        // 区域和设备列表
        var area_str = '';
        var facility_str = '';
        // 在后端接收到的areas循环添加html标签，加到区域列表中
        for(var i=0; i<msg.areas.length; i++){
          area_option = '<option value=' + msg.areas[i].id + '>' + msg.areas[i].name + '</option>'
          area_str += area_option
        }
        // 拿到页面标签添加html属性
        $('#area-id').html(area_str)
        }
        // 在后端接收到的facilitys循环添加html标签，加到设备列表中
        for(var j=0; j<msg.facilitys.length; j++){
            facility_li = '<li><div class="checkbox"><label>';
            facility_li += '<input type="checkbox" name="facility" value="'+ msg.facilitys[j].id +'">' + msg.facilitys[j].name;
            facility_li += '</label></div></li>';
            facility_str += facility_li
        }
        // 拿到页面标签添加html属性
        $('.house-facility-list').html(facility_str)

});


// 发布新房源
$(document).ready(function(){
    $('#form-house-info').submit(function (){
        $.post('/house/newhouse/', $(this).serialize(), function (msg) {
            if(msg.code == '200'){
                $('#form-house-info').hide();
                $('#form-house-image').show();
                $('#house-id').val(msg.house_id)
            }
        });
        return false;
    });

    // 上传图片
    $('#form-house-image').submit(function(){

        $(this).ajaxSubmit({
            url:'/house/house_images/',
            type:'POST',
            dataType:'json',
            success:function(msg){
                if(msg.code == '200'){
                    var img_html = '<img src="/static/' + msg.image_url + '">'
                    $('.house-image-cons').append(img_html)
                }
            },
            error:function(msg){
                alert('请求失败')
            }
        });
        return false
    });

});



