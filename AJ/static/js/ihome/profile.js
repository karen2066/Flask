function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){});
        },1000)
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}


$(document).ready(function () {
    // 将图片保存到数据库
    $('#form-avatar').submit(function () {
       //  提交表单
        $(this).ajaxSubmit({
            url: '/user/profile/',
            type: 'PATCH',
            dataType: 'json',
            success: function (msg) {
                $('#user-avatar').attr('src','/static/' +msg.image_url)
            },
            error: function (msg) {
                alert('修改失败')
            }
        });
        return false;
    });


// 修改名字
//     向后端提交
    $('#form-name').submit(function(){
        var name = $('#user-name').val();
        $.ajax({
            url:'/user/proname/',
            type:'PATCH',
            dataType:'json',
            data:{'name':name},
            success:function(msg){
                if(msg.code == '1008'){
                    $('.error-msg').html('<i class="fa fa-exclamation-circle"></i>' + msg.msg)
                    $('.error-msg').show()
                }
            },
            error:function(msg){
                alert('上传失败')
            }
        });
        return false;
    });
});


// 删除提示
 function delete_msg(){
    $('.error-msg').hide()
 }
