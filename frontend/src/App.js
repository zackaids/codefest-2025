import React, { useState } from "react";
import { Route, Routes, Link, useNavigate } from "react-router-dom"; 
import axios from "axios";
import "./App.css";
import Leaderboard from "./Leaderboard";
import CandidateAnalysis from "./CandidateAnalysis"; 
import CandidateSummary from "./CandidateSummary";

function App() {
  const [jobDescription, setJobDescription] = useState("");
  const [selectedFile, setSelectedFile] = useState(null);
  const [jobId, setJobId] = useState("");
  const [jobName, setJobName] = useState("");
  const [skills, setSkills] = useState("");
  const navigate = useNavigate(); 

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
    setSkills(event.target.value);
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
    formData.append("skills", skills);

    axios
      .post("http://localhost:5000/api/uploadfile", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
      .then((response) => {
        console.log("File uploaded and evaluated successfully:", response.data);
        alert("File uploaded and evaluated successfully!");

        navigate("/candidate-analysis", {
          state: {
            resumePath: response.data.resumePath,
            score: response.data.score,
            strengths: response.data.strengths,
            weaknesses: response.data.weaknesses,
            suggestedSkills: response.data.suggested_skills,
            gapsInExperience: response.data.gaps_in_experience,
          },
        });
      })
      .catch((error) => {
        console.error("Error uploading file:", error);
        alert("Error uploading file. Please try again.");
      });
  };

  return (
    <div className="App">
      <nav className="navbar">
        <ul>
          <li>
            <Link to="/">Home</Link>
          </li>
          <li>
            <Link to="/leaderboard">Leaderboard</Link>
          </li>
        </ul>
      </nav>

      <Routes>
        <Route
          path="/"
          element={
            <>
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
            </>
          }
        />
        <Route path="/leaderboard" element={<Leaderboard />} />
        <Route path="/candidate-analysis" element={<CandidateAnalysis />} />
        <Route path="/candidate-summary/:id" element={<CandidateSummary />} />
      </Routes>
    </div>
  );
}

export default App;