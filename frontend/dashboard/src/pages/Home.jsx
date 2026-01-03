import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import Header from '../components/Header';
import Footer from '../components/Footer';
import './Home.css';

const Home = () => {
  const [text, setText] = useState('');
  const [llmToken, setLlmToken] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!text.trim()) {
      setError('Please enter some text to analyze');
      return;
    }

    if (!llmToken.trim()) {
      setError('Please enter your LLM Foundry Token');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await axios.post('http://localhost:8000/analyze', {
        text: text,
        llm_token: llmToken
      });

      // Navigate to dashboard with data
      navigate('/dashboard', { state: { data: response.data } });
    } catch (err) {
      setError('Failed to analyze text. Please ensure the backend server is running.');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleExample = () => {
    setText(
      'Heavy rainfall has caused severe flooding in Vellore and Katpadi regions. ' +
      'Multiple residential areas are submerged, and critical infrastructure including ' +
      'roads and bridges have been damaged. Emergency services are on high alert. ' +
      'The meteorological department has issued a red alert for the next 48 hours.'
    );
  };

  return (
    <div className="home-page">
      <Header />
      
      <main className="home-content">
        <div className="hero-section">
          <h2 className="hero-title">Geospatial Risk Intelligence Platform</h2>
          <p className="hero-description">
            Transform unstructured news articles and reports into actionable geospatial intelligence. 
            Our AI-powered platform extracts locations, assesses risks, and provides spatial insights 
            to help you make informed decisions.
          </p>
        </div>

        <div className="input-section">
          <form onSubmit={handleSubmit}>
            <label htmlFor="token-input" className="input-label">
              LLM Foundry Token:
            </label>
            
            <input
              id="token-input"
              type="password"
              className="token-input"
              value={llmToken}
              onChange={(e) => setLlmToken(e.target.value)}
              placeholder="Enter your LLM Foundry Token"
              disabled={loading}
            />

            <label htmlFor="text-input" className="input-label" style={{marginTop: '1.5rem'}}>
              Paste your news article or report below:
            </label>
            
            <textarea
              id="text-input"
              className="text-input"
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Enter or paste text about any event, incident, or report with location information..."
              rows={10}
              disabled={loading}
            />

            {error && <div className="error-message">{error}</div>}

            <div className="button-group">
              <button
                type="button"
                className="example-button"
                onClick={handleExample}
                disabled={loading}
              >
                Try Example
              </button>
              
              <button
                type="submit"
                className="submit-button"
                disabled={loading}
              >
                {loading ? (
                  <>
                    <span className="spinner"></span>
                    Analyzing...
                  </>
                ) : (
                  'Analyze Text'
                )}
              </button>
            </div>
          </form>
        </div>

        <div className="features-section">
          <h3>What you'll get:</h3>
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">🗺️</div>
              <h4>Interactive Map</h4>
              <p>Visualize all locations mentioned in the text</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">⚠️</div>
              <h4>Risk Analysis</h4>
              <p>AI-powered risk classification and severity assessment</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">📊</div>
              <h4>Spatial Insights</h4>
              <p>Geographic patterns and clustering analysis</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">🎯</div>
              <h4>Action Items</h4>
              <p>Recommended actions based on risk analysis</p>
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default Home;
