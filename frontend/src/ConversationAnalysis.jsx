import React, { useState } from "react";

export default function ConversationAnalysis() {
  const [file, setFile] = useState(null);
  const [transcript, setTranscript] = useState("");
  const [diarization, setDiarization] = useState([]);
  const [loading, setLoading] = useState(false);

  const onFileChange = (e) => {
    setFile(e.target.files[0]);
    setTranscript("");
    setDiarization([]);
  };

  const handleSubmit = async () => {
    if (!file) return alert("Please upload an audio file");
    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://localhost:8000/api/conversation", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setTranscript(data.transcript);
      setDiarization(data.diarization);
    } catch (error) {
      alert("Error processing audio");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h3>Conversation Analysis (Speech to Text + Diarization)</h3>
      <input type="file" accept="audio/*" onChange={onFileChange} />
      <button onClick={handleSubmit} disabled={loading}>
        {loading ? "Processing..." : "Analyze"}
      </button>

      {transcript && (
        <div>
          <h4>Transcript:</h4>
          <p>{transcript}</p>
        </div>
      )}

      {diarization.length > 0 && (
        <div>
          <h4>Diarization:</h4>
          <ul>
            {diarization.map((seg, i) => (
              <li key={i}>
                Speaker: {seg.speaker}, Start: {seg.start.toFixed(2)}s, End:{" "}
                {seg.end.toFixed(2)}s
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
