import { useContext, useEffect } from "react";
import { AuthContext } from "../context/AuthContext";
import { getProfile } from "../api/auth";
import { useNavigate } from "react-router-dom";
import NavbarHorizontal from "../components/Navbarhorizontal";
import NavbarVertical from "../components/Navbarvertical";
import ChatArea from "../components/chatarea";
import LoanStatus from "../components/LoanStatus";
import "./dashboard.css";
import "../design/layout.css";

const Dashboard = () => {
  const { token, user, setUser, logout } = useContext(AuthContext);
  const navigate = useNavigate();

  useEffect(() => {
    if (!token) {
      navigate("/");
      return;
    }

    const fetchUser = async () => {
      try {
        const res = await getProfile(token);
        setUser(res.data);
      } catch (err) {
        logout();
        navigate("/");
      }
    };

    fetchUser();
  }, [token]);

  return (
    <div className="dashboard-container">
      

      <div className="dashboard-body">
        <div className="loan-status"><LoanStatus /></div>
        <div className="chat-area"><ChatArea /></div>
        <div className="navbar-vertical"><NavbarVertical /></div>
      </div>
        

    </div>
  );
};

export default Dashboard;
