import React from "react";
import { useLocation } from "react-router-dom";

const CandidateAnalysis = () => {
  const location = useLocation();
  const {
    resumePath,
    score,
    strengths,
    weaknesses,
    suggestedSkills,
    gapsInExperience,
  } = location.state;

  // Debug: Log the location.state to verify the data
  console.log("Location State:", location.state);

  // Helper function to format text into bullet points
  const formatText = (text) => {
    return text
      .split("\n")
      .filter((item) => item.trim() !== "")
      .map((item, index) => (
        <li key={index}>
          {item.trim().replace(/^\*/, "").trim()}
        </li>
      ));
  };

  return (
    <div className="candidate-analysis">
      <h1>Candidate Analysis</h1>
      <div className="analysis-container">
        <div className="resume-preview">
          <h2>Resume Preview</h2>
          <iframe
            src={`http://localhost:5000${resumePath}`}
            title="Resume Preview"
            width="100%"
            height="100%"
          />
        </div>
        <div className="analysis-results">
          <h2>Score: {score !== undefined ? `${score}/100` : "N/A"}</h2> {/* Display the score */}
          <h2>Strengths</h2>
          <ul>{formatText(strengths)}</ul>

          <h2>Weaknesses</h2>
          <ul>{formatText(weaknesses)}</ul>

          <h2>Suggested Skills</h2>
          <ul>{formatText(suggestedSkills)}</ul>

          <h2>Gaps in Experience</h2>
          <ul>{formatText(gapsInExperience)}</ul>
        </div>
      </div>
    </div>
  );
};

export default CandidateAnalysis;