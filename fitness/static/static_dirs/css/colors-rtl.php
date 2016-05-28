<?php

header ("Content-Type:text/css");

/** ===============================================================
 *
 *      Edit your Color Configurations below:
 *      You should only enter 6-Digits HEX Colors.
 *
 ================================================================== */

$color = "#1ABC9C"; // Change your Color Here

/** ===============================================================
 *
 *      Do not Edit anything below this line if you do not know
 *      what you are trying to do..!
 *
 ================================================================== */

function checkhexcolor($color) {

    return preg_match('/^#[a-f0-9]{6}$/i', $color);

}

/** ===============================================================
 *
 *      Primary Color Scheme
 *
 ================================================================== */

if( isset( $_GET[ 'color' ] ) AND $_GET[ 'color' ] != '' ) {
    $color = "#" . $_GET[ 'color' ];
}

if( !$color OR !checkhexcolor( $color ) ) {
    $color = "#1ABC9C";
}

?>


/* ----------------------------------------------------------------
    Colors

    Replace the HEX Code with your Desired Color HEX
-----------------------------------------------------------------*/

#page-menu.dots-menu nav li span:after,
.title-block { border-left-color: <?php echo $color; ?>; }

.title-block-right { border-right-color: <?php echo $color; ?>; }

.fbox-effect.fbox-dark .fbox-icon i:after,
.dark .fbox-effect.fbox-dark .fbox-icon i:after { box-shadow: 0 0 0 2px <?php echo $color; ?>; }

.fbox-border.fbox-effect.fbox-dark .fbox-icon i:hover,
.fbox-border.fbox-effect.fbox-dark:hover .fbox-icon i,
.dark .fbox-border.fbox-effect.fbox-dark .fbox-icon i:hover,
.dark .fbox-border.fbox-effect.fbox-dark:hover .fbox-icon i { box-shadow: 0 0 0 0 <?php echo $color; ?>; }

