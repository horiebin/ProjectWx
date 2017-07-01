<?php
require 'wxpay.class.php';//数组参数
$mysql_server_name='localhost'; //
 
$mysql_username='xiaob'; //
 
$mysql_password='skdfjkasdf'; //
 
$mysql_database='xiaob'; //

$conn=mysqli_connect($mysql_server_name,$mysql_username,$mysql_password,$mysql_database) or die("error connecting") ; //连接数据库
$conn->query("set names 'utf8'"); //UTF-8 国际标准编码.
$stopFlag = false;
$lastRow = 0;
while(! $stopFlag){
    $config = array();
    $sql = "select * from server_config where name_space='wx'";
    $result2 = $conn->query($sql);
    while($row =  $result2->fetch_assoc())
    {
        $config[$row['k']] = $row['v'];   
    }

    $sql = 'select * from verify_refund where refund_flag=0 and del_flag=0 order by id asc limit 100';
    $result = $conn->query($sql);
    $stopFlag = true;
    while($row = $result->fetch_assoc())
    {
	$stopFlag = false;
	if ($row['id'] <= $lastRow){
	    $stopFlag = true;
	    break;
	}
        $sql = 'select * from shop_setting where shop_id='.$row['shop_id'];
        $result2 = $conn->query($sql);
        $ss = $result2->fetch_all(MYSQLI_ASSOC)[0];
        $shop_name = $ss['name'];
        $order_id = $row['order_id'];
        $open_id = $row['open_id'];
        $money = $row['money'];
        $sender = $shop_name;

	$obj2 = array();
	$obj2['wxappid'] = $config['app_id']; //appid
	$obj2['mch_id'] = $config['pay_id'];//商户id
	$obj2['mch_billno'] = $order_id;
	$obj2['client_ip'] = '120.25.195.197';
	$obj2['re_openid'] = $open_id;//接收红包openid
	$obj2['total_amount'] = $money;
	$obj2['total_num'] = 1;
	$obj2['send_name'] = $shop_name;
	$obj2['wishing'] = "感谢您的好评";
	$obj2['act_name'] = $shop_name."的好评返现";
	$obj2['remark'] = $shop_name."红包";
 
	$url = "https://api.mch.weixin.qq.com/mmpaymkttransfers/sendredpack";
	$wxpay = new wxPay();
	$res = $wxpay->pay($url, $obj2,$config['pay_key']);
	if ($res == 'SUCCESS'){
	    $sql = 'update verify_refund set refund_flag=1 where id='.$row['id'] ;
	    $conn->query($sql);
	}else if ($res == 'USER_ERROR'){
	    $sql = 'update verify_refund set del_flag=1 where id='.$row['id'] ;
	    $conn->query($sql);
	}
	$lastRow = $row['id'];
	
    }
}
