import React, { useState } from "react";

export default function ImageAnalysis() {
  const [file, setFile] = useState(null);
  const [description, setDescription] = useState("");
  const [loading, setLoading] = useState(false);

  const onFileChange = (e) => {
    setFile(e.target.files[0]);
    setDescription("");
  };

  const handleSubmit = async () => {
    if (!file) return alert("Please upload an image file");
    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://localhost:8001/api/image", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setDescription(data.description);
    } catch (error) {
      alert("Error analyzing image");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h3>Image Analysis</h3>
      <input type="file" accept="image/*" onChange={onFileChange} />
      <button onClick={handleSubmit} disabled={loading}>
        {loading ? "Analyzing..." : "Analyze Image"}
      </button>

      {description && (
        <div>
          <h4>Description:</h4>
          <p>{description}</p>
        </div>
      )}
    </div>
  );
}

