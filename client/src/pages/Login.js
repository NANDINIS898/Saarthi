import { useState, useContext } from "react";
import { loginUser } from "../api/auth";
import { AuthContext } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

const Login = () => {
  const { setToken } = useContext(AuthContext);
  const navigate = useNavigate();

  const [form, setForm] = useState({ email: "", password: "" });

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const res = await loginUser(form);
      setToken(res.data.token);
      navigate("/dashboard");
    } catch (err) {
      alert("Invalid credentials");
    }
  };

  return (
    <div className="form-container">
      <h2>Saarthi Login</h2>

      <form onSubmit={handleLogin}>
        <input
          type="email"
          placeholder="Email"
          value={form.email}
          onChange={(e) => setForm({ ...form, email: e.target.value })}
        />

        <input
          type="password"
          placeholder="Password"
          value={form.password}
          onChange={(e) => setForm({ ...form, password: e.target.value })}
        />

        <button type="submit">Login</button>
      </form>

      <p onClick={() => navigate("/signup")} className="link">
        Don't have an account? Signup
      </p>
    </div>
  );
};

export default Login;
