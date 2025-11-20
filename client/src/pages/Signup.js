import { useState } from "react";
import { signupUser } from "../api/auth";
import { useNavigate } from "react-router-dom";

const Signup = () => {
  const [form, setForm] = useState({ email: "", password: "" });
  const navigate = useNavigate();

  const handleSignup = async (e) => {
    e.preventDefault();

    try {
      await signupUser(form);
      alert("Signup successful! Please login.");
      navigate("/dashboard");
    } catch (err) {
      alert("Signup failed");
    }
  };

  return (
    <div className="form-container">
      <h2>Create Account</h2>

      <form onSubmit={handleSignup}>
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

        <button type="submit">Signup</button>
      </form>
    </div>
  );
};

export default Signup;
