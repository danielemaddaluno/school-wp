<?php
ini_set('display_errors', 1);
error_reporting(E_ALL);

// Database connection details
$host       = 'db'; // service name from docker-compose.yml
$user       = 'root';
$password   = 'password';

// Get all site folders and databases
$siteFolders = array_filter(glob('site*'), 'is_dir');  // Check for siteN folders in the current directory
$siteDatabases = [];

// Connect to the database and retrieve the list of databases
$conn = new mysqli($host, $user, $password);
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$result = $conn->query("SHOW DATABASES");
if ($result) {
    while ($row = $result->fetch_assoc()) {
        if (strpos($row['Database'], 'site') === 0) {
            $siteDatabases[] = $row['Database'];
        }
    }
}

// Create the table HTML
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>School School WordPress Sites Overview</title>
    <!-- Bootstrap CSS -->
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container">
        <h1 class="mt-5">School WordPress Sites Overview</h1>
        <p>Below is the status of each WordPress site:</p>

        <table class="table table-bordered">
            <thead>
                <tr>
                    <th>Site</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                <?php
                $maxSites = max(count($siteFolders), count($siteDatabases));

                for ($i = 1; $i <= $maxSites; $i++) {
                    $siteName = "site" . $i;
                    $siteUrl = "$siteName/";

                    // Check if the folder and the database exist
                    $folderExists = in_array($siteName, $siteFolders);
                    $dbExists = in_array($siteName, $siteDatabases);

                    // Check database connection
                    if ($folderExists && $dbExists) {
                        $dbConnection = new mysqli($host, $user, $password, $siteName);
                        $dbConnectionStatus = $dbConnection->connect_error ? false : true;
                        $dbConnection->close();
                    } else {
                        $dbConnectionStatus = false;
                    }

                    // Table row: Site link and connection status
                    echo "<tr>";
                    echo "<td><a href='$siteUrl'>$siteName</a></td>";
                    echo "<td>";
                    if ($dbConnectionStatus) {
                        echo "<span class='text-success'>&#10004; Database Connected</span>";
                    } else {
                        echo "<span class='text-danger'>&#10008; Database Not Connected</span>";
                    }
                    echo "</td>";
                    echo "</tr>";
                }

                $conn->close();
                ?>
            </tbody>
        </table>
    </div>

    <!-- Link to phpinfo.php -->
    <div class="container">
        <p>For PHP configuration details, visit the <a href="phpinfo.php" target="_blank">PHP Info</a> page.</p>
    </div>

    <!-- Bootstrap JS and dependencies -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>
