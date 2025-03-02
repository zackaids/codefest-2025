import React from "react";
import { Link, useLocation } from "react-router-dom";
import logo from "./logo.png"; // Make sure your logo.png is in the same directory
import "./Navbar.css"; // We'll create this file next

function Navbar() {
  const location = useLocation();
  
  // Check which page is active
  const isActive = (path) => {
    return location.pathname === path ? "active" : "";
  };
  
  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="logo-container">
          <Link to="/" className="logo-link">
            <img src={logo} alt="HireHive Logo" className="logo-image" />
            <span className="logo-text">HireHive</span>
          </Link>
        </div>
        <div className="nav-links">
          <Link to="/" className={`nav-item ${isActive("/")}`}>
            Home
          </Link>
          <Link to="/evaluate" className={`nav-item ${isActive("/evaluate")}`}>
            Evaluate Candidate
          </Link>
          <Link to="/leaderboard" className={`nav-item ${isActive("/leaderboard")}`}>
            Leaderboard
          </Link>
          <button className="nav-cta">Get Started</button>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;