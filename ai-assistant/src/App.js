import React, { useState } from 'react';
import './App.css';

function App() {
  const [email, setEmail] = useState('');
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    setLoading(true);
    const res = await fetch(`http://localhost:5437/chat?email=${encodeURIComponent(email)}&question=${encodeURIComponent(question)}`);
    const data = await res.json();
    setResponse(data.response);
    setLoading(false);
  };

  return (
    <div className="App">
      <h1>AI Assistant</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Email:
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </label>
        <br />
        <label>
          Question:
          <input type="text" value={question} onChange={(e) => setQuestion(e.target.value)} required />
        </label>
        <br />
        <button type="submit">Ask</button>
      </form>
      {loading ? <div>Loading...</div> : <div className="response">{response}</div>}
    </div>
  );
}

export default App;
