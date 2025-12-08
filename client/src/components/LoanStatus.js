import React from "react";
import "../design/layout.css";

const LoanStatus = () => {
  return (
    <div className="loan-status">
      <h2>Your Loan Applications</h2>
      <ul>
        <li>Application #123 - Pending</li>
        <li>Application #124 - Approved</li>
        <li>Application #125 - Rejected</li>
      </ul>
    </div>
  );
};

export default LoanStatus;
