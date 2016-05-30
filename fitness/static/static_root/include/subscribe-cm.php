<?php

require_once 'campaign-monitor/csrest_subscribers.php';

$apiKey = ''; // Your MailChimp API Key
$listId = ''; // Your MailChimp List ID

if( isset( $_GET['list'] ) AND $_GET['list'] != '' ) {
	$listId = $_GET['list'];
}

$email = $_POST['widget-subscribe-form-email'];

if( isset( $email ) AND $email != '' ) {

	$auth = array('api_key' => $apiKey);

	$wrap = new CS_REST_Subscribers( $listId, $auth);

	$result = $wrap->add(array(
		'EmailAddress' => $email,
		'Resubscribe' => true
	));

	if($result->was_successful()) {
		echo '{ "alert": "success", "message": "You have been <strong>successfully</strong> subscribed to our Email List." }';
	} else {
		echo '{ "alert": "error", "message": "Failed with code ' . $result->http_status_code . "\n<br /><pre>";
		var_dump($result->response);
		echo '</pre>" }';
	}

}