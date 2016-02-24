<?php

require_once $_SERVER['DOCUMENT_ROOT'] .'/PhpProject1/defines.php';

if(isset($_POST['task']) && $_POST['task'] == 'comment_insert')
{
    $userId= (int)$_POST['userId'];
    $comment= addslashes(str_replace("\n","<br />",$_POST['comment']));
    
    $std= new stdClass();
    $comment_id=24;
    $std->userId=$userId;
    $std->comment=$comment;
    $std->userName="Saitama";
    $std->profile_img="httpdocs/images/saitama.jpg";
    require_once MODELS_DIR.'comments.php';
    if(class_exists('comments'))
    {
       $commentInfo= Comments::insert($comment,$userId);
       if($commentInfo != null)
       {
           
       }
    }
    echo json_encode($std);
    
    
    
}
else
{
//    echo 'sad';
   header('Location: http://localhost/PhpProject1/index.php' );
}




?>

