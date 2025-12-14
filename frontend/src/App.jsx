import { useState } from "react";
import "./App.css";

function App() {
  const [form, setForm] = useState({
    Tenure_Months: "",
    Monthly_Charges: "",
    Total_Charges: "",
    Churn_Score: "",
    CLTV: "",
    Gender: "",
    Senior_Citizen: "",
    Partner: "",
    Dependents: "",
    Internet_Service: "",
    Contract: "",
    Payment_Method: ""
  });

  const [result, setResult] = useState(null);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const predictChurn = async () => {
    const response = await fetch("http://127.0.0.1:8000/api/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form),
    });

    const data = await response.json();
    setResult(data);
  };

  return (
    <div style={{ padding: "40px" }}>
      <h1>AI Churn Prediction</h1>

      {Object.keys(form).map((key) => (
        <div key={key} style={{ marginBottom: "14px" }}>
          <label>{key}</label>
          <input
            name={key}
            value={form[key]}
            onChange={handleChange}
            style={{ marginLeft: "10px", padding: "5px" }}
          />
        </div>
      ))}

      <button 
        onClick={predictChurn} 
        style={{ padding: "10px 20px", marginTop: "10px" }}
      >
        Predict Churn
      </button>

      {/* RESULT SECTION */}
      {result && (
        <div 
          style={{
            marginTop: "30px",
            padding: "20px",
            border: "1px solid #ccc",
            borderRadius: "8px",
            width: "350px",
          }}
        >
          <h3>Prediction Result</h3>
          <p><strong>Churn Prediction:</strong> {result.prediction}</p>
          <p><strong>Confidence:</strong> {result.confidence}</p>
        </div>
      )}
    </div>
  );
}

export default App;
