function About() {
  return (
    <div className="page-content">
      <h2>About This Platform</h2>
      
      <div className="about-section">
        <h3>Purpose</h3>
        <p>
          The Soil Suitability Analysis Platform is designed to provide preliminary geotechnical 
          assessments for civil engineering projects. It helps engineers, students, and planners 
          evaluate soil conditions for construction purposes.
        </p>
      </div>

      <div className="about-section">
        <h3>Features</h3>
        <ul>
          <li>USCS/IS soil classification</li>
          <li>Construction suitability assessment</li>
          <li>Risk identification and analysis</li>
          <li>Engineering recommendations</li>
          <li>PDF report generation</li>
        </ul>
      </div>

      <div className="about-section">
        <h3>Methodology</h3>
        <p>
          Our analysis is based on established geotechnical engineering principles and 
          Indian Standard (IS) codes. The system uses rule-based logic to evaluate soil 
          parameters including Atterberg limits, grain size distribution, and compaction 
          characteristics.
        </p>
      </div>

      <div className="about-section">
        <h3>Limitations</h3>
        <ul>
          <li>This is a preliminary assessment tool only</li>
          <li>Does not replace detailed site investigation</li>
          <li>Professional engineer review is mandatory</li>
          <li>Does not account for groundwater or seismic conditions</li>
        </ul>
      </div>
    </div>
  );
}

export default About;
