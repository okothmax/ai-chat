# AI Q&A Interview Project

A modern, full-stack AI-powered Q&A web application built with **FastAPI** and **Next.js**. This project demonstrates professional-grade software development practices, clean architecture, and modern UI/UX design.

## 🚀 Live Demo

// TODO : Add deployed URL

## 📋 Project Overview

This application showcases:

- **Backend Excellence**: FastAPI with proper API design, error handling, and documentation
- **Frontend Mastery**: Next.js with modern React patterns and responsive design
- **AI Integration**: Multiple LLM providers with advanced prompt engineering
- **Professional Code**: Clean architecture, TypeScript, and comprehensive documentation

## 🏗️ Architecture

```
ai-qa-interview-project/
├── backend/                 # FastAPI Backend
│   ├── app/
│   │   ├── routers/        # API endpoints
│   │   ├── models/         # Data models
│   │   ├── services/       # Business logic
│   │   └── config.py       # Configuration
│   ├── main.py             # Application entry point
│   └── requirements.txt    # Python dependencies
├── frontend/               # Next.js Frontend
│   ├── src/
│   │   ├── app/           # App router pages
│   │   ├── components/    # React components
│   │   └── types/         # TypeScript types
│   └── package.json       # Node dependencies
└── docs/                  # Documentation
```

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - Database ORM
- **Pydantic** - Data validation
- **OpenAI/Anthropic APIs** - LLM integration
- **SQLite** - Database (easily replaceable)

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first styling
- **Responsive Design** - Mobile-first approach

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 18+
- npm or yarn

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.template .env
   # Edit .env with your API keys
   ```

5. **Start the server**
   ```bash
   python main.py
   ```

The API will be available at `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/api/v1/health`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```

The application will be available at `http://localhost:3000`

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# CORS Settings
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# LLM API Keys
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Default LLM Provider (openai or anthropic)
DEFAULT_LLM_PROVIDER=openai

# Database
DATABASE_URL=sqlite:///./qa_history.db

# Security
SECRET_KEY=your_secret_key_here_change_in_production
```

## 📚 API Documentation

### Endpoints

- `GET /` - Root endpoint with API information
- `GET /api/v1/health` - Health check
- `POST /api/v1/ask` - Ask a question to the AI
- `GET /api/v1/history` - Get query history
- `GET /api/v1/providers` - Get available LLM providers
- `GET /api/v1/stats` - Get usage statistics

### Example Request

```bash
curl -X POST "http://localhost:8000/api/v1/ask" \
     -H "Content-Type: application/json" \
     -d '{
       "question": "What is machine learning?",
       "context": "I am a beginner in AI"
     }'
```

## 🎨 Features

### Core Features
- ✅ **AI-Powered Q&A** - Ask questions and get comprehensive answers
- ✅ **Multiple LLM Providers** - Support for OpenAI and Anthropic
- ✅ **Query History** - Track and revisit previous questions
- ✅ **Real-time Responses** - Live response streaming
- ✅ **Responsive Design** - Works on all devices
- ✅ **Dark Mode** - Toggle between light and dark themes

### Technical Features
- ✅ **Input Validation** - Comprehensive request validation
- ✅ **Error Handling** - Graceful error management
- ✅ **API Documentation** - Auto-generated Swagger docs
- ✅ **Type Safety** - Full TypeScript implementation
- ✅ **Performance Monitoring** - Response time tracking
- ✅ **Usage Statistics** - API usage analytics

## 🧠 Prompt Engineering

This project demonstrates advanced prompt engineering techniques:

### System Prompts
- **Structured Instructions** - Clear role definition and capabilities
- **Response Guidelines** - Formatting and tone specifications
- **Context Awareness** - Adaptive responses based on user context

### User Prompts
- **Context Integration** - Optional context for better responses
- **Question Enhancement** - Automatic question clarification
- **Response Optimization** - Tailored for different use cases

See [docs/PROMPT_ENGINEERING.md](docs/PROMPT_ENGINEERING.md) for detailed documentation.

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 🚀 Deployment

### Backend Deployment
- **Docker**: Containerized deployment ready
- **Cloud Platforms**: Compatible with AWS, GCP, Azure
- **Environment**: Production-ready configuration

### Frontend Deployment
- **Vercel**: Optimized for Next.js deployment
- **Netlify**: Static site deployment
- **Docker**: Containerized deployment

## 📊 Performance

- **Response Time**: < 2s average for most queries
- **Concurrent Users**: Supports 100+ concurrent requests
- **Database**: Optimized queries with indexing
- **Caching**: Response caching for improved performance

## 🔒 Security

- **Input Validation**: Comprehensive request validation
- **CORS Configuration**: Proper cross-origin setup
- **Environment Variables**: Secure configuration management
- **Error Handling**: No sensitive data exposure

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Max Okoth**
- Cloud Architect | DevOps Engineer | AI & Software Engineer | Data & Analytics Specialist
- GitHub: [@okothmax](https://github.com/okothmax)
- LinkedIn: [Max Okoth](https://linkedin.com/in/okothmax)

## 🙏 Acknowledgments

- OpenAI for GPT models
- Anthropic for Claude models
- FastAPI community
- Next.js team
- Tailwind CSS team

---

