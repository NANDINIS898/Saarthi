import React, { useState } from "react";
import axios from "axios";
import "../design/layout.css";

const ChatArea = () => {
  const [messages, setMessages] = useState([
    { sender: "bot", text: "Hello! 👋 I'm Saarthi, your personal loan advisor. How can I help you today?" },
  ]);
  const [input, setInput] = useState("");
  const [sessionId, setSessionId] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadProgress, setUploadProgress] = useState(0);

  const sendMessage = async (messageText) => {
    const textToSend = messageText || input;
    if (!textToSend.trim()) return;

    // Add user message
    const userMessage = { sender: "user", text: textToSend };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    // Call backend
    try {
      const res = await axios.post("http://127.0.0.1:8000/api/chat", {
        message: textToSend,
        session_id: sessionId,
      });

      // Update session ID if new
      if (res.data.session_id && !sessionId) {
        setSessionId(res.data.session_id);
      }

      // Add bot response
      const botResponse = res.data.response || "I'm sorry, I couldn't process that.";
      setMessages((prev) => [...prev, { sender: "bot", text: botResponse }]);

    } catch (err) {
      console.error("Chat error:", err);
      setMessages((prev) => [...prev, {
        sender: "bot",
        text: "I'm having trouble connecting. Please try again."
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      // Check file size (max 10MB)
      if (file.size > 10 * 1024 * 1024) {
        alert("File size must be less than 10MB");
        return;
      }

      // Check file type
      const allowedTypes = ['application/pdf', 'image/jpeg', 'image/jpg', 'image/png'];
      if (!allowedTypes.includes(file.type)) {
        alert("Only PDF, JPG, and PNG files are allowed");
        return;
      }

      setSelectedFile(file);
    }
  };

  const uploadDocument = async () => {
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append('file', selectedFile);

    setIsLoading(true);
    setUploadProgress(0);

    try {
      const res = await axios.post("http://127.0.0.1:8000/api/documents/upload", formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          setUploadProgress(percentCompleted);
        }
      });

      // Add success message
      setMessages((prev) => [...prev, {
        sender: "bot",
        text: `✅ Document "${selectedFile.name}" uploaded successfully! File ID: ${res.data.file_id}`
      }]);

      // Clear selected file
      setSelectedFile(null);
      setUploadProgress(0);

    } catch (err) {
      console.error("Upload error:", err);
      setMessages((prev) => [...prev, {
        sender: "bot",
        text: "❌ Failed to upload document. Please try again."
      }]);
    } finally {
      setIsLoading(false);
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
        {isLoading && (
          <div className="message bot">
            <em>Typing...</em>
          </div>
        )}
      </div>

  

      {/* Document Upload Section */}
      <div className="document-upload-section">
        <label htmlFor="file-upload" className="file-upload-label">
          📎 Upload Document
        </label>
        <input
          id="file-upload"
          type="file"
          accept=".pdf,.jpg,.jpeg,.png"
          onChange={handleFileSelect}
          style={{ display: 'none' }}
        />

        {selectedFile && (
          <div className="file-preview">
            <span className="file-name">📄 {selectedFile.name}</span>
            <span className="file-size">({(selectedFile.size / 1024).toFixed(1)} KB)</span>
            <button
              className="upload-btn"
              onClick={uploadDocument}
              disabled={isLoading}
            >
              {isLoading ? `Uploading... ${uploadProgress}%` : 'Upload'}
            </button>
            <button
              className="cancel-btn"
              onClick={() => setSelectedFile(null)}
              disabled={isLoading}
            >
              ✕
            </button>
          </div>
        )}
      </div>

      <input
        type="text"
        placeholder="Type your message or use voice 🎤"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && !isLoading && sendMessage()}
        disabled={isLoading}
      />
      <button onClick={() => sendMessage()} disabled={isLoading}>
        {isLoading ? "Sending..." : "Send"}
      </button>
    </div>
  );
};

export default ChatArea;
