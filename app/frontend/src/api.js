const BASE_URL = "https://carsuggestai.onrender.com/api"
export async function sendMessage(session_id, message) {
  try {
    const res = await fetch(`${BASE_URL}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        session_id,
        message
      })
    });

    if (!res.ok) {
      throw new Error("Server error");
    }

    return await res.json();

  } catch (err) {
    return {
      type: "ERROR",
      data: {
        message: err.message || "Something went wrong"
      }
    };
  }
}