<?php

require_once 'common.php';

class UserDAO {

    public function authenticate($userid, $password) { 
        // Authenticate Student Login
        
        // Connect to Database
        $connMgr = new connectionManager();
        $conn = $connMgr->getConnection();

        // Write & Prepare SQL Query (take care of Param Binding if necessary)
        $sql = "SELECT * FROM USER WHERE userid=:userid";
        $stmt = $conn->prepare($sql);
        $stmt->bindParam(':userid',$userid,PDO::PARAM_STR);
        
        // Execute SQL Query
        $stmt->setFetchMode(PDO::FETCH_ASSOC);
        $status=$stmt->execute();

        // Retrieve Query Results (if any)
        $return_message = 'Invalid username!';
        if ($row=$stmt->fetch()){
            if ($password===$row['password']){
                $return_message= 'SUCCESS';
            }
            else{
                $return_message='Password is incorrect!';
            }
        }
        
        // Clear Resources $stmt, $pdo
        $stmt = null;
        $conn = null;

        // Return (if any)
        return $return_message;
    }
}


?>