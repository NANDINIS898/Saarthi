import { useState } from "react";
import { signupUser } from "../api/auth";
import { useNavigate } from "react-router-dom";

const Signup = () => {
  const [form, setForm] = useState({ name: "", email: "", password: "" });
  const navigate = useNavigate();

  const handleSignup = async (e) => {
    e.preventDefault();

    try {
      const response = await signupUser(form);
      if (response.status === 200 || response.status === 201) {
        alert("Signup successful! Please login.");
        navigate("/dashboard");
      }
    } catch (err) {
      console.log(err);
      alert(err.response?.data?.detail || "Signup failed");
    }
  };

  return (
    <div className="form-container">
      <h2>Create Account</h2>
      <form onSubmit={handleSignup}>
        <input
          type="text"
          placeholder="Full Name"
          value={form.name}
          onChange={(e) => setForm({ ...form, name: e.target.value })}
        />

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
        onChange={(e) => {
          if (e.target.value.length <= 72) {
            setForm({ ...form, password: e.target.value });
          }
        }}
        />


        <button type="submit">Signup</button>
      </form>
    </div>
  );
};

export default Signup;
