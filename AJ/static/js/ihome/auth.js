function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

// 身份认证
$(document).ready(function () {
    //  提交身份认证的数据
   $('#form-auth').submit(function(){
       var real_name = $('#real-name').val();
       var id_card = $('#id-card').val();
       $.ajax({
           url:'/user/auth/',
           type:'PATCH',
           data:{'real_name': real_name, 'id_card': id_card},
           dataType:'json',
            success:function(msg) {
                if(msg.code == '200'){
                    $('.btn-success').hide()
                }
            },
           error:function(msg){
             alert('请求失败')
           }
       });
       return false;
   });
// 当页面刷新启动方法
   $.get('/user/auths/', function (msg) {
        if(msg.code = '200'){
            // 判断是否已经认证
            if(msg.data.id_name){
                $('#real-name').val(msg.data.id_name);
                $('#id-card').val(msg.data.id_card);
                $('.btn-success').hide()
            }
        }
   });
});
