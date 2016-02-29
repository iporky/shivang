<?php if(isset($GLOBALS['comments']) && is_array($comments)):?>

<?php foreach($comments as $key=> $comment):?>
<?php $user=  subscribers::getSubscriber($comment->user_id); ?>


<li class="comment-holder" id="_ <?php echo $comment->comment_id; ?>">
                            <div class="usr-img">
                                <img src=<?php echo $user->profile_img; ?> class="usr-img-pic" />
                            </div> 
                             <div class="comment-body">
                                <h3 class="usrnm">
                                   <?php echo $user->userName; ?>
                                </h3>
                                <div class="comment-text">
                                    <?php echo $comment->comment; ?>  
                                    
                                </div>
                             </div>   
                            
                            <div class="comment-button-hldr">
                                <ul>
                                    <li class="dlt-btn">
                                    X
                                    </li>
                                
                                </ul> 
                            
                            </div>
                        
                        </li>
                        <?php endforeach; ?>
<?php endif; ?>
