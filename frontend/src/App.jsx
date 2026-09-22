import { useEffect, useState } from "react";

import { createSession, sendMessage, getMessages } from "./services/api";
import "./index.css";


function App() {
  const [sessionId, setSessionId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    async function initializeSession() {
      try {
        const storedSessionId = localStorage.getItem(
          "acreassistant_session_id"
        );

        if (storedSessionId) {
          const history = await getMessages(
            storedSessionId
          );

          setSessionId(storedSessionId);
          setMessages(history.messages);

          return;
        }

        const session = await createSession();

        localStorage.setItem(
          "acreassistant_session_id",
          session.session_id
        );

        setSessionId(session.session_id);
      } catch {
        localStorage.removeItem(
          "acreassistant_session_id"
        );

        setError("Unable to load conversation.");
      }
    }

    initializeSession();
  }, []);

  async function handleSubmit(event) {
    event.preventDefault();

    const trimmedInput = input.trim();

    if (!trimmedInput || !sessionId || isLoading) {
      return;
    }

    const userMessage = {
      role: "user",
      content: trimmedInput,
    };

    setMessages((previous) => [
      ...previous,
      userMessage,
    ]);

    setInput("");
    setIsLoading(true);
    setError("");

    try {
      const response = await sendMessage(
        sessionId,
        trimmedInput
      );

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: response.reply,
        },
      ]);
    } catch {
      setError("Unable to send message. Please try again.");
    } finally {
      setIsLoading(false);
    }
  }

  function resetConversation() {
    localStorage.removeItem(
      "acreassistant_session_id"
    );

    setSessionId(null);
    setMessages([]);
    setError("");

    window.location.reload();
  }

  return (
    <div className="app">
      <header className="header">
        <div>
          <h1>AcreAssistant</h1>
          <p>Northstar Homes · Northstar One</p>
        </div>

        <div className="header-actions">
          <span className="status">AI Assistant</span>

          <button
            className="reset-button"
            onClick={resetConversation}
          >
            New chat
          </button>
        </div>
      </header>

      <main className="chat-container">
        <div className="welcome">
          <h2>Welcome to Northstar Homes</h2>
          <p>
            Ask me about Northstar One in Sector 79,
            Gurugram.
          </p>
        </div>

        <div className="messages">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`message ${message.role}`}
            >
              {message.content}
            </div>
          ))}

          {isLoading && (
            <div className="message assistant">
              Thinking...
            </div>
          )}
        </div>

        {error && (
          <p className="error">{error}</p>
        )}

        <form
          className="input-form"
          onSubmit={handleSubmit}
        >
          <input
            type="text"
            placeholder="Ask about Northstar One..."
            value={input}
            onChange={(event) => setInput(event.target.value)}
            disabled={!sessionId || isLoading}
          />

          <button
            type="submit"
            disabled={!sessionId || isLoading || !input.trim()}
          >
            Send
          </button>
        </form>
      </main>
    </div>
  );
}

export default App;
