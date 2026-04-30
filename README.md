# AI Tutor Chatbot

An intelligent AI-powered tutoring chatbot specialized in Artificial Intelligence, Machine Learning, Deep Learning, and related technologies. The chatbot uses Retrieval-Augmented Generation (RAG) with LangChain, Qdrant vector database, and Google's Gemini API.

## Features

- 🤖 **AI-Powered Teaching**: Specialized in AI, ML, Deep Learning, and technology concepts
- 📚 **Context-Aware Responses**: Uses RAG to fetch relevant information from knowledge base
- 🔄 **Conversational Memory**: Maintains chat history for coherent multi-turn conversations
- 🎨 **Interactive UI**: Built with Streamlit for an intuitive user experience
- 🔐 **Secure API Integration**: Supports multiple LLM providers (Gemini, Groq, DeepSeek)

## Prerequisites

- Python 3.13 or higher
- API Keys for:
  - [Google Gemini API](https://ai.google.dev/)
  - [Qdrant Cloud](https://cloud.qdrant.io/)

## Installation

### 1. Clone and Setup
```bash
# Navigate to project directory
cd Sun-Marke

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the project root with the following credentials:

```env
# Google Gemini API Key
GEMINI_API_KEY=your_gemini_api_key_here

# Qdrant Cloud Configuration
QDRANT_URL=your_qdrant_cloud_url
QDRANT_API_KEY=your_qdrant_api_key

# Optional: For other LLM providers
GROQ_API_KEY=your_groq_api_key_here
DEEPSEEK_API_KEY=your_deepseek_api_key_here
```

**⚠️ Important**: Never commit the `.env` file to version control. Add it to `.gitignore`.

## Running the Application

### Start the Chatbot

```bash
streamlit run main.py
```

The application will open in your default browser at `http://localhost:8501`

### First Run

On the first run, the chatbot will:
1. Scrape AI-related content from the configured URL
2. Split the content into chunks for better retrieval
3. Store embeddings in the Qdrant vector database
4. Initialize the knowledge base

Subsequent runs will use the existing knowledge base for faster startup.

## How to Use

1. **Start a Conversation**: Type your question in the chat input box
2. **Ask Follow-ups**: The chatbot remembers previous messages in the conversation
3. **Get Explanations**: Responses are structured and beginner-friendly, with deeper details available

### Example Questions

- "What is a neural network?"
- "Explain the concept of overfitting in machine learning"
- "What are the differences between supervised and unsupervised learning?"

## Project Structure

```
Sun-Marke/
├── main.py                 # Main application entry point
├── scrape.py              # Web scraping module for data collection
├── requirements.txt       # Python dependencies
├── pyproject.toml         # Project configuration
├── .env                   # Environment variables (not in repo)
├── README.md              # This file
└── testing.ipynb          # Jupyter notebook for testing/development
```

## Configuration

### Embedding Model
Currently uses **Google's Gemini Embedding Model 2 Preview** for high-quality semantic embeddings.

### LLM (Language Model)
Currently uses **Gemini 2.5 Flash** for response generation with temperature set to 0 for deterministic answers.

### Vector Database
- **Qdrant Cloud** for scalable vector storage
- Collection name: `AI_DATA`
- Search type: Similarity search with top-5 results

### Data Processing
- **Chunk size**: 1000 tokens
- **Chunk overlap**: 100 tokens (for context continuity)
- **Splitter**: Recursive Character Text Splitter

## Troubleshooting

### Issue: "Connection refused to Qdrant"
- Verify `QDRANT_URL` and `QDRANT_API_KEY` in `.env`
- Check internet connectivity
- Ensure your IP is whitelisted in Qdrant Cloud

### Issue: "API key not found"
- Ensure `.env` file exists in the project root
- Verify all required API keys are set
- Restart Streamlit after updating `.env`

### Issue: "Module not found" errors
- Run: `pip install -r requirements.txt`
- Verify Python version is 3.13 or higher: `python --version`

### Issue: Slow response times
- First run takes longer due to data scraping and embedding generation
- Subsequent responses are faster as data is cached
- Check your internet connection speed

## Performance Notes

- **Startup Time**: ~30-60 seconds (first run), ~5-10 seconds (subsequent runs)
- **Response Time**: 5-15 seconds depending on question complexity and API latency
- **Knowledge Base Size**: Grows with added documents

## Development

To modify or extend the chatbot:

1. **Adjust System Prompt**: Edit `qa_prompt` in `main.py` to change teaching style
2. **Change LLM Model**: Uncomment alternative providers in `main.py` (Groq, DeepSeek)
3. **Add More Data Sources**: Modify `scrape.py` to include additional URLs
4. **Tune Embedding Settings**: Adjust `chunk_size` and `chunk_overlap` for different granularity

## API Rate Limits

- **Gemini API**: Free tier has rate limits; consider upgrading for production use
- **Qdrant Cloud**: Free tier with sufficient quotas for development
- Monitor API usage in respective dashboards

## Future Enhancements

- [ ] Multi-language support
- [ ] Document upload feature
- [ ] Export conversation history
- [ ] User authentication and profiles
- [ ] Analytics dashboard

## Support

For issues or questions:
1. Review error messages in the Streamlit terminal
2. Verify all environment variables are correctly set

---

**Happy Learning! 🚀**
