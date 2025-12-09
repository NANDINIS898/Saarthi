import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Dashboard from "./pages/Dashboard";
import Navbar from "./components/Navbarhorizontal";
import Navbarvertical from "./components/Navbarvertical";

console.log("DEBUG:", { Home, Login, Signup, Dashboard, Navbar , Navbarvertical});

const App = () => {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/dashboard" element={<Dashboard />} />
          
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
};

export default App;
