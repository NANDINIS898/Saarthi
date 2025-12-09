import React, { useState } from "react";
import axios from "axios";
import "../design/layout.css";

const ChatArea = () => {
  const [messages, setMessages] = useState([
    { sender: "bot", text: "Hello! How can I help you with your loan today?" },
  ]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (!input.trim()) return;

    // Add user message
    setMessages([...messages, { sender: "user", text: input }]);
    const userInput = input;
    setInput("");

    // Call backend
    try {
      const res = await axios.post("http://127.0.0.1:3000/api/chat", {
        message: userInput,
      });
      setMessages((prev) => [...prev, { sender: "bot", text: res.data.response }]);
    } catch (err) {
      setMessages((prev) => [...prev, { sender: "bot", text: "Error contacting server." }]);
    }
  };

  return (
    <div className="chat-area">
      <h2>Saarthi</h2>
      <div className="chat-box">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.sender}`}>
            {msg.text}
          </div>
        ))}
      </div>
      <input
        type="text"
        placeholder="Type your message..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && sendMessage()}
      />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
};

export default ChatArea;
