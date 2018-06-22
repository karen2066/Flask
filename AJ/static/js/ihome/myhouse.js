function hrefBack() {
    history.go(-1);
}

$(document).ready(function(){
    $(".auth-warn").show();
});

// 用get请求加载
$.get('/user/auths/', function (msg){
    // 如果请求成功
    if(msg.code == '200'){
        // 如果能够拿到id_name，就说明已经实名认证了
        if(msg.data.id_name){
            // 就把要求实名认证的提示隐藏起来
            $('.auth-warn').hide()
            $('#houses-list').show()
        }else {
            $('.auth-warn').show()
            $('#houses-list').hide()
        }
    }
});

// 动态展示我的房源页面
$.get('/house/myhouses/', function(msg){
    if(msg.code == '200'){
        var house_html = ''
        for(var i=0;i<msg.houses.length; i++){
            house_li = ''
            house_li +='<li>'
            house_li +='<a href="/house/detail/?house_id=' + msg.houses[i].id +'">'
            house_li +='<div class="house-title">'
            house_li +='<h3>房屋ID:' + msg.houses[i].id + ' —— ' + msg.houses[i].title + '</h3>'
            house_li +='</div>'
            house_li +='<div class="house-content">'
            house_li +='<img src="/static/' + msg.houses[i].image + '" alt="">'
            house_li +='<div class="house-text">'
            house_li +='<ul>'
            house_li +='<li>位于：' + msg.houses[i].area + '</li>'
            house_li +='<li>价格：￥' + msg.houses[i].price + '/晚</li>'
            house_li +='<li>发布时间：' + msg.houses[i].create_time +'</li>'
            house_li +='</ul>'
            house_li +='</div>'
            house_li +='</div>'
            house_li +='</a>'
            house_li +='</li>'

            house_html += house_li
        }
        $('#houses-list').append(house_html)
    }
});