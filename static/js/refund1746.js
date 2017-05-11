localIds = [0, 0, 0];
$(document).ready(function () {
    console.log('jquery ready')
    $(".ui-dialog").dialog("show");
    $("#rulesBtu").click(function () {
        $(".ui-dialog").dialog("show");
    });

    $('#orderInput').on("focus", function () {
            $('.model2').css("height", "200px");
            $('.model2').css("margin-top", "-20%");
            $('#ff').css("margin-top", "5%");
        }
    )

    $("#choseImgBtn").click(function () {
        var restPhoto = 0;
        for (var id in localIds) {
            if (localIds[id] == 0)
                restPhoto += 1;
        }
        console.log('rest photo number:' + restPhoto);
        wx.chooseImage({
            count: restPhoto, // 最大3
            sizeType: ['original', 'compressed'], // 可以指定是原图还是压缩图，默认二者都有
            sourceType: ['album', 'camera'], // 可以指定来源是相册还是相机，默认二者都有
            success: function (res) {
                var nowSelectedIds = res.localIds; // 返回选定照片的本地ID列表，localId可以作为img标签的src属性显示图片
                var tempId = 0;
                for (var i = 0; i < 3; i++) {
                    if (localIds[i] == 0) {
                        localIds[i] = nowSelectedIds[tempId];
                        $("#img" + i).attr('src', nowSelectedIds[tempId]);
                        $("#img" + i).parent().removeAttr('hidden');
                        tempId += 1;
                    }
                    if (tempId == nowSelectedIds.length) {
                        break;
                    }
                }

            }
        });

    });

    $(".close").click(function () {
        var v = $(this).attr('v');
        console.log('choose ' + v);
        $("#img" + v).parent().attr('hidden', 'hidden');
        localIds[v] = 0;
    });

    $('#submit').click(function () {
        $(this).addClass('active');
        var serverIdList = Array();

        var orderId = $("#orderInput").attr('value');

        uploadImage(0,serverIdList);
    });


});

wx.ready(function () {
    // config信息验证后会执行ready方法，所有接口调用都必须在config接口获得结果之后，config是一个客户端的异步操作，所以如果需要在页面加载时就调用相关接口，则须把相关接口放在ready函数中调用来确保正确执行。对于用户触发时才调用的接口，则可以直接调用，不需要放在ready函数中。
    console.log('wx success verify')
});
wx.error(function (res) {
    // config信息验证失败会执行error函数，如签名过期导致验证失败，具体错误信息可以打开config的debug模式查看，也可以在返回的res参数中查看，对于SPA可以在这里更新签名。
    console.log('wx verify error:' + res.errMsg)
});

// wx.checkJsApi({
//     jsApiList: ['chooseImage'], // 需要检测的JS接口列表，所有JS接口列表见附录2,
//     success: function(res) {
//         // 以键值对的形式返回，可用的api值true，不可用为false
//         // 如：{"checkResult":{"chooseImage":true},"errMsg":"checkJsApi:ok"}
//     }
// });
function uploadImage(currentId,serverIdList) {

    if(currentId == 3){
        postRequest(serverIdList);
        return;
    }
    if (localIds[currentId] != 0) {
        wx.uploadImage({
            localId: localIds[currentId], // 需要上传的图片的本地ID，由chooseImage接口获得
            isShowProgressTips: 1, // 默认为1，显示进度提示
            success: function (res) {
                var serverId = res.serverId; // 返回图片的服务器端ID
                serverIdList.push(serverId);
                //上传完再传下一张
                uploadImage(currentId + 1,serverIdList);
            }
        });
    }else{
        uploadImage(currentId + 1,serverIdList);
    }
}
function postRequest(serverIdList) {
    var orderId = $("#orderInput").attr('value');
    var openId = $("#orderInput").attr('openId');
    var shopId = $("#orderInput").attr('shopId');

    console.log('orderId: ' + orderId);
    $.ajax({
        type: "POST",
        url: "/refund/submit",
        data: {info:JSON.stringify({shop_id:shopId, open_id:openId,order_id: orderId, server_ids: serverIdList})},
        success: function (data) {
            if(data == 'true'){
                alert('上传成功!');
                $('.close').trigger("click");
                $('#orderInput').val('') ;
            }else if(data == 'wrong'){
                alert('订单号不存在！');
            }else{
                alert('请勿重复上传单号');
            }
            $('#submit').removeClass('active');

        }
    });

}


