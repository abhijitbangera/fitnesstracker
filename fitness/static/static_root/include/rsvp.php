<?php

require_once('phpmailer/PHPMailerAutoload.php');

$toemails = array();

$toemails[] = array(
				'email' => 'username@website.com', // Your Email Address
				'name' => 'Your Name' // Your Name
			);

// Form Processing Messages
$message_success = 'Thank you for Confirming your RSVP.';

// Add this only if you use reCaptcha with your Contact Forms
$recaptcha_secret = 'your-recaptcha-secret-key'; // Your reCaptcha Secret

$mail = new PHPMailer();

// If you intend you use SMTP, add your SMTP Code after this Line


if( $_SERVER['REQUEST_METHOD'] == 'POST' ) {
	if( $_POST['wedding-rsvp-name'] != '' AND $_POST['wedding-rsvp-email'] != '' ) {

		$name = $_POST['wedding-rsvp-name'];
		$email = $_POST['wedding-rsvp-email'];
		$guests = $_POST['wedding-rsvp-guests'];
		$events = $_POST['wedding-rsvp-events'];

		$subject = 'Wedding RSVP Confirmation';

		$botcheck = $_POST['wedding-rsvp-botcheck'];

		if( $botcheck == '' ) {

			$mail->SetFrom( $email , $name );
			$mail->AddReplyTo( $email , $name );
			foreach( $toemails as $toemail ) {
				$mail->AddAddress( $toemail['email'] , $toemail['name'] );
			}
			$mail->Subject = $subject;

			$name = isset($name) ? "Name: $name<br><br>" : '';
			$email = isset($email) ? "Email: $email<br><br>" : '';
			$guests = isset($guests) ? "Guests: $guests<br><br>" : '';
			$events = isset($events) ? "Event: $events<br><br>" : '';

			$referrer = $_SERVER['HTTP_REFERER'] ? '<br><br><br>This Form was submitted from: ' . $_SERVER['HTTP_REFERER'] : '';

			$body = "$name $email $guests $events $referrer";

			// Runs only when reCaptcha is present in the Contact Form
			if( isset( $_POST['g-recaptcha-response'] ) ) {
				$recaptcha_response = $_POST['g-recaptcha-response'];
				$response = file_get_contents( "https://www.google.com/recaptcha/api/siteverify?secret=" . $recaptcha_secret . "&response=" . $recaptcha_response );

				$g_response = json_decode( $response );

				if ( $g_response->success !== true ) {
					echo '{ "alert": "error", "message": "Captcha not Validated! Please Try Again." }';
					die;
				}
			}

			$mail->MsgHTML( $body );
			$sendEmail = $mail->Send();

			if( $sendEmail == true ):
				echo '{ "alert": "success", "message": "' . $message_success . '" }';
			else:
				echo '{ "alert": "error", "message": "Sorry couldn\'t confirm your RSVP. Please Try Again later.<br /><br /><strong>Reason:</strong><br />' . $mail->ErrorInfo . '" }';
			endif;
		} else {
			echo '{ "alert": "error", "message": "Bot <strong>Detected</strong>.! Clean yourself Botster.!" }';
		}
	} else {
		echo '{ "alert": "error", "message": "Please <strong>Fill up</strong> all the Fields and Try Again." }';
	}
} else {
	echo '{ "alert": "error", "message": "An <strong>unexpected error</strong> occured. Please Try Again later." }';
}

?>