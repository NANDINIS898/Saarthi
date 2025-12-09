import React from "react";
import profilePic from "./profile.png";
import "./navbarvertical.css";

const NavbarVertical = () => {
  return (
    <aside className="navbar-vertical">
      <div className="profile-section">
        <img
          src={profilePic}
          alt="Profile"
          className="profile-pic"
        />
        <h3 className="profile-name">Nandini Singh</h3>
        
      </div>

      <ul className="nav-list">
        <li className="nav-item">Profile</li>
        <li className="nav-item">Documents</li>
        <li className="nav-item">Applications</li>
        <li className="nav-item">Loan Assistant</li>
        <li className="nav-item">More Options</li>
      </ul>
    </aside>
  );
};

export default NavbarVertical;

