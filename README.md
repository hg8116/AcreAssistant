# AcreAssistant

AI-powered conversational sales assistant for Northstar Homes.

AcreAssistant is a full-stack real-estate sales assistant built as an assignment project. It uses FastAPI for the backend, React + Vite for the frontend, and an OpenRouter-compatible LLM for natural-language conversations.

## Project

### Developer
Northstar Homes

### Project
Northstar One

### Location
Sector 79, Gurugram

### Configurations

| Configuration | Starting Price |
|---|---|
| 2 BHK | ₹1.35 crore onwards |
| 3 BHK | ₹1.75 crore onwards |

The application intentionally does not invent project information that is not available in the configured project data.

---

# Features

- Natural conversational interaction
- English, Hindi and Hinglish support
- Project information queries
- Requirement gathering
- Lead qualification
- Intent detection
- Conversation state management
- Site visit scheduling
- Booking confirmation and failure handling
- Follow-up handling
- Human escalation
- Communication opt-out
- Conversation analytics
- Persistent frontend session ID
- Conversation history restoration
- Responsive React chat interface
- Quick replies
- Loading and error states

---

# Architecture

```text
                         ┌──────────────────────┐
                         │      React UI        │
                         │      Vite            │
                         └──────────┬───────────┘
                                    │
                                    │ HTTP / JSON
                                    ▼
                         ┌──────────────────────┐
                         │      FastAPI         │
                         │       API            │
                         └──────────┬───────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
                    ▼               ▼               ▼
             Conversation       Agent/LLM       Booking
               Service           Service         Service
                    │               │               │
                    │               ▼               │
                    │        OpenRouter LLM         │
                    │                               │
                    └───────────────┬───────────────┘
                                    │
                                    ▼
                              Analytics



Tech Stack
Backend
Python
FastAPI
Pydantic
OpenRouter
OpenAI-compatible Python client
Frontend
React
Vite
JavaScript
CSS
Testing
pytest
FastAPI TestClient



Backend Setup
1. Create virtual environment

From the repository root:

cd backend

python -m venv .venv
source .venv/bin/activate
2. Install dependencies
pip install -r ../requirements.txt
3. Configure environment variables

Create:

.env

The environment file should contain:

OPENROUTER_API_KEY=your_api_key
OPENROUTER_MODEL=openrouter/free

Do not commit .env to Git.

Run Backend

From backend/:

source .venv/bin/activate
fastapi dev app/main.py

Backend:

http://localhost:8000

Swagger documentation:

http://localhost:8000/docs
Run Frontend

Open another terminal:

cd frontend
npm install
npm run dev

The Vite development server will display the frontend URL.

API Endpoints
Health
GET /health

Checks whether the API is running.

Create Session
POST /api/sessions

Creates a new conversation session.

Send Message
POST /api/chat

Example:

{
  "session_id": "session-id",
  "message": "I am looking for a 3 BHK"
}
Get Session
GET /api/sessions/{session_id}

Returns the current conversation state.

Get Messages
GET /api/sessions/{session_id}/messages

Returns conversation history.

Analytics
GET /api/sessions/{session_id}/analytics

Returns conversation-level analytics.

Book Site Visit
POST /api/bookings

Creates a simulated site visit booking.

Conversation Flow
User
 │
 ▼
Send message
 │
 ▼
FastAPI /api/chat
 │
 ├── Store user message
 │
 ├── Generate assistant response
 │
 ├── Extract lead information
 │
 ├── Detect intent
 │
 └── Update conversation state
 │
 ▼
Return assistant response
Site Visit Flow
Customer expresses interest
            │
            ▼
Collect name
            │
            ▼
Collect phone
            │
            ▼
Collect preferred date
            │
            ▼
Collect preferred time
            │
            ▼
Confirm booking details
            │
            ▼
BookingService
       ┌────┴────┐
       │         │
    Success    Failure
       │         │
       ▼         ▼
  CONFIRMED    FAILED

The booking service is currently a simulated in-memory implementation and does not connect to a real calendar or CRM.

Lead Qualification

The application can track:

Name
Phone
Configuration
Budget
Buying purpose
Purchase timeline
Interest level
Follow-up requirement
Follow-up preference
Human escalation
Communication opt-out
Site visit details
Current intent
Intent Categories

The application supports intents including:

general_inquiry
project_information
requirement
price_inquiry
objection
site_visit
follow_up
busy
not_interested
opt_out
human_escalation
unknown
Analytics

Analytics currently provides:

Total messages
User messages
Assistant messages
Detected intents
Configuration
Budget
Buying purpose
Purchase timeline
Interest level
Site visit status
Follow-up requirement
Human escalation
Communication opt-out
Conversation outcome

Possible outcomes include:

ongoing
qualified_lead
site_visit_confirmed
follow_up_required
human_escalation
not_interested
opted_out
incomplete
Testing

Run backend tests from the repository root:

pytest -v

Compile-check the Python application:

python -m compileall backend/app tests

Build the frontend:

cd frontend
npm run build

Vite's production build generates the frontend bundle in dist/.


Current Limitations
Conversation state is stored in memory.
Restarting the backend clears active sessions.
Site visit booking is simulated.
No real CRM/calendar integration.
No authentication.
No production database.
OpenRouter free-model routing can vary by availability.
Frontend currently uses the local backend API URL.
No real voice interface is implemented yet.
Future Improvements

Potential production extensions include:

PostgreSQL or another persistent database
Redis for session/cache management
Authentication
Real CRM integration
Real calendar integration
WhatsApp integration
Voice interface
Agent observability
Structured conversation summaries
Better qualification scoring
Production deployment
Automated CI/CD
Persistent analytics storage
Design Principles

AcreAssistant prioritizes:

Accurate project information
Natural conversation
Customer intent
Transparent handling of unknown information
No fabricated pricing, discounts or availability
Respect for customers who are busy or uninterested
Explicit confirmation before site-visit booking
Clear handling of booking failures
Human escalation when appropriate

The system is designed to assist customers rather than pressure them into a conversion.
