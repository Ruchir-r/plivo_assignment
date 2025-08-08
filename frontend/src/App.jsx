import React, { useState } from "react";
import LoginPage from "./LoginPage";

function App() {
  const [token, setToken] = useState(localStorage.getItem("token") || null);
  const [profile, setProfile] = useState(null);

  const checkProfile = async () => {
    const res = await fetch("http://localhost:8001/users/me", {
      headers: { Authorization: "Bearer " + token },
    });
    const data = await res.json();
    setProfile(data);
  };

  return (
    <>
      {!token ? (
        <LoginPage onLogin={setToken} />
      ) : (
        <div>
          <h2>Logged in ✅</h2>
          <p>JWT: {token.substring(0, 20)}...</p>
          <button onClick={checkProfile}>Check Profile</button>
          {profile && <pre>{JSON.stringify(profile, null, 2)}</pre>}
        </div>
      )}
    </>
  );
}


export default App;
