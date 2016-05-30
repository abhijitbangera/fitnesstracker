<?php

$apiKey = ''; // Your MailChimp API Key
$listId = ''; // Your MailChimp List ID

if( isset( $_GET['list'] ) AND $_GET['list'] != '' ) {
	$listId = $_GET['list'];
}

$email = $_POST['widget-subscribe-form-email'];
$fname = isset( $_POST['widget-subscribe-form-fname'] ) ? $_POST['widget-subscribe-form-fname'] : '';
$lname = isset( $_POST['widget-subscribe-form-lname'] ) ? $_POST['widget-subscribe-form-lname'] : '';
$datacenter = explode( '-', $apiKey );
$submit_url = "https://" . $datacenter[1] . ".api.mailchimp.com/3.0/lists/" . $listId . "/members/" ;

if( isset( $email ) AND $email != '' ) {

	$merge_vars = array();
	if( $fname != '' ) { $merge_vars['FNAME'] = $fname; }
	if( $lname != '' ) { $merge_vars['LNAME'] = $lname; }

	$data = array(
		'email_address' => $email,
		'status' => 'subscribed'
	);

	if( !empty( $merge_vars ) ) { $data['merge_fields'] = $merge_vars; }

	$payload = json_encode($data);

	$auth = base64_encode( 'user:' . $apiKey );

	$header   = array();
	$header[] = 'Content-type: application/json; charset=utf-8';
	$header[] = 'Authorization: Basic ' . $auth;

	$ch = curl_init();
	curl_setopt($ch, CURLOPT_URL, $submit_url);
	curl_setopt($ch, CURLOPT_HTTPHEADER, $header);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
	curl_setopt($ch, CURLOPT_TIMEOUT, 10);
	curl_setopt($ch, CURLOPT_POST, true);
	curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
	curl_setopt($ch, CURLOPT_POSTFIELDS, $payload);

	$result = curl_exec($ch);
	curl_close($ch);
	$data = json_decode($result);

	if ( isset( $data->status ) AND $data->status == 'subscribed' ){
		echo '{ "alert": "success", "message": "You have been <strong>successfully</strong> subscribed to our Email List." }';
	} else {
		echo '{ "alert": "error", "message": "' . $data->title . '" }';
	}

}

?>