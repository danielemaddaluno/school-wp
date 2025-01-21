<?php
$host       = 'db'; // service name from docker-compose.yml
$user       = 'root';
$password   = 'password';
$db         = 'site1';

echo "Connection test:";
echo "<br>";

$conn = new mysqli($host, $user, $password, $db);

if($conn->connect_error){
   echo 'Connection failed: ' . $conn->connect_error;
} else {
   echo 'Sucessfully connected to MySQL';
}
?>

<?php
phpinfo();
?>