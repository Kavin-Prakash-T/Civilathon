import { AlertTriangle } from 'lucide-react';

function Disclaimer() {
  return (
    <div className="disclaimer-banner">
      <div className="disclaimer-icon">
        <AlertTriangle size={24} color="#F4A261" />
      </div>
      <div className="disclaimer-content">
        <strong>PRELIMINARY ANALYSIS ONLY</strong>
        <p>This tool provides indicative results for educational and preliminary assessment purposes. 
        Detailed geotechnical investigation and professional engineer review required before construction decisions.</p>
      </div>
    </div>
  );
}

export default Disclaimer;
