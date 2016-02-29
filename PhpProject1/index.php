<?php  require_once $_SERVER['DOCUMENT_ROOT'] .'/PhpProject1/defines.php' ?>
<?php  require_once MODELS_DIR.'comments.php' ?>
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
        <script type="text/javascript" src="httpdocs/js/script.js?t=<?php echo time(); ?>"> </script>
    </head>
    <body>
        <div class="wrapper">
            <div class="page-data">
                page data is in here
            </div>
            <div class="comment-wrapper">
                <h3 class="comment-title">User comments.....</h3>
                
                <div class="comment-insert">
                    <h3 class="who-says"><span>Says</span>: Saitama</h3>
                    <div class="container-comnt" id="comment-insert-container">
                    <textarea id="comment-post-text" class="comments-insert-text"></textarea>
                    </div>
                    <div class="comment-post-btn-wrapper" id="comment-insert-btn">
                        Post
                        
                    </div>
                </div>
                
                <div class="comments-list">
                    <ul class="comment-holder-ul">
                       <?php $comments = comments::getComments(); ?>
                       <?php require_once INCLUDES . 'comment_box.php' ?> 
                        
                    </ul>
                    
                </div>
            </div>
        </div>
        
        <input type="hidden" id="userId" value="1"/>
        <input type="hidden" id="userName" value="Saitama"/>
        
    </body>
</html>
