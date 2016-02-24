<?php
define('DOC_ROOT' , $_SERVER['DOCUMENT_ROOT'].'/');
define('DS', DIRECTORY_SEPARATOR);

define('INCLUDES', DOC_ROOT . 'PhpProject1/httpdocs/includes'. DS);
define('MODELS_DIR', DOC_ROOT . 'PhpProject1/httpdocs/mySql'.DS.'models'.DS);
define('MYSQL_DIR', DOC_ROOT . 'PhpProject1/httpdocs/mySql'.DS);

require_once MYSQL_DIR.'db_connect.php';
?>
