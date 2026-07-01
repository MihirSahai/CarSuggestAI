import React, { useState } from "react";

export default function FollowupBox({ question, onAnswer, loading }) {
  const [answer, setAnswer] = useState("");

  if (!question) return null;

  return (
    <div style={{ marginTop: "20px" }}>
      <p style={{ fontWeight: "bold" }}>💬 {question}</p>

      <div style={{ display: "flex", gap: "10px" }}>
        <input
          value={answer}
          onChange={(e) => setAnswer(e.target.value)}
          placeholder="Your answer..."
          style={{
            flex: 1,
            padding: "10px",
            border: "1px solid #ccc",
            borderRadius: "6px"
          }}
        />

        <button
          onClick={() => {
            onAnswer(answer);
            setAnswer("");
          }}
          disabled={loading}
          style={{
            padding: "10px 16px",
            background: "#333",
            color: "#fff",
            border: "none",
            borderRadius: "6px"
          }}
        >
          Submit
        </button>
      </div>
    </div>
  );
}