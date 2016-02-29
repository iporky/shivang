<?php

require_once MODELS_DIR.'subscribers.php';

class comments {
    
    public static function getComments()
    {
        $output= null;
        $sql= "select * from comments order by comment_id desc";
        
        $query=mysqli_query($GLOBALS['connect'], $sql);
        if($query )
        {
            $output = array();
            if(mysqli_num_rows($query) > 0)
            {
                while($row=mysqli_fetch_object($query))
                {
                    $output[]=$row;
                }
            
            return $output;    
            }
        }
        
    }
    public static function insert($comment,$userId)
    {
        
        $comment_txt=  addslashes($comment);
        $sql="insert into comments values('','$comment',$userId)";
        
        $query=mysqli_query($GLOBALS['connect'],$sql);
        
        if($query)
        {
            $insert_id= mysqli_insert_id($GLOBALS['connect']);
            $std= new stdClass();
            $comment_id=null;
            $std->comment=$comment;
            $std->userId=(int)$userId;
            return $std;
        }
        
        
        
        
        return null;
    }
    public static function delete($data)
    {
        //mysql_query('delete from comments where id=$commentId');
    }
    public static function update($data)
    {
        
    }

    
    
}
