const API_BASE_URL = "http://localhost:8000/api";

export async function createSession() {
  const response = await fetch(`${API_BASE_URL}/sessions`, {
    method: "POST",
  });

  if (!response.ok) {
    throw new Error("Failed to create session");
  }

  return response.json();
}

export async function sendMessage(sessionId, message) {
  const response = await fetch(`${API_BASE_URL}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      session_id: sessionId,
      message,
    }),
  });

  if (!response.ok) {
    throw new Error("Failed to send message");
  }

  return response.json();
}

export async function getMessages(sessionId) {
  const response = await fetch(
    `${API_BASE_URL}/sessions/${sessionId}/messages`
  );

  if (!response.ok) {
    throw new Error("Failed to load conversation");
  }

  return response.json();
}

export async function getSession(sessionId) {
  const response = await fetch(
    `${API_BASE_URL}/sessions/${sessionId}`
  );

  if (!response.ok) {
    throw new Error("Failed to load session");
  }

  return response.json();
}
