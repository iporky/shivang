<?php

require_once $_SERVER['DOCUMENT_ROOT'] .'/PhpProject1/defines.php';

if(isset($_POST['task']) && $_POST['task'] == 'comment_insert')
{
    $userId= (int)$_POST['userId'];
    $comment= addslashes(str_replace("\n","<br />",$_POST['comment']));
    
       $std= new stdClass();
       $std->user= NULL;
       $std->comment=NULL;
       $std->error=false;
    
    require_once MODELS_DIR.'comments.php';
    if(class_exists('comments')&& class_exists('subscribers'))
    {
       
       $userInfo = subscribers::getSubscriber($userId);
       if($userInfo == null)
       {
          $std->error=TRUE; 
       }
       
       $commentInfo= comments::insert($comment,$userId);
       if($commentInfo == null)
       {
           $std->error=TRUE;
       }
       $std= new stdClass();
       $std->user= $userInfo;
       $std->comment=$commentInfo;
      
       
       
    }
    echo json_encode($std);
    
    
    
}
else
{
//    echo 'sad';
   header('Location: http://localhost/PhpProject1/index.php' );
}




?>

