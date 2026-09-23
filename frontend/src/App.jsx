import { useEffect, useState } from "react";

import { createSession, sendMessage, getMessages, getSession } from "./services/api";
import "./index.css";

function App() {
  const [sessionId, setSessionId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [sessionDetails, setSessionDetails] = useState(null);

  useEffect(() => {
    async function initializeSession() {
      try {
        const storedSessionId = localStorage.getItem(
          "acreassistant_session_id"
        );

        if (storedSessionId) {
          try {
            const [history, details] = await Promise.all([
              getMessages(storedSessionId),
              getSession(storedSessionId),
            ]);

            setSessionId(storedSessionId);
            setMessages(history.messages);
            setSessionDetails(details);

            return;
          } catch (error) {
            console.warn(
              "Stored session unavailable. Creating a new session.",
              error
            );

            localStorage.removeItem(
              "acreassistant_session_id"
            );
          }
        }

        const session = await createSession();

        localStorage.setItem(
          "acreassistant_session_id",
          session.session_id
        );

        setSessionId(session.session_id);
        setSessionDetails(session);
      } catch {
        localStorage.removeItem(
          "acreassistant_session_id"
        );

        setError("Unable to load conversation.");
      }
    }

    initializeSession();
  }, []);

  function handleQuickReply(message) {
    setInput(message);
  }

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

      const updatedSession = await getSession(sessionId);

      setSessionDetails(updatedSession);

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

        {sessionDetails?.booking?.status &&
          sessionDetails.booking.status !== "not_requested" && (
            <div className="booking-panel">
              <h3>Site Visit</h3>

              <p>
                <strong>Status:</strong>{" "}
                {sessionDetails.booking.status}
              </p>

              {sessionDetails.booking.preferred_date && (
                <p>
                  <strong>Date:</strong>{" "}
                  {sessionDetails.booking.preferred_date}
                </p>
              )}

              {sessionDetails.booking.preferred_time && (
                <p>
                  <strong>Time:</strong>{" "}
                  {sessionDetails.booking.preferred_time}
                </p>
              )}

              {sessionDetails.booking.booking_id && (
                <p>
                  <strong>Booking ID:</strong>{" "}
                  {sessionDetails.booking.booking_id}
                </p>
              )}

              {sessionDetails.booking.failure_reason && (
                <p className="error">
                  {sessionDetails.booking.failure_reason}
                </p>
              )}
            </div>
          )}

        <div className="quick-replies">
          <p>Quick questions</p>

          <button
            type="button"
            onClick={() => handleQuickReply("What is the starting price of 2 BHK?")}
          >
            2 BHK pricing
          </button>

          <button
            type="button"
            onClick={() => handleQuickReply("What is the starting price of 3 BHK?")}
          >
            3 BHK pricing
          </button>

          <button
            type="button"
            onClick={() => handleQuickReply("I want to schedule a site visit.")}
          >
            Schedule a site visit
          </button>

          <button
            type="button"
            onClick={() => handleQuickReply("I want to talk to a representative.")}
          >
            Talk to a representative
          </button>
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
