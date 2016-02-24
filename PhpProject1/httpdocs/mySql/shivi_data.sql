
CREATE TABLE `subscribers` (
 `userId` int(11) NOT NULL AUTO_INCREMENT,
 `userName` varchar(255) NOT NULL,
 `profile_img` varchar(255) NOT NULL,
 PRIMARY KEY (`userId`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;




CREATE TABLE `comments` (
 `comment_id` int(11) NOT NULL AUTO_INCREMENT,
 `comment` text NOT NULL,
 `user_id` int(11) NOT NULL,
 PRIMARY KEY (`comment_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;



