import React, { useState } from "react";

export default function Summarizer() {
  const [tab, setTab] = useState("upload"); // 'upload' or 'url'
  const [file, setFile] = useState(null);
  const [url, setUrl] = useState("");
  const [summary, setSummary] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setSummary("");
    setLoading(true);

    try {
      const formData = new FormData();

      if (tab === "upload") {
        if (!file) {
          setError("Please upload a file.");
          setLoading(false);
          return;
        }
        formData.append("file", file);
      } else {
        if (!url.trim()) {
          setError("Please enter a URL.");
          setLoading(false);
          return;
        }
        formData.append("url", url.trim());
      }

      const response = await fetch("/api/summarize", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`);
      }

      const data = await response.json();
      setSummary(data.summary || "No summary returned.");
    } catch (err) {
      setError(err.message);
    }

    setLoading(false);
  }

  return (
    <div style={{ maxWidth: 600, margin: "auto", padding: 20 }}>
      <h2>Document / URL Summarizer</h2>
      <div>
        <button onClick={() => setTab("upload")} disabled={tab === "upload"}>
          Upload Document
        </button>
        <button onClick={() => setTab("url")} disabled={tab === "url"}>
          Enter URL
        </button>
      </div>

      <form onSubmit={handleSubmit} style={{ marginTop: 20 }}>
        {tab === "upload" && (
          <input
            type="file"
            accept=".pdf,.doc,.docx"
            onChange={(e) => setFile(e.target.files[0])}
          />
        )}
        {tab === "url" && (
          <input
            type="url"
            placeholder="Enter URL"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            style={{ width: "100%", padding: 8 }}
          />
        )}
        <button type="submit" disabled={loading} style={{ marginTop: 10 }}>
          {loading ? "Summarizing..." : "Summarize"}
        </button>
      </form>

      {error && <p style={{ color: "red" }}>{error}</p>}
      {summary && (
        <div style={{ marginTop: 20, whiteSpace: "pre-wrap" }}>
          <h3>Summary</h3>
          <p>{summary}</p>
        </div>
      )}
    </div>
  );
}
