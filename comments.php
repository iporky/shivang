<?php


class comments {
    
    public static function getComments()
    {
        
    }
    public static function insert($comment,$userId)
    {
        
        //mysql_query("insert into comments('','$comment',$userId)");
        $std= new stdClass();
        $comment_id=null;
        $std->comment=$comment;
        $std->userId=(int)$userId;
        
        return $std;
    }
    public static function delete($data)
    {
        //mysql_query('delete from comments where id=$commentId');
    }
    public static function update($data)
    {
        
    }

    
    
}
