import { useContext, useEffect } from "react";
import { AuthContext } from "../context/AuthContext";
import { getProfile } from "../api/auth";
import { useNavigate } from "react-router-dom";

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
    <div>
      <h1>Welcome to Saarthi 🚀</h1>
      {user && <p>Logged in as: {user.email}</p>}
      <button onClick={logout}>Logout</button>
    </div>
  );
};

export default Dashboard;
