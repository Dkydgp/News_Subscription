document.getElementById("subscribeForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const email = document.getElementById("email").value;

  try {
    const res = await fetch("https://news-subscription-ielo.onrender.com/subscribe", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email }),
    });

    if (res.ok) {
      alert("✅ Subscription successful!");
    } else {
      alert("⚠️ Subscription failed.");
    }
  } catch (err) {
    alert("🚨 Server connection failed!");
    console.error(err);
  }
});
