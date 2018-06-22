function hrefBack() {
    history.go(-1);
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}


$(document).ready(function(){
    var info = location.search
    house_id = info.split('=')[1]
    $.get('/house/detail/' + house_id + '/', function(msg){
        $('.house-title').text(msg.house_info.title)
        $('.landlord-name').text(msg.house_info.user_name)
        $('.text-center li').text(msg.house_info.address)
        $('.house_room').text('出租'+msg.house_info.room_count+'间')
        $('.house_acreage').text('房屋面积:'+msg.house_info.acreage+'平米')

        $('.book-house').attr('href', '/house/booking/?house_id=' + msg.house_info.id)

    });

    var mySwiper = new Swiper ('.swiper-container', {
        loop: true,
        autoplay: 2000,
        autoplayDisableOnInteraction: false,
        pagination: '.swiper-pagination',
        paginationType: 'fraction'
    })
    $(".book-house").show();
})

