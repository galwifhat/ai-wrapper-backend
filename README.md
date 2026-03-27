backend-promt-toolkit/
├── app/
│ ├── **init**.py # App factory (create_app)
│ ├── config.py # Config classes (Dev, Prod, Test)
│ ├── extensions.py # Flask extensions (CORS, SQLAlchemy etc.)
│ │
│ ├── api/ # All route blueprints
│ │ ├── **init**.py
│ │ ├── v1/
│ │ │ ├── **init**.py
│ │ │ ├── journal_routes.py # /api/v1/journal endpoints
│ │ │ ├── ai.py # /api/v1/ai endpoints
│ │ │ └── auth.py # /api/v1/auth endpoints
│ │
│ ├── services/ # Business logic layer
│ │ ├── **init**.py
│ │ ├── openrouter/
│ │ │ ├── **init**.py
│ │ │ ├── client.py # OpenRouter HTTP client / wrapper
│ │ │ ├── prompts.py # Prompt templates
│ │ │ └── stream.py # SSE streaming handler
│ │ ├── journal_service.py
│ │ └── auth_service.py
│ │
│ ├── models/ # DB models (SQLAlchemy etc.)
│ │ ├── **init**.py
│ │ ├── user.py
│ │ └── journal.py
│ │
│ ├── schemas/ # Request/response validation (Marshmallow/Pydantic)
│ │ ├── **init**.py
│ │ ├── journal_schema.py
│ │ └── ai_schema.py
│ │
│ └── utils/
│ ├── **init**.py
│ ├── helpers.py
│ ├── errors.py # Custom exception classes
│ └── decorators.py # Auth guards, rate limiters
│
├── tests/
│ ├── conftest.py
│ ├── test_journal.py
│ └── test_openrouter.py
│
├── .env # Never commit this
├── .env.example # Commit this as a template
├── requirements.txt
├── run.py # Entry point
└── wsgi.py # Production WSGI entry
