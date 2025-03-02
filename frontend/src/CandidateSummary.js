import React, { useEffect, useState } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";

const CandidateSummary = () => {
  const { id } = useParams(); 
  const [candidate, setCandidate] = useState(null);

  // Fetch candidate data when the component mounts
  useEffect(() => {
    axios.get(`http://localhost:5000/api/candidate/${id}`)
      .then(response => {
        console.log("Candidate Data:", response.data); // error function, remove later
        setCandidate(response.data);
      })
      .catch(error => {
        console.error("Error fetching candidate data:", error);
      });
  }, [id]);

  if (!candidate) {
    return <div>Loading...</div>;
  }

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
    <div className="candidate-summary">
      <h1>Candidate Summary</h1>
      <h2>{candidate.candidate_name}</h2>

      <div className="analysis-container">
        <div className="resume-preview">
          <h2>Resume Preview</h2>
          <iframe
            src={`http://localhost:5000${candidate.resumePath}`}  // Use resumePath
            title="Resume Preview"
            width="100%"
            height="600px"
          />
        </div>
        <div className="analysis-results">
          <h2>Score: {candidate.score !== undefined ? `${candidate.score}/100` : "N/A"}</h2> {/* Display the score */}
          <h2>Strengths</h2>
          <ul>{formatText(candidate.strengths)}</ul>

          <h2>Weaknesses</h2>
          <ul>{formatText(candidate.weaknesses)}</ul>

          <h2>Suggested Skills</h2>
          <ul>{formatText(candidate.suggested_skills)}</ul>

          <h2>Gaps in Experience</h2>
          <ul>{formatText(candidate.gaps_in_experience)}</ul>
        </div>
      </div>
    </div>
  );
};

export default CandidateSummary;