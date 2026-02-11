import { Beaker, Edit3, FlaskConical, Download, CheckCircle, AlertTriangle, XCircle } from 'lucide-react';

function Guide() {
  return (
    <div className="page-content">
      <h2>User Guide</h2>
      
      <div className="guide-section">
        <h3><Beaker size={20} style={{display: 'inline', marginRight: '8px', verticalAlign: 'middle'}} /> Step 1: Gather Soil Data</h3>
        <p>Collect the following parameters from laboratory soil tests:</p>
        <ul>
          <li><strong>Liquid Limit (LL):</strong> Moisture content at liquid state transition</li>
          <li><strong>Plastic Limit (PL):</strong> Moisture content at plastic state transition</li>
          <li><strong>Plasticity Index (PI):</strong> LL - PL</li>
          <li><strong>Grain Size Distribution:</strong> Gravel, Sand (Coarse, Medium, Fine), Fines</li>
          <li><strong>Compaction Properties:</strong> OMC, MDD, NMC</li>
        </ul>
      </div>

      <div className="guide-section">
        <h3><Edit3 size={20} style={{display: 'inline', marginRight: '8px', verticalAlign: 'middle'}} /> Step 2: Enter Data</h3>
        <p>Fill in all 11 soil parameter fields in the input form. Ensure:</p>
        <ul>
          <li>All values are numeric</li>
          <li>LL must be greater than PL</li>
          <li>Grain sizes should sum to approximately 100%</li>
          <li>Use proper units as indicated</li>
        </ul>
      </div>

      <div className="guide-section">
        <h3><FlaskConical size={20} style={{display: 'inline', marginRight: '8px', verticalAlign: 'middle'}} /> Step 3: Analyze</h3>
        <p>Click "Analyze Suitability" to generate the geotechnical report including:</p>
        <ul>
          <li>Soil classification (USCS/IS)</li>
          <li>Behavior characteristics</li>
          <li>Suitability rating</li>
          <li>Construction risks</li>
          <li>Engineering recommendations</li>
        </ul>
      </div>

      <div className="guide-section">
        <h3><Download size={20} style={{display: 'inline', marginRight: '8px', verticalAlign: 'middle'}} /> Step 4: Download Report</h3>
        <p>Generate a professional PDF report for documentation and sharing with your team.</p>
      </div>

      <div className="guide-section">
        <h3>Interpreting Results</h3>
        <div className="result-guide">
          <div className="result-item suitable-guide">
            <strong><CheckCircle size={18} style={{display: 'inline', marginRight: '8px', verticalAlign: 'middle'}} /> SUITABLE</strong>
            <p>Soil is appropriate for standard construction with normal precautions</p>
          </div>
          <div className="result-item moderate-guide">
            <strong><AlertTriangle size={18} style={{display: 'inline', marginRight: '8px', verticalAlign: 'middle'}} /> MODERATELY SUITABLE</strong>
            <p>Construction possible with soil improvement or special foundation design</p>
          </div>
          <div className="result-item unsuitable-guide">
            <strong><XCircle size={18} style={{display: 'inline', marginRight: '8px', verticalAlign: 'middle'}} /> UNSUITABLE</strong>
            <p>Major ground improvement required or consider alternative site</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Guide;
