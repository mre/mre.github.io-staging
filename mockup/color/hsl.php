<?php


function normalize($i) {
    // returns a normalized number with flat distribution from 0 to 1
    return (float)$i/(float)getrandmax();
}

/**
 * Converts an HSL color value to RGB. Conversion formula
 * adapted from http://en.wikipedia.org/wiki/HSL_color_space.
 * Assumes h, s, and l are contained in the set [0, 1] and
 * returns r, g, and b in the set [0, 255].
 *
 * @param   Number  h       The hue
 * @param   Number  s       The saturation
 * @param   Number  l       The lightness
 * @return  Array           The RGB representation
 */
function hslToRgb($h, $s, $l){

    if($s == 0){
        $r = $g = $b = $l; // achromatic
    }else{
        function hue2rgb($p, $q, $t){
            if($t < 0) $t += 1;
            if($t > 1) $t -= 1;
            if($t < 1/6) return $p + ($q - $p) * 6 * $t;
            if($t < 1/2) return $q;
            if($t < 2/3) return $p + ($q - $p) * (2/3 - $t) * 6;
            return $p;
        }

        $q = $l < 0.5 ? $l * (1 + $s) : $l + $s - $l * $s;
        $p = 2 * $l - $q;
        $r = hue2rgb($p, $q, $h + 1/3);
        $g = hue2rgb($p, $q, $h);
        $b = hue2rgb($p, $q, $h - 1/3);
    }

    return [round($r * 255), round($g * 255), round($b * 255)];
}

function colorize($name) {
  $id = hexdec(md5($name));
  return normalize($id);
}

echo colorize("Markus Enzler") . "\n";
echo colorize("Andreas Grunwald") . "\n";
echo colorize("Frankenstein") . "\n";

$saturation = 1;
$light = 0.5;

#print_r(hslToRgb($hue, $saturation, $light));
