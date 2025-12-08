import React from "react";
import "./navbarhorizontal.css";

const NavbarHorizontal = () => {
  return (
    <nav className="navbar-horizontal">
      
      <div className="nav-items">
        <a href="/">Home</a>
        <a href="/dashboard">Dashboard</a>
        
        <a href="/logout">Logout</a>
      </div>
    </nav>
  );
};

export default NavbarHorizontal;

