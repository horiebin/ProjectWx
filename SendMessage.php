<?php
$text = '红包发放失败，由于您的用户状态异常，使用常用的活跃的微信号可避免这种情况，请联系淘宝客服索取红包。';
$openid = '9PalwD2NwcxyuXNQXBWsq8Hf4tk';
    $mysql_server_name='localhost'; //
 
$mysql_username='xiaob'; //
 
$mysql_password='skdfjkasdf'; //
 
$mysql_database='xiaob'; //

$conn=mysql_connect($mysql_server_name,$mysql_username,$mysql_password) or die("error connecting") ; //连接数据库
mysql_query("set names 'utf8'"); //UTF-8 国际标准编码.
mysql_select_db($mysql_database); //打开数据库
$sql = "select v from server_config where name_space='wx' and k='access_token'";
$result2 = mysql_query($sql,$conn);
$row =  mysql_fetch_row($result2);
$access_token = $row[0];
$url = "https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=$access_token";
$data_string = '{"touser":"'.$openid.'","msgtype":"text","text":{"content":"'.$text.'"}}';
 
$ch = curl_init();
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_POSTFIELDS, $data_string);
curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json; charset=utf-8','Content-Length: ' . strlen($data_string)));
ob_start();
curl_exec($ch);
$return_content = ob_get_contents();
ob_end_clean();

$return_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
 
return array($return_code, $return_content);
