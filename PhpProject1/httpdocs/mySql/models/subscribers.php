<?php
require_once MYSQL_DIR.'db_connect.php';

class subscribers {
    
    public static function getSubscriber($userID)
    {
        
        $sql= "select * from subscribers where userId=$userID";
        $query= mysqli_query($GLOBALS ['connect'],$sql);
        
        if ($query)
        {
            if(mysqli_num_rows($query)== 1)
            {
                return mysqli_fetch_object($query);
            }
        }
        return null;
    }
}