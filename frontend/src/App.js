import React, { useState } from "react";
import { Route, Routes, useNavigate } from "react-router-dom"; 
import axios from "axios";
import "./App.css";
import Navbar from "./Navbar.js";
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
      {/* Use the new Navbar component instead of the inline navbar */}
      <Navbar />

      <Routes>
        <Route
          path="/"
          element={
            <div className="home-container">
              <div className="hero-section">
                <h1>Welcome to <span className="highlight">HireHive</span></h1>
                <p className="tagline">Find your perfect candidate with our intelligent resume analysis</p>
                <button className="cta-button" onClick={() => navigate('/evaluate')}>
                  Evaluate a Candidate
                </button>
              </div>
              
              <div className="features-section">
                <div className="feature-card">
                  <div className="feature-icon">📋</div>
                  <h3>Resume Analysis</h3>
                  <p>Upload resumes and get instant AI-powered analysis</p>
                </div>
                <div className="feature-card">
                  <div className="feature-icon">🏆</div>
                  <h3>Candidate Ranking</h3>
                  <p>Compare candidates and find the best fit for your position</p>
                </div>
                <div className="feature-card">
                  <div className="feature-icon">💡</div>
                  <h3>Skill Matching</h3>
                  <p>Identify strengths and gaps in candidate experience</p>
                </div>
              </div>
            </div>
          }
        />
        <Route
          path="/evaluate"
          element={
            <div className="evaluate-container">
              <h1>Evaluate a Candidate</h1>
              <div className="input-container">
                <h2>Job Details</h2>
                <div className="job-detail-inputs">
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
                </div>
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
                <div className="file-upload-area">
                  <input type="file" id="resume-file" onChange={onFileChange} />
                  <label htmlFor="resume-file" className="file-label">
                    {selectedFile ? selectedFile.name : "Choose a file"}
                  </label>
                </div>
                <button className="upload-button" onClick={onFileUpload}>Upload and Evaluate</button>
              </div>
            </div>
          }
        />
        <Route path="/leaderboard" element={<Leaderboard />} />
        <Route path="/candidate-analysis" element={<CandidateAnalysis />} />
        <Route path="/candidate-summary/:id" element={<CandidateSummary />} />
      </Routes>

      <footer className="footer">
        <div className="footer-content">
          <p>&copy; {new Date().getFullYear()} HireHive. All rights reserved.</p>
          <div className="footer-links">
            <a href="#">Privacy Policy</a>
            <a href="#">Terms of Service</a>
            <a href="#">Contact Us</a>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;