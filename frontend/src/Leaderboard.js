import React, { useEffect, useState } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import "./Leaderboard.css";

const Leaderboard = () => {
  const [jobs, setJobs] = useState([]); // Jobs with id and name
  const [selectedJobId, setSelectedJobId] = useState(null);
  const [leaderboardData, setLeaderboardData] = useState([]);
  const [loading, setLoading] = useState(true);

  // Fetch all jobs when the component mounts
  useEffect(() => {
    setLoading(true);
    axios.get("http://localhost:5000/api/jobs")
      .then(response => {
        // Use the actual job names from the API response
        setJobs(response.data.jobs.map(job => ({ id: job.id, name: job.name })));
        setLoading(false);
      })
      .catch(error => {
        console.error("Error fetching jobs:", error);
        setLoading(false);
      });
  }, []);
  
  // Fetch leaderboard data when a job ID is selected
  useEffect(() => {
    if (selectedJobId) {
      setLoading(true);
      axios.get(`http://localhost:5000/api/leaderboard/${selectedJobId}`)
        .then(response => {
          setLeaderboardData(response.data.candidates);
          // If you want to update the job name from the response:
          // const jobIndex = jobs.findIndex(job => job.id === selectedJobId);
          // if (jobIndex !== -1) {
          //   const updatedJobs = [...jobs];
          //   updatedJobs[jobIndex].name = response.data.job_name;
          //   setJobs(updatedJobs);
          // }
          setLoading(false);
        })
        .catch(error => {
          console.error("Error fetching leaderboard data:", error);
          setLoading(false);
        });
    }
  }, [selectedJobId]);

  // Helper function to determine candidate status based on score
  const getCandidateStatus = (score) => {
    if (score >= 80) return "excellent";
    if (score >= 60) return "good";
    if (score >= 40) return "average";
    return "poor";
  };

  return (
    <div className="leaderboard-page">
      <h1>Job Selection</h1>
      
      {/* Hexagon Grid for Job Selection */}
      <div className="grid-container">
        <div className="hex-grid">
          {jobs.map((job) => (
            <div 
              key={job.id}
              className={`hex-item ${selectedJobId === job.id ? "selected" : ""}`}
              onClick={() => setSelectedJobId(job.id)}
            >
              <div className="hex-content">
                <div className="job-info">
                  <div className="job-name">{job.name}</div>
                  <div className="job-id">ID: {job.id}</div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Leaderboard Display */}
      {selectedJobId && (
        <div className="leaderboard-container">
          <div className="leaderboard">
            <h2>Candidates for {jobs.find(job => job.id === selectedJobId)?.name || `Job ${selectedJobId}`}</h2>
            
            {loading ? (
              <div className="loading">Loading leaderboard data...</div>
            ) : leaderboardData.length > 0 ? (
              <table>
                <thead>
                  <tr>
                    <th>Rank</th>
                    <th>Candidate</th>
                    <th>Score</th>
                    <th>Status</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {leaderboardData.map((candidate, index) => (
                    <tr 
                      key={index} 
                      className={getCandidateStatus(candidate.score)}
                    >
                      <td>{index + 1}</td>
                      <td>{candidate.candidate_name || "Unknown Candidate"}</td>
                      <td>{candidate.score}</td>
                      <td>
                        <span className="status-badge">
                          {getCandidateStatus(candidate.score)}
                        </span>
                      </td>
                      <td>
                        <Link 
                          to={`/candidate-summary/${candidate._id}`}
                          className="details-btn"
                        >
                          Details
                        </Link>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <div className="no-data">No candidates found for this job.</div>
            )}
          </div>
        </div>
      )}

      {!selectedJobId && (
        <div className="instructions">
          <p>Please select a job from the honeycomb grid above to view its leaderboard.</p>
        </div>
      )}
    </div>
  );
};

export default Leaderboard;