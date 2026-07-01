import React from "react";

export default function RecommendationCard({ car }) {
  return (
    <div
      style={{
        border: "1px solid #ddd",
        padding: "12px",
        borderRadius: "8px",
        marginBottom: "10px"
      }}
    >
      <h3>{car.display_name}</h3>

      <p>💰 Price: ₹{car.price_lakh}L</p>
      <p>⛽ Fuel: {car.fuel_type}</p>
      <p>🪑 Seats: {car.seating}</p>

      <p>⭐ Safety: {car.safety} | Mileage: {car.mileage}</p>

      <p style={{ fontWeight: "bold" }}>
        Score: {car.score}
      </p>
    </div>
  );
}