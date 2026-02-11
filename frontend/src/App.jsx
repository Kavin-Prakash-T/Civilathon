import { useState, useEffect } from 'react';
import { analyzeSuitability, generateReport } from './api';
import { FlaskConical, BookOpen, Info, Download, LogOut, FileText, Microscope, ClipboardList, Beaker, CheckCircle, AlertTriangle, Lightbulb, BarChart3, Construction } from 'lucide-react';
import Disclaimer from './Disclaimer';
import About from './About';
import Guide from './Guide';
import Login from './Login';
import Register from './Register';
import Reports from './Reports';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('analyze');
  const [suitabilityResult, setSuitabilityResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [user, setUser] = useState(null);
  const [authView, setAuthView] = useState('login');

  useEffect(() => {
    const token = localStorage.getItem('token');
    const savedUser = localStorage.getItem('user');
    if (token && savedUser) {
      setUser(JSON.parse(savedUser));
    }
  }, []);

  const handleLogin = (userData) => {
    setUser(userData);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
  };

  const [manualInput, setManualInput] = useState({
    'LL': '',
    'PL': '',
    'PI': '',
    'G': '',
    'CS': '',
    'MS': '',
    'FS': '',
    'F': '',
    'OMC%': '',
    'MDD (kN/m3)': '',
    'NMC (%)': ''
  });

  const fieldLabels = {
    'LL': 'Liquid Limit (%)',
    'PL': 'Plastic Limit (%)',
    'PI': 'Plasticity Index',
    'G': 'Gravel Content (%)',
    'CS': 'Coarse Sand (%)',
    'MS': 'Medium Sand (%)',
    'FS': 'Fine Sand (%)',
    'F': 'Fines Content (%)',
    'OMC%': 'Optimum Moisture Content (%)',
    'MDD (kN/m3)': 'Maximum Dry Density (kN/m³)',
    'NMC (%)': 'Natural Moisture Content (%)'
  };

  const handleAnalyze = async () => {
    const data = {};
    Object.keys(manualInput).forEach(key => {
      if (manualInput[key] !== '') {
        data[key] = parseFloat(manualInput[key]);
      }
    });
    
    setLoading(true);
    try {
      const res = await analyzeSuitability({ soil_data: data });
      setSuitabilityResult(res.data);
    } catch (error) {
      alert('Analysis failed: ' + (error.response?.data?.error || error.message));
    }
    setLoading(false);
  };

  const handleDownloadReport = async () => {
    if (!suitabilityResult) {
      alert('Please analyze soil data first');
      return;
    }
    
    setLoading(true);
    try {
      const res = await generateReport({ result: suitabilityResult });
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `soil_report_${Date.now()}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      alert('Report generation failed: ' + (error.response?.data?.error || error.message));
    }
    setLoading(false);
  };

  return (
    <div className="app">
      {!user ? (
        authView === 'login' ? (
          <Login onLogin={handleLogin} onSwitchToRegister={() => setAuthView('register')} />
        ) : (
          <Register onSwitchToLogin={() => setAuthView('login')} />
        )
      ) : (
        <>
      <header>
        <div className="header-content">
          <div>
            <h1><Construction size={28} style={{display: 'inline', marginRight: '8px', verticalAlign: 'middle'}} /> Soil Suitability Analysis for Construction</h1>
            <p className="subtitle">Professional geotechnical assessment platform</p>
          </div>
          <div className="user-info">
            <span>Welcome, {user.name}</span>
            <button onClick={handleLogout} className="logout-btn">
              <LogOut size={18} /> Logout
            </button>
          </div>
        </div>
        <nav className="nav-tabs">
          <button 
            className={activeTab === 'analyze' ? 'active' : ''} 
            onClick={() => setActiveTab('analyze')}
          >
            <FlaskConical size={18} /> Analyze
          </button>
          <button 
            className={activeTab === 'reports' ? 'active' : ''} 
            onClick={() => setActiveTab('reports')}
          >
            <FileText size={18} /> Reports
          </button>
          <button 
            className={activeTab === 'guide' ? 'active' : ''} 
            onClick={() => setActiveTab('guide')}
          >
            <BookOpen size={18} /> Guide
          </button>
          <button 
            className={activeTab === 'about' ? 'active' : ''} 
            onClick={() => setActiveTab('about')}
          >
            <Info size={18} /> About
          </button>
        </nav>
      </header>

      <main>
        <Disclaimer />
        {loading && <div className="loading">Processing...</div>}

        {activeTab === 'analyze' && (
          <div className="section">
          <h2>Soil Parameter Input</h2>
          <p>Enter soil test data from laboratory investigation reports</p>
          <div className="manual-form">
            {Object.keys(manualInput).map(key => (
              <label key={key}>
                {fieldLabels[key]}:
                <input 
                  type="number"
                  step="0.01"
                  value={manualInput[key]}
                  onChange={(e) => setManualInput({...manualInput, [key]: e.target.value})}
                  placeholder={`Enter ${fieldLabels[key]}`}
                />
              </label>
            ))}
            <button onClick={handleAnalyze} disabled={loading} className="analyze-btn">
              {loading ? 'Analyzing...' : 'Analyze Suitability'}
            </button>
          </div>

          {suitabilityResult && (
            <div className={`result-card ${suitabilityResult.suitability === 'SUITABLE' ? 'suitable' : suitabilityResult.suitability === 'MODERATELY SUITABLE' ? 'moderate' : 'not-suitable'}`}>
              <h3><Microscope size={20} style={{display: 'inline', marginRight: '8px', verticalAlign: 'middle'}} /> Geotechnical Analysis Report</h3>
              
              <div className="result-section">
                <h4><ClipboardList size={18} style={{display: 'inline', marginRight: '8px', verticalAlign: 'middle'}} /> Soil Classification</h4>
                <div className="classification-box">{suitabilityResult.classification}</div>
              </div>

              <div className="result-section">
                <h4><Beaker size={18} style={{display: 'inline', marginRight: '8px', verticalAlign: 'middle'}} /> Soil Behavior</h4>
                <ul>
                  {suitabilityResult.behavior.map((item, i) => (
                    <li key={i}>{item}</li>
                  ))}
                </ul>
              </div>

              <div className="result-section">
                <h4><CheckCircle size={18} style={{display: 'inline', marginRight: '8px', verticalAlign: 'middle'}} /> Suitability Assessment</h4>
                <div className="result-status">
                  {suitabilityResult.suitability === 'SUITABLE' ? <CheckCircle size={24} style={{display: 'inline', marginRight: '8px', verticalAlign: 'middle', color: 'inherit'}} /> : 
                   suitabilityResult.suitability === 'MODERATELY SUITABLE' ? <AlertTriangle size={24} style={{display: 'inline', marginRight: '8px', verticalAlign: 'middle', color: 'inherit'}} /> : <AlertTriangle size={24} style={{display: 'inline', marginRight: '8px', verticalAlign: 'middle', color: 'inherit'}} />} 
                  {suitabilityResult.suitability}
                </div>
                <p className="suitability-text">{suitabilityResult.suitability_text}</p>
              </div>

              <div className="result-section">
                <h4><AlertTriangle size={18} style={{display: 'inline', marginRight: '8px', verticalAlign: 'middle'}} /> Construction Risks</h4>
                <ul className="risks-list">
                  {suitabilityResult.risks.map((risk, i) => (
                    <li key={i}>{risk}</li>
                  ))}
                </ul>
              </div>

              <div className="result-section">
                <h4><Lightbulb size={18} style={{display: 'inline', marginRight: '8px', verticalAlign: 'middle'}} /> Recommendations</h4>
                <ul className="recommendations-list">
                  {suitabilityResult.recommendations.map((rec, i) => (
                    <li key={i}>{rec}</li>
                  ))}
                </ul>
              </div>

              <div className="result-section">
                <h4><BarChart3 size={18} style={{display: 'inline', marginRight: '8px', verticalAlign: 'middle'}} /> Input Parameters</h4>
                <div className="parameters-grid">
                  {Object.entries(suitabilityResult.parameters).map(([key, value]) => (
                    <div key={key} className="param-item">
                      <strong>{key}:</strong> {value}
                    </div>
                  ))}
                </div>
              </div>

              <div className="report-actions">
                <button onClick={handleDownloadReport} className="download-btn" disabled={loading}>
                  <Download size={20} />
                  {loading ? 'Generating...' : 'Download PDF Report'}
                </button>
              </div>
            </div>
          )}
        </div>
        )}

        {activeTab === 'reports' && <Reports />}
        {activeTab === 'guide' && <Guide />}
        {activeTab === 'about' && <About />}
      </main>
      </>
      )}
    </div>
  );
}

export default App;
