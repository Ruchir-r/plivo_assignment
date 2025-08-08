import React, { useState } from "react";
import LoginPage from "./LoginPage";
import ConversationAnalysis from "./ConversationAnalysis";
import ImageAnalysis from "./ImageAnalysis";
import Summarization from "./Summarization";

function App() {
  // Auth state
  const [token, setToken] = useState(localStorage.getItem("token") || null);
  const [profile, setProfile] = useState(null);

  // Skill selection
  const [skill, setSkill] = useState("conversation");

  // Fetch user profile
  const checkProfile = async () => {
    if (!token) return;
    try {
      const res = await fetch("https://plivo-assignment-okge.onrender.com/api/users/me", {
        headers: { Authorization: "Bearer " + token },
      });
      if (!res.ok) throw new Error("Failed to fetch profile");
      const data = await res.json();
      setProfile(data);
    } catch (error) {
      alert("Error fetching profile: " + error.message);
    }
  };

  // Save token to localStorage and state on login
  const handleLogin = (newToken) => {
    localStorage.setItem("token", newToken);
    setToken(newToken);
  };

  // Logout handler
  const handleLogout = () => {
    localStorage.removeItem("token");
    setToken(null);
    setProfile(null);
  };

  if (!token) {
    return <LoginPage onLogin={handleLogin} />;
  }

  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h1>Multi-Modal AI Playground</h1>
      <div style={{ marginBottom: "20px" }}>
        <h2>Logged in ✅</h2>
        <p>
          JWT: {token.substring(0, 20)}...
          <button onClick={handleLogout} style={{ marginLeft: "10px" }}>
            Logout
          </button>
        </p>
        <button onClick={checkProfile}>Check Profile</button>
        {profile && (
          <pre
            style={{
              background: "#f0f0f0",
              padding: "10px",
              maxWidth: "600px",
              overflowX: "auto",
            }}
          >
            {JSON.stringify(profile, null, 2)}
          </pre>
        )}
      </div>

      <label htmlFor="skill-select">Select Skill:</label>
      <select
        id="skill-select"
        value={skill}
        onChange={(e) => setSkill(e.target.value)}
        style={{ marginLeft: "10px", padding: "5px" }}
      >
        <option value="conversation">Conversation Analysis</option>
        <option value="image">Image Analysis</option>
        <option value="summarization">Document/URL Summarization</option>
      </select>

      <hr />

      {skill === "conversation" && <ConversationAnalysis token={token} />}
      {skill === "image" && <ImageAnalysis token={token} />}
      {skill === "summarization" && <Summarization token={token} />}
    </div>
  );
}

export default App;
