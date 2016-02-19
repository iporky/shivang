<?php  require_once $_SERVER['DOCUMENT_ROOT'] .'/PhpProject1/defines.php' ?>
<!DOCTYPE html>
<!--
To change this license header, choose License Headers in Project Properties.
To change this template file, choose Tools | Templates
and open the template in the editor.
-->
<html>
    <head>
        <meta charset="UTF-8">
        <title>Comment Box</title>
        <link href="httpdocs/css/layout.css" rel="stylesheet" />
        <script type="text/javascript" src="httpdocs/js/jquery.js"> </script>
        <script type="text/javascript" src="httpdocs/js/script.js"> </script>
    </head>
    <body>
        <div class="wrapper">
            <div class="page-data">
                page data is in here
            </div>
            <div class="comment-wrapper">
                <h3 class="comment-title">User comments.....</h3>
                
                <div class="comment-insert">
                    <h3 class="who-says">Says: Saitama</h3>
                    <textarea class="comments-insert-text"></textarea>
                </div>
                
                <div class="comments-list">
                    <ul class="comment-holder-ul">
                       <?php $comments = array("a", "b" ,"c", "d","e","f")?>
                       <?php require_once INCLUDES . 'comment_box.php' ?> 
                        
                    </ul>
                    
                </div>
            </div>
        </div>
    </body>
</html>
