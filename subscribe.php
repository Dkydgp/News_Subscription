<?php
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: POST");
header("Access-Control-Allow-Headers: Content-Type");

// ✅ Database credentials will come from Render environment variables
$servername = getenv("DB_HOST");
$username   = getenv("DB_USER");
$password   = getenv("DB_PASS");
$dbname     = getenv("DB_NAME");

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
  die(json_encode(["status" => "error", "message" => "Database connection failed."]));
}

// Read incoming data
$data = json_decode(file_get_contents("php://input"), true);
$email = $data["email"] ?? "";

if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
  echo json_encode(["status" => "error", "message" => "Invalid email address."]);
  exit;
}

// Insert new subscriber with timestamp
$stmt = $conn->prepare("INSERT INTO subscribers (email, subscribed_at) VALUES (?, NOW())");
$stmt->bind_param("s", $email);

if ($stmt->execute()) {
  echo json_encode(["status" => "success", "message" => "Email saved successfully."]);
} else {
  if ($conn->errno === 1062) {
    echo json_encode(["status" => "error", "message" => "This email is already subscribed."]);
  } else {
    echo json_encode(["status" => "error", "message" => "Database error occurred."]);
  }
}

$stmt->close();
$conn->close();
?>
