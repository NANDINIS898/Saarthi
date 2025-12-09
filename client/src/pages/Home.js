import { useState, useEffect } from "react";
import Login from "./Login";
import Signup from "./Signup";
import "./home.css";

const Home = () => {
  const [showLogin, setShowLogin] = useState(true);
  const [taglineIndex, setTaglineIndex] = useState(0);
  const taglines = [
    "The end of frustration & Begining of Trust",
    "Your 24/7 Loan AI Assistant"
  ];

  // Change tagline every 3 seconds
  useEffect(() => {
    const timer = setInterval(() => {
      setTaglineIndex((prev) => (prev + 1) % taglines.length);
    }, 3000);
    return () => clearInterval(timer);
  }, []);

  const switchToSignup = () => setShowLogin(false);
  const switchToLogin = () => setShowLogin(true);
  
  return (
    <div className="home-container">
      
      {/* LEFT SIDE ANIMATION */}
      <div className="left-section">
      <div className="saarthi-animation">SAARTHI</div>

      <p key={taglineIndex} className="tagline fade">
          {taglines[taglineIndex]}
        </p>
      </div>


      {/* RIGHT SIDE LOGIN/SIGNUP BOX */}
      <div className="right-section">
        <div className="toggle-buttons">
          <button 
            className={showLogin ? "active" : ""} 
            onClick={() => setShowLogin(true)}
          >
            Login
          </button>

          <button 
            className={!showLogin ? "active" : ""} 
            onClick={() => setShowLogin(false)}
          >
            Signup
          </button>
        </div>

        <div className="form-box">
          {showLogin ? <Login /> : <Signup />}
        </div>
      </div>

    </div>
  );
};

export default Home;
