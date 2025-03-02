import React, { useEffect, useState } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import "./Leaderboard.css";

const Leaderboard = () => {
  const [jobIds, setJobIds] = useState([]); 
  const [selectedJobId, setSelectedJobId] = useState(null); 
  const [leaderboardData, setLeaderboardData] = useState([]); 

  // Fetch all job IDs when the component mounts
  // need to change this ...!!!
  useEffect(() => {
    axios.get("http://localhost:5000/api/jobs")
      .then(response => {
        setJobIds(response.data.job_ids);
      })
      .catch(error => {
        console.error("Error fetching job IDs:", error);
      });
  }, []);

  // Fetch leaderboard data when a job ID is selected
  useEffect(() => {
    if (selectedJobId) {
      axios.get(`http://localhost:5000/api/leaderboard/${selectedJobId}`)
        .then(response => {
          setLeaderboardData(response.data.candidates);
        })
        .catch(error => {
          console.error("Error fetching leaderboard data:", error);
        });
    }
  }, [selectedJobId]);

  return (
    <div className="leaderboard-page">
      <div className="job-hex-grid">
        {jobIds.map((jobId, index) => (
          <div
            key={index}
            className="hex-button"
            onClick={() => setSelectedJobId(jobId)}
          >
            {jobId}
          </div>
        ))}
      </div>

      {selectedJobId && (
        <div className="leaderboard-container">
          <div className="leaderboard">
            <h2>Leaderboard for Job ID: {selectedJobId}</h2>
            <table>
              <thead>
                <tr>
                  <th>Rank</th>
                  <th>Candidate</th>
                  <th>Score</th>
                </tr>
              </thead>
              <tbody>
                {leaderboardData.map((candidate, index) => (
                  <tr key={index} data-score={candidate.score}>
                    <td>{index + 1}</td>
                    <td>
                      <Link to={`/candidate-summary/${candidate._id}`}>
                        {candidate.candidate_name || "Unknown Candidate"}
                      </Link>
                    </td>
                    <td>{candidate.score}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};

export default Leaderboard;