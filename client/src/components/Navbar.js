import { Link } from "react-router-dom";

const Navbar = () => {
  return (
    <nav style={{ padding: "10px", background: "#f0f0f0" }}>
      <Link to="/" style={{ marginRight: "10px" }}>Login</Link>
      <Link to="/signup" style={{ marginRight: "10px" }}>Signup</Link>
      <Link to="/dashboard">Dashboard</Link>
    </nav>
  );
};

export default Navbar;
