import React, { useState } from "react";
import LoginPage from "./LoginPage";
import Summarizer from "./Summarizer";

// Main App component
// Handles login state and profile checking
// Displays LoginPage if not logged in, otherwise shows profile and summarizer
// Uses localStorage to persist JWT token
// Fetches user profile on button click
// Displays JWT token and profile information

function App() {
  const [token, setToken] = useState(localStorage.getItem("token") || null);
  const [profile, setProfile] = useState(null);

  // Save token to localStorage when token changes
  React.useEffect(() => {
    if (token) {
      localStorage.setItem("token", token);
    } else {
      localStorage.removeItem("token");
      setProfile(null);
    }
  }, [token]);

  const checkProfile = async () => {
    try {
      const res = await fetch("https://plivo-assignment-okge.onrender.com/api/users/me", {
        headers: { Authorization: "Bearer " + token },
      });
      if (!res.ok) throw new Error("Failed to fetch profile");
      const data = await res.json();
      setProfile(data);
    } catch (err) {
      alert(err.message);
      setToken(null);
    }
  };

  const logout = () => {
    setToken(null);
  };

  return (
    <>
      {!token ? (
        <LoginPage onLogin={setToken} />
      ) : (
        <div style={{ maxWidth: 800, margin: "auto", padding: 20 }}>
          <h2>Logged in ✅</h2>
          <p><strong>JWT:</strong> {token.substring(0, 20)}...</p>
          <button onClick={checkProfile} style={{ marginRight: 10 }}>
            Check Profile
          </button>
          <button onClick={logout}>Logout</button>

          {profile && (
            <div>
              <h3>Profile Info</h3>
              <pre>{JSON.stringify(profile, null, 2)}</pre>
            </div>
          )}

          <hr style={{ margin: "40px 0" }} />

          <Summarizer />
        </div>
      )}
    </>
  );
}

export default App;
