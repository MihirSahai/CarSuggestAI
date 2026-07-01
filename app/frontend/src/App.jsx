import React, { useState } from "react";

import PromptInput from "./components/PromptInput";
import RecommendationCard from "./components/RecommendationCard";
import LoadingIndicator from "./components/LoadingIndicator";
import FollowupBox from "./components/FollowupBox";

import { sendMessage } from "./api";

export default function App() {
  const [sessionId, setSessionId] = useState(null);

  const [recommendations, setRecommendations] = useState([]);
  const [explanation, setExplanation] = useState(null);

  const [followupQuestion, setFollowupQuestion] = useState(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSend = async (message) => {
    setLoading(true);
    setError(null);

    const res = await sendMessage(sessionId, message);

    if (res.session_id) setSessionId(res.session_id);

    // ERROR
    if (res.type === "ERROR") {
      setError(res.data.message);
      setLoading(false);
      return;
    }

    // CLARIFICATION
    if (res.type === "CLARIFICATION") {
      setFollowupQuestion(res.data.question);
      setRecommendations([]);
      setExplanation(null);
      setLoading(false);
      return;
    }

    // RECOMMENDATION
    if (res.type === "RECOMMENDATION") {
      setRecommendations(res.data.recommendations);
      setExplanation(res.data.explanation);
      setFollowupQuestion(null);
      setLoading(false);
      return;
    }

    setLoading(false);
  };

  const handleFollowup = async (answer) => {
    await handleSend(answer);
  };

  return (
    <div style={{ maxWidth: "750px", margin: "40px auto", fontFamily: "Arial" }}>
      <h2>🚗 AI Car Assistant</h2>

      <PromptInput onSend={handleSend} loading={loading} />

      {loading && <LoadingIndicator />}

      {error && (
        <div style={{ color: "red", marginTop: "10px" }}>
          ⚠️ {error}
        </div>
      )}

      <FollowupBox
        question={followupQuestion}
        onAnswer={handleFollowup}
        loading={loading}
      />

      {/* ---------------- EXPLANATION LAYER ---------------- */}
      {explanation && (
        <div
          style={{
            marginTop: "20px",
            padding: "12px",
            background: "#f7f7f7",
            borderRadius: "8px"
          }}
        >
          <h3>🧠 Why these cars?</h3>

          <p>{explanation.overall_summary}</p>

          {explanation.cars?.map((item, idx) => (
            <p key={idx}>
              🚗 <b>{item.car}</b>: {item.reason}
            </p>
          ))}
        </div>
      )}

      {/* ---------------- CARDS ---------------- */}
      <div style={{ marginTop: "20px" }}>
        {recommendations.map((car) => (
          <RecommendationCard key={car.id} car={car} />
        ))}
      </div>
    </div>
  );
}