<?php

require_once('phpmailer/PHPMailerAutoload.php');

$toemails = array();

$toemails[] = array(
				'email' => 'username@website.com', // Your Email Address
				'name' => 'Your Name' // Your Name
			);

// Form Processing Messages
$message_success = 'We have <strong>successfully</strong> received your Application and will get Back to you as soon as possible.';

// Add this only if you use reCaptcha with your Contact Forms
$recaptcha_secret = 'your-recaptcha-secret-key'; // Your reCaptcha Secret

$mail = new PHPMailer();

// If you intend you use SMTP, add your SMTP Code after this Line

if( $_SERVER['REQUEST_METHOD'] == 'POST' ) {

	$fname = $_POST['template-jobform-fname'];
	$lname = $_POST['template-jobform-lname'];
	$email = $_POST['template-jobform-email'];
	$age = $_POST['template-jobform-age'];
	$city = $_POST['template-jobform-city'];
	$position = $_POST['template-jobform-position'];
	$salary = $_POST['template-jobform-salary'];
	$start = $_POST['template-jobform-start'];
	$website = $_POST['template-jobform-website'];
	$experience = $_POST['template-jobform-experience'];
	$application = $_POST['template-jobform-application'];

	$name = $fname . ' ' . $lname;

	$subject = 'New Job Application';

	$botcheck = $_POST['template-jobform-botcheck'];

	if( $botcheck == '' ) {

		$mail->SetFrom( $email , $name );
		$mail->AddReplyTo( $email , $name );
		foreach( $toemails as $toemail ) {
			$mail->AddAddress( $toemail['email'] , $toemail['name'] );
		}
		$mail->Subject = $subject;

		$name = isset($name) ? "Name: $name<br><br>" : '';
		$email = isset($email) ? "Email: $email<br><br>" : '';
		$age = isset($age) ? "Age: $age<br><br>" : '';
		$city = isset($city) ? "City: $city<br><br>" : '';
		$position = isset($position) ? "Position: $position<br><br>" : '';
		$salary = isset($salary) ? "Salary: $salary<br><br>" : '';
		$start = isset($start) ? "Start: $start<br><br>" : '';
		$website = isset($website) ? "Website: $website<br><br>" : '';
		$experience = isset($experience) ? "Experience: $experience<br><br>" : '';
		$application = isset($application) ? "Application: $application<br><br>" : '';

		$referrer = $_SERVER['HTTP_REFERER'] ? '<br><br><br>This Form was submitted from: ' . $_SERVER['HTTP_REFERER'] : '';

		$body = "$name $email $age $city $position $salary $start $website $experience $application $referrer";

		// Runs only when File Field is present in the Contact Form
		if ( isset( $_FILES['template-jobform-cvfile'] ) && $_FILES['template-jobform-cvfile']['error'] == UPLOAD_ERR_OK ) {
			$mail->IsHTML(true);
			$mail->AddAttachment( $_FILES['template-jobform-cvfile']['tmp_name'], $_FILES['template-jobform-cvfile']['name'] );
		}

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
			echo 'We have <strong>successfully</strong> received your Application and will get Back to you as soon as possible.';
		else:
			echo 'Email <strong>could not</strong> be sent due to some Unexpected Error. Please Try Again later.<br /><br /><strong>Reason:</strong><br />' . $mail->ErrorInfo . '';
		endif;
	} else {
		echo 'Bot <strong>Detected</strong>.! Clean yourself Botster.!';
	}
} else {
	echo 'An <strong>unexpected error</strong> occured. Please Try Again later.';
}

?>