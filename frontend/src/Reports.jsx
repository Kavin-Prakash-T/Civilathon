import { useState, useEffect } from 'react';
import { getMyReports, generateReport } from './api';
import { Download, Calendar, FileText, ClipboardList, GitCompare, X } from 'lucide-react';

function Reports() {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedReports, setSelectedReports] = useState([]);
  const [compareMode, setCompareMode] = useState(false);

  useEffect(() => {
    fetchReports();
  }, []);

  const fetchReports = async () => {
    setLoading(true);
    try {
      const res = await getMyReports();
      setReports(res.data.reports);
    } catch (error) {
      alert('Failed to load reports: ' + (error.response?.data?.error || error.message));
    }
    setLoading(false);
  };

  const handleDownload = async (report) => {
    try {
      const res = await generateReport({ result: report });
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `soil_report_${new Date(report.created_at).getTime()}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      alert('Download failed: ' + (error.response?.data?.error || error.message));
    }
  };

  const toggleSelectReport = (report) => {
    if (selectedReports.find(r => r._id === report._id)) {
      setSelectedReports(selectedReports.filter(r => r._id !== report._id));
    } else if (selectedReports.length < 2) {
      setSelectedReports([...selectedReports, report]);
    }
  };

  const startCompare = () => {
    if (selectedReports.length === 2) {
      setCompareMode(true);
    }
  };

  const exitCompare = () => {
    setCompareMode(false);
    setSelectedReports([]);
  };

  if (compareMode && selectedReports.length === 2) {
    const [report1, report2] = selectedReports;
    return (
      <div className="section">
        <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px'}}>
          <h2><GitCompare size={20} style={{display: 'inline', marginRight: '8px', verticalAlign: 'middle'}} /> Compare Reports</h2>
          <button onClick={exitCompare} className="compare-exit-btn">
            <X size={18} /> Exit Comparison
          </button>
        </div>
        
        <div className="compare-container">
          <div className="compare-column">
            <div className="compare-header">
              <h3>Report 1</h3>
              <span className={`badge ${report1.suitability.toLowerCase().replace(' ', '-')}`}>
                {report1.suitability}
              </span>
            </div>
            <div className="compare-content">
              <div className="compare-item">
                <strong>Classification:</strong>
                <p>{report1.classification}</p>
              </div>
              <div className="compare-item">
                <strong>Date:</strong>
                <p>{new Date(report1.created_at).toLocaleString()}</p>
              </div>
              <div className="compare-item">
                <strong>Suitability:</strong>
                <p>{report1.suitability_text}</p>
              </div>
              <div className="compare-item">
                <strong>Parameters:</strong>
                <div className="param-list">
                  {Object.entries(report1.parameters).map(([key, value]) => (
                    <div key={key}><span>{key}:</span> {value}</div>
                  ))}
                </div>
              </div>
              <div className="compare-item">
                <strong>Risks ({report1.risks.length}):</strong>
                <ul>
                  {report1.risks.map((risk, i) => <li key={i}>{risk}</li>)}
                </ul>
              </div>
              <div className="compare-item">
                <strong>Recommendations ({report1.recommendations.length}):</strong>
                <ul>
                  {report1.recommendations.map((rec, i) => <li key={i}>{rec}</li>)}
                </ul>
              </div>
            </div>
          </div>

          <div className="compare-divider"></div>

          <div className="compare-column">
            <div className="compare-header">
              <h3>Report 2</h3>
              <span className={`badge ${report2.suitability.toLowerCase().replace(' ', '-')}`}>
                {report2.suitability}
              </span>
            </div>
            <div className="compare-content">
              <div className="compare-item">
                <strong>Classification:</strong>
                <p>{report2.classification}</p>
              </div>
              <div className="compare-item">
                <strong>Date:</strong>
                <p>{new Date(report2.created_at).toLocaleString()}</p>
              </div>
              <div className="compare-item">
                <strong>Suitability:</strong>
                <p>{report2.suitability_text}</p>
              </div>
              <div className="compare-item">
                <strong>Parameters:</strong>
                <div className="param-list">
                  {Object.entries(report2.parameters).map(([key, value]) => (
                    <div key={key}><span>{key}:</span> {value}</div>
                  ))}
                </div>
              </div>
              <div className="compare-item">
                <strong>Risks ({report2.risks.length}):</strong>
                <ul>
                  {report2.risks.map((risk, i) => <li key={i}>{risk}</li>)}
                </ul>
              </div>
              <div className="compare-item">
                <strong>Recommendations ({report2.recommendations.length}):</strong>
                <ul>
                  {report2.recommendations.map((rec, i) => <li key={i}>{rec}</li>)}
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="section">
      <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px'}}>
        <div>
          <h2><ClipboardList size={20} style={{display: 'inline', marginRight: '8px', verticalAlign: 'middle'}} /> My Reports</h2>
          <p>View and download your previous soil analysis reports</p>
        </div>
        {selectedReports.length > 0 && (
          <div className="compare-actions">
            <span className="selected-count">{selectedReports.length} selected</span>
            <button 
              onClick={startCompare} 
              disabled={selectedReports.length !== 2}
              className="compare-btn"
            >
              <GitCompare size={18} /> Compare
            </button>
            <button onClick={() => setSelectedReports([])} className="clear-btn">
              Clear
            </button>
          </div>
        )}
      </div>
      
      {loading ? (
        <div className="loading">Loading reports...</div>
      ) : reports.length === 0 ? (
        <div className="no-reports">
          <FileText size={48} color="#ccc" />
          <p>No reports found. Analyze soil data to generate reports.</p>
        </div>
      ) : (
        <div className="reports-grid">
          {reports.map((report) => {
            const isSelected = selectedReports.find(r => r._id === report._id);
            return (
            <div 
              key={report._id} 
              className={`report-card ${isSelected ? 'selected' : ''}`}
              onClick={() => toggleSelectReport(report)}
              style={{cursor: 'pointer'}}
            >
              {isSelected && <div className="selected-badge">Selected</div>}
              <div className="report-header">
                <h3>{report.classification}</h3>
                <span className={`badge ${report.suitability.toLowerCase().replace(' ', '-')}`}>
                  {report.suitability}
                </span>
              </div>
              
              <div className="report-meta">
                <Calendar size={16} />
                <span>{new Date(report.created_at).toLocaleString()}</span>
              </div>
              
              <div className="report-summary">
                <p><strong>Suitability:</strong> {report.suitability_text}</p>
                <p><strong>Risks:</strong> {report.risks.length} identified</p>
                <p><strong>Recommendations:</strong> {report.recommendations.length} provided</p>
              </div>
              
              <button 
                onClick={(e) => { e.stopPropagation(); handleDownload(report); }} 
                className="download-btn-small"
              >
                <Download size={16} /> Download PDF
              </button>
            </div>
          )})}
        </div>
      )}
    </div>
  );
}

export default Reports;
