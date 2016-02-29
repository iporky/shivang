$(document).ready(function(){
   
    
    $('#comment-insert-btn').click(function(){
        comment_post_btn_click();
    });
});

function comment_post_btn_click()
{
    //text being posted.
    var _comment=$('#comment-post-text').val();
    var _userId=$('#userId').val();
    var _userName=$('#userName').val();

    if(_comment.length > 0 && _userId != null)
    {
        //ajax
        $('#comment-insert-container').css('border', '1px solid #e1e1e1');
        console.log(_comment+" "+ _userName);

        $.post("httpdocs/ajax/comment_insert.php",
        {
            task: "comment_insert",
            userId: _userId,
            comment: _comment
        }
       )
      .error( 
       function()
        {
            console.log("error"); 
        }
       )

      .success( 
       function(data)
        {
               comment_insert(jQuery.parseJSON(data));
        }
       );
    }
    else
    {
        $('#comment-insert-container').css('border', '1px solid red');
        console.log("text empty");
    }

    //removing text from textarea.
    $('#comment-post-text').val("");
}

function comment_insert(data)
{
   
   var t=''; 
   t += '<li class="comment-holder" id="_1'+data.comment.comment_id+'">';
   t += '    <div class="usr-img">';
   t += '         <img src="'+data.user.profile_img+'" class="usr-img-pic" />';
   t += '    </div>'; 
   t += '    <div class="comment-body">';
   t += '         <h3 class="usrnm">'+data.user.userName+'</h3>';
   t += '      <div class="comment-text">'+data.comment.comment+'</div>';
   t += '    </div> ';  
   t += '    <div class="comment-button-hldr">';
   t += '        <ul>';
   t += '        <li class="dlt-btn">X </li>';
   t += '        </ul> ';
   t += '    </div>';
   t += '</li>';
   
   
   $('.comment-holder-ul').prepend( t );
}

