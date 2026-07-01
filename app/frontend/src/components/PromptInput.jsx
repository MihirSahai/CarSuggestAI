import React, { useState } from "react";

export default function PromptInput({ onSend, loading }) {
  const [text, setText] = useState("");

  const handleSend = () => {
    if (!text.trim()) return;
    onSend(text);
    setText("");
  };

  return (
    <div style={{ display: "flex", gap: "10px" }}>
      <input
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Describe your car requirement..."
        style={{
          flex: 1,
          padding: "10px",
          border: "1px solid #ccc",
          borderRadius: "6px"
        }}
      />

      <button
        onClick={handleSend}
        disabled={loading}
        style={{
          padding: "10px 16px",
          background: "#111",
          color: "#fff",
          border: "none",
          borderRadius: "6px",
          cursor: "pointer"
        }}
      >
        Send
      </button>
    </div>
  );
}