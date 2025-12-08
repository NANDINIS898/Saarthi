import React from "react";
import "../design/layout.css";

const ChatArea = () => {
  return (
    <div className="chat-area">
      <h2>Saarthi</h2>
      <div className="chat-box">
        <div className="message bot">Hello! How can I help you with your loan today?</div>
        {/* Messages will go here dynamically */}
      </div>
      <input type="text" placeholder="Type your message..." />
    </div>
  );
};

export default ChatArea;
