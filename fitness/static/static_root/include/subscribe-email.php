<?php

require_once('phpmailer/PHPMailerAutoload.php');

$toemails = array();

$toemails[] = array(
				'email' => 'username@website.com', // Your Email Address
				'name' => 'Your Name' // Your Name
			);

// Form Processing Messages
$message_success = 'We have <strong>successfully</strong> received your Message and will get Back to you as soon as possible.';

$mail = new PHPMailer();

// If you intend you use SMTP, add your SMTP Code after this Line


if( isset( $_POST['widget-subscribe-form-email'] ) ) {
	if( $_POST['widget-subscribe-form-email'] != '' ) {

		$email = $_POST['widget-subscribe-form-email'];

		$subject = 'Subscribe me to the List';

		$mail->SetFrom( $email , 'New Subscriber' );
		$mail->AddReplyTo( $email );
		foreach( $toemails as $toemail ) {
			$mail->AddAddress( $toemail['email'] , $toemail['name'] );
		}
		$mail->Subject = $subject;

		$email = isset($email) ? "Email: $email<br><br>" : '';

		$referrer = $_SERVER['HTTP_REFERER'] ? '<br><br><br>This Form was submitted from: ' . $_SERVER['HTTP_REFERER'] : '';

		$body = "$email $referrer";

		$mail->MsgHTML( $body );
		$sendEmail = $mail->Send();

		if( $sendEmail == true ):
			echo '{ "alert": "success", "message": "' . $message_success . '" }';
		else:
			echo '{ "alert": "error", "message": "Email <strong>could not</strong> be sent due to some Unexpected Error. Please Try Again later.<br /><br /><strong>Reason:</strong><br />' . $mail->ErrorInfo . '" }';
		endif;
	} else {
		echo '{ "alert": "error", "message": "Please <strong>Fill up</strong> all the Fields and Try Again." }';
	}
} else {
	echo '{ "alert": "error", "message": "An <strong>unexpected error</strong> occured. Please Try Again later." }';
}

?>