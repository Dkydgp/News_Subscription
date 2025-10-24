document.getElementById("subscribeForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const email = document.getElementById("email").value.trim();
  if (!email) {
    alert("⚠️ Please enter a valid email address!");
    return;
  }

  try {
    const res = await fetch("https://email-newsletter-flask.onrender.com/subscribe", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email })   // <-- key is "email"
    });

    if (res.ok) {
      alert("✅ Subscription successful!");
    } else {
      const data = await res.json().catch(()=>({}));
      alert("⚠️ Subscription failed: " + (data.message || res.status));
    }
  } catch (error) {
    console.error("Connection error:", error);
    alert("🚨 Server connection failed! Check console and try again.");
  }
});
