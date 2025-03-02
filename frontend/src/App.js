import React, { useState } from "react";
import axios from "axios";
import './App.css';

function App() {
  const [jobDescription, setJobDescription] = useState("");
  const [selectedFile, setSelectedFile] = useState(null);
  const [jobId, setJobId] = useState("");
  const [jobName, setJobName] = useState("");
  const [skills, setSkills] = useState(""); // New state for skills

  const onFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const onJobDescriptionChange = (event) => {
    setJobDescription(event.target.value);
  };

  const onJobIdChange = (event) => {
    setJobId(event.target.value);
  };

  const onJobNameChange = (event) => {
    setJobName(event.target.value);
  };

  const onSkillsChange = (event) => {
    setSkills(event.target.value); // Handle skills input change
  };

  const onFileUpload = () => {
    if (!selectedFile) {
      alert("Please select a file first.");
      return;
    }

    if (!jobId || !jobName || !skills) {
      alert("Please enter Job ID, Job Name, and Skills.");
      return;
    }

    const formData = new FormData();
    formData.append("myFile", selectedFile, selectedFile.name);
    formData.append("jobDescription", jobDescription);
    formData.append("jobId", jobId);
    formData.append("jobName", jobName);
    formData.append("skills", skills); // Add skills to the form data

    axios.post("http://localhost:5000/api/uploadfile", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    })
    .then((response) => {
      console.log("File uploaded successfully:", response.data);
      alert("File uploaded successfully!");
    })
    .catch((error) => {
      console.error("Error uploading file:", error);
      alert("Error uploading file. Please try again.");
    });
  };

  return (
    <div className="App">
      <h1>HireHive</h1>
      <div className="input-container">
        <h2>Job Details</h2>
        <input
          type="text"
          placeholder="Job ID"
          value={jobId}
          onChange={onJobIdChange}
          className="job-id-input"
        />
        <input
          type="text"
          placeholder="Job Name"
          value={jobName}
          onChange={onJobNameChange}
          className="job-name-input"
        />
        <h2>Job Description</h2>
        <textarea
          className="job-description-input"
          placeholder="Paste the job description here..."
          value={jobDescription}
          onChange={onJobDescriptionChange}
        />
        <h2>Skills Required</h2>
        <textarea
          className="skills-input"
          placeholder="Enter the skills you're looking for (comma-separated)..."
          value={skills}
          onChange={onSkillsChange}
        />
      </div>
      <div className="upload-container">
        <h2>Upload Resume (PDF)</h2>
        <input type="file" onChange={onFileChange} />
        <button onClick={onFileUpload}>Upload and Evaluate</button>
      </div>
    </div>
  );
}

export default App;