async function subscribe(e) {
  e.preventDefault();

  const emailField = document.getElementById('email');
  const message = document.getElementById('message');
  const email = emailField.value.trim();

  if (!email) {
    message.textContent = "⚠️ Please enter a valid email address!";
    message.style.color = "red";
    return;
  }

  try {
    // ⚠️ Replace this URL after Render deploy
    const response = await fetch("https://news-subscription.onrender.com/subscribe.php", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email })
    });

    const result = await response.json();

    if (result.status === "success") {
      message.textContent = "✅ Subscribed successfully!";
      message.style.color = "green";
      emailField.value = "";
    } else {
      message.textContent = "❌ " + result.message;
      message.style.color = "red";
    }
  } catch (error) {
    console.error("Error:", error);
    message.textContent = "❌ Server connection failed.";
    message.style.color = "red";
  }
}
