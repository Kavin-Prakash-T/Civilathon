from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from flask_bcrypt import Bcrypt
import os
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from pymongo import MongoClient
from dotenv import load_dotenv
import jwt


load_dotenv()

app = Flask(__name__)

CORS(
    app,
    resources={r"/api/*": {
        "origins": [
            "http://localhost:5173",          # local frontend
            "https://civilathon.vercel.app/" # deployed frontend
        ]
    }},
    supports_credentials=True,
    allow_headers=["Content-Type", "Authorization"],
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')

# MongoDB connection
mongo_uri = os.getenv('MONGODB_URI')
if not mongo_uri:
    print("ERROR: MONGODB_URI not found in .env file")
    exit(1)

try:
    client = MongoClient(mongo_uri)
    # Test connection
    client.admin.command('ping')
    print("MongoDB connected successfully")
except Exception as e:
    print(f"MongoDB connection error: {e}")
    exit(1)

db = client['soildata']  # Changed to 'soildata'
users_collection = db['users']
reports_collection = db['reports']

def verify_token(token):
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload
    except:
        return None

REPORT_PATH = os.path.join(os.path.dirname(__file__), 'reports')
os.makedirs(REPORT_PATH, exist_ok=True)

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'message': 'Soil Data Management API is running'})

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    
    if not email or not password or not name:
        return jsonify({'error': 'All fields required'}), 400
    
    if users_collection.find_one({'email': email}):
        return jsonify({'error': 'Email already exists'}), 400
    
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    user = {
        'name': name,
        'email': email,
        'password': hashed_password,
        'created_at': datetime.utcnow()
    }
    
    users_collection.insert_one(user)
    
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400
    
    user = users_collection.find_one({'email': email})
    
    if not user or not bcrypt.check_password_hash(user['password'], password):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    token = jwt.encode({
        'user_id': str(user['_id']),
        'email': user['email'],
        'exp': datetime.utcnow() + timedelta(days=7)
    }, app.config['SECRET_KEY'], algorithm='HS256')
    
    return jsonify({
        'token': token,
        'user': {
            'name': user['name'],
            'email': user['email']
        }
    }), 200

@app.route('/api/analyze-suitability', methods=['POST'])
def analyze_suitability():
    # Verify token
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    user_data = verify_token(token)
    if not user_data:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    soil_data = data.get('soil_data', {})
    
    # Extract parameters
    LL = soil_data.get('LL', 0)
    PL = soil_data.get('PL', 0)
    PI = soil_data.get('PI', 0)
    G = soil_data.get('G', 0)  # Gravel
    CS = soil_data.get('CS', 0) + soil_data.get('MS', 0) + soil_data.get('FS', 0)  # Total Sand
    F = soil_data.get('F', 0)  # Fines
    OMC = soil_data.get('OMC%', 0)
    MDD = soil_data.get('MDD (kN/m3)', 0)
    NMC = soil_data.get('NMC (%)', 0)
    
    # 1. SOIL CLASSIFICATION (USCS/IS)
    classification = ""
    if F < 50:  # Coarse-grained
        if G > CS:
            if F < 5:
                classification = "GW/GP - Well/Poorly graded Gravel"
            elif PI < 4:
                classification = "GM - Silty Gravel"
            else:
                classification = "GC - Clayey Gravel"
        else:
            if F < 5:
                classification = "SW/SP - Well/Poorly graded Sand"
            elif PI < 4:
                classification = "SM - Silty Sand"
            else:
                classification = "SC - Clayey Sand"
    else:  # Fine-grained
        if LL < 35:
            if PI < 7:
                classification = "ML - Silt of Low Plasticity"
            else:
                classification = "CL - Clay of Low Plasticity"
        elif LL < 50:
            if PI < 7:
                classification = "MI - Silt of Medium Plasticity"
            else:
                classification = "CI - Clay of Medium Plasticity"
        else:
            if PI < 7:
                classification = "MH - Silt of High Plasticity"
            else:
                classification = "CH - Clay of High Plasticity"
    
    # 2. SOIL BEHAVIOR ANALYSIS
    behavior = []
    if PI > 17:
        behavior.append("Highly plastic - prone to volume changes with moisture")
    elif PI > 7:
        behavior.append("Medium plasticity - moderate volume change potential")
    else:
        behavior.append("Low plasticity - minimal volume change")
    
    if F > 50:
        behavior.append("Fine-grained soil - susceptible to moisture sensitivity")
    else:
        behavior.append("Coarse-grained soil - good drainage characteristics")
    
    if MDD > 18:
        behavior.append("High density achievable - good compaction potential")
    elif MDD > 16:
        behavior.append("Moderate density - adequate compaction")
    
    # 3. SUITABILITY ASSESSMENT
    suitability_score = 0
    risks = []
    
    # Bearing capacity assessment
    if PI < 12 and F < 50:
        suitability_score += 3
    elif PI < 20:
        suitability_score += 2
        risks.append("Moderate bearing capacity - may require deeper foundations")
    else:
        suitability_score += 0
        risks.append("Low bearing capacity - deep foundations recommended")
    
    # Compressibility check
    if LL > 50 or PI > 30:
        risks.append("High compressibility - significant settlement expected")
        suitability_score -= 2
    elif LL > 35 or PI > 17:
        risks.append("Moderate compressibility - monitor settlement")
        suitability_score -= 1
    
    # Expansive soil check
    if PI > 35 and F > 50:
        risks.append("Highly expansive soil - severe swelling/shrinkage risk")
        suitability_score -= 3
    elif PI > 25 and F > 40:
        risks.append("Moderately expansive - foundation movement possible")
        suitability_score -= 2
    
    # Moisture sensitivity
    if abs(NMC - OMC) > 4:
        risks.append(f"Moisture content ({NMC}%) deviates from OMC ({OMC}%) - compaction issues")
        suitability_score -= 1
    
    # Drainage assessment
    if F > 50 and PI > 15:
        risks.append("Poor drainage - waterlogging risk, drainage system essential")
    
    # Final suitability
    if suitability_score >= 3:
        suitability = "SUITABLE"
        suitability_text = "Suitable for residential/light commercial construction"
    elif suitability_score >= 0:
        suitability = "MODERATELY SUITABLE"
        suitability_text = "Moderately suitable - requires soil improvement measures"
    else:
        suitability = "UNSUITABLE"
        suitability_text = "Not suitable without major ground improvement"
    
    # 4. RECOMMENDATIONS
    recommendations = []
    
    if PI > 25:
        recommendations.append("Use deep foundations (piles/piers) to reach stable strata")
        recommendations.append("Provide moisture barrier around foundation perimeter")
    
    if F > 50:
        recommendations.append("Install proper drainage system to control groundwater")
        recommendations.append("Consider soil stabilization with lime/cement")
    
    if MDD < 16:
        recommendations.append("Improve compaction through mechanical stabilization")
    
    if LL > 50:
        recommendations.append("Conduct consolidation tests for settlement analysis")
        recommendations.append("Consider preloading or ground improvement techniques")
    
    if suitability == "SUITABLE" and not recommendations:
        recommendations.append("Proceed with standard foundation design as per IS codes")
        recommendations.append("Maintain proper compaction at 95% of MDD")
        recommendations.append("Ensure adequate drainage around structures")
    
    if not recommendations:
        recommendations.append("Consult geotechnical engineer for detailed investigation")
        recommendations.append("Perform additional tests: triaxial, consolidation, CBR")
    
    # Save report to database
    report_data = {
        'user_id': user_data['user_id'],
        'user_email': user_data['email'],
        'classification': classification,
        'behavior': behavior,
        'suitability': suitability,
        'suitability_text': suitability_text,
        'risks': risks if risks else ['No major risks identified'],
        'recommendations': recommendations,
        'parameters': {
            'LL': LL,
            'PL': PL,
            'PI': PI,
            'Gravel': G,
            'Sand': CS,
            'Fines': F,
            'OMC': OMC,
            'MDD': MDD,
            'NMC': NMC
        },
        'created_at': datetime.utcnow()
    }
    
    result = reports_collection.insert_one(report_data)
    report_data['_id'] = str(result.inserted_id)
    
    return jsonify({
        'report_id': str(result.inserted_id),
        'classification': classification,
        'behavior': behavior,
        'suitability': suitability,
        'suitability_text': suitability_text,
        'risks': risks if risks else ['No major risks identified'],
        'recommendations': recommendations,
        'parameters': {
            'LL': LL,
            'PL': PL,
            'PI': PI,
            'Gravel': G,
            'Sand': CS,
            'Fines': F,
            'OMC': OMC,
            'MDD': MDD,
            'NMC': NMC
        }
    })

@app.route('/api/generate-report', methods=['POST'])
def generate_report():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    user_data = verify_token(token)
    if not user_data:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    result = data.get('result', {})
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"soil_report_{timestamp}.pdf"
    filepath = os.path.join(REPORT_PATH, filename)
    
    doc = SimpleDocTemplate(filepath, pagesize=A4, topMargin=0.6*inch, bottomMargin=0.6*inch, leftMargin=0.8*inch, rightMargin=0.8*inch)
    story = []
    styles = getSampleStyleSheet()
    
    # Professional styles
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], 
        fontSize=24, textColor=colors.HexColor('#1e3a5f'), 
        spaceAfter=6, alignment=TA_CENTER, fontName='Helvetica-Bold', leading=28)
    
    subtitle_style = ParagraphStyle('Subtitle', parent=styles['Normal'], 
        fontSize=10, textColor=colors.HexColor('#4a5568'), 
        alignment=TA_CENTER, spaceAfter=20)
    
    heading_style = ParagraphStyle('Heading', parent=styles['Heading2'], 
        fontSize=12, textColor=colors.HexColor('#1e3a5f'), 
        spaceAfter=8, spaceBefore=16, fontName='Helvetica-Bold', 
        borderPadding=(5, 0, 5, 0), leftIndent=0)
    
    body_style = ParagraphStyle('Body', parent=styles['Normal'], 
        fontSize=9.5, textColor=colors.HexColor('#1a1a1a'), 
        spaceAfter=5, leading=13, leftIndent=0)
    
    # Professional Header
    header_data = [[
        Paragraph("<b>GEOTECHNICAL ANALYSIS REPORT</b>", title_style),
    ]]
    header_table = Table(header_data, colWidths=[6.7*inch])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f7fafc')),
        ('TOPPADDING', (0, 0), (-1, -1), 20),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 0.15*inch))
    
    # Report Info
    info_data = [[
        Paragraph(f"<b>Report Date:</b> {datetime.now().strftime('%B %d, %Y')}", 
                 ParagraphStyle('Info', parent=styles['Normal'], fontSize=9, textColor=colors.HexColor('#4a5568'))),
        Paragraph(f"<b>Report ID:</b> {timestamp}", 
                 ParagraphStyle('Info', parent=styles['Normal'], fontSize=9, textColor=colors.HexColor('#4a5568'), alignment=TA_RIGHT))
    ]]
    info_table = Table(info_data, colWidths=[3.35*inch, 3.35*inch])
    info_table.setStyle(TableStyle([
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Disclaimer
    disclaimer_data = [[
        Paragraph("<b>DISCLAIMER:</b> This report provides preliminary geotechnical analysis for reference purposes. "
                 "Professional site investigation and licensed engineer review are required before construction.", 
                 ParagraphStyle('Disc', parent=styles['Normal'], fontSize=8.5, textColor=colors.HexColor('#c0392b'), leading=11))
    ]]
    disclaimer_table = Table(disclaimer_data, colWidths=[6.7*inch])
    disclaimer_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fef5e7')),
        ('BOX', (0, 0), (-1, -1), 1.5, colors.HexColor('#f39c12')),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(disclaimer_table)
    story.append(Spacer(1, 0.25*inch))
    
    # Section 1: Classification
    story.append(Paragraph("1. SOIL CLASSIFICATION", heading_style))
    class_data = [[Paragraph(result.get('classification', 'N/A'), 
                   ParagraphStyle('Class', parent=styles['Normal'], fontSize=10.5, 
                   textColor=colors.HexColor('#1a1a1a'), fontName='Helvetica-Bold', leading=14))]]
    class_table = Table(class_data, colWidths=[6.7*inch])
    class_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#edf2f7')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#2c5f8d')),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(class_table)
    story.append(Spacer(1, 0.18*inch))
    
    # Section 2: Parameters
    story.append(Paragraph("2. LABORATORY TEST RESULTS", heading_style))
    params = result.get('parameters', {})
    param_data = [[
        Paragraph('<b>Parameter</b>', ParagraphStyle('H', parent=styles['Normal'], fontSize=9.5, textColor=colors.white, fontName='Helvetica-Bold')),
        Paragraph('<b>Value</b>', ParagraphStyle('H', parent=styles['Normal'], fontSize=9.5, textColor=colors.white, fontName='Helvetica-Bold', alignment=TA_CENTER)),
        Paragraph('<b>Unit</b>', ParagraphStyle('H', parent=styles['Normal'], fontSize=9.5, textColor=colors.white, fontName='Helvetica-Bold', alignment=TA_CENTER))
    ]]
    
    param_rows = [
        ['Liquid Limit (LL)', params.get('LL', 'N/A'), '%'],
        ['Plastic Limit (PL)', params.get('PL', 'N/A'), '%'],
        ['Plasticity Index (PI)', params.get('PI', 'N/A'), '-'],
        ['Gravel Content', params.get('Gravel', 'N/A'), '%'],
        ['Sand Content', params.get('Sand', 'N/A'), '%'],
        ['Fines Content', params.get('Fines', 'N/A'), '%'],
        ['Optimum Moisture Content (OMC)', params.get('OMC', 'N/A'), '%'],
        ['Maximum Dry Density (MDD)', params.get('MDD', 'N/A'), 'kN/m³'],
        ['Natural Moisture Content (NMC)', params.get('NMC', 'N/A'), '%']
    ]
    
    for row in param_rows:
        param_data.append([str(row[0]), str(row[1]), str(row[2])])
    
    param_table = Table(param_data, colWidths=[3.8*inch, 1.8*inch, 1.1*inch])
    param_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a5f')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f7fafc')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(param_table)
    story.append(Spacer(1, 0.18*inch))
    
    # Section 3: Suitability
    story.append(Paragraph("3. SUITABILITY ASSESSMENT", heading_style))
    suitability = result.get('suitability', 'N/A')
    suit_color = '#2d6a4f' if suitability == 'SUITABLE' else ('#f39c12' if 'MODERATELY' in suitability else '#c0392b')
    suit_bg = '#d5f4e6' if suitability == 'SUITABLE' else ('#fef5e7' if 'MODERATELY' in suitability else '#fadbd8')
    
    suit_data = [[
        Paragraph(f"<b>{suitability}</b>", 
                 ParagraphStyle('Suit', parent=styles['Normal'], fontSize=12, 
                 textColor=colors.HexColor(suit_color), fontName='Helvetica-Bold', alignment=TA_CENTER)),
        Paragraph(result.get('suitability_text', ''), 
                 ParagraphStyle('SuitText', parent=body_style, fontSize=9.5, leading=13))
    ]]
    suit_table = Table(suit_data, colWidths=[1.6*inch, 5.1*inch])
    suit_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(suit_bg)),
        ('BOX', (0, 0), (-1, -1), 1.5, colors.HexColor(suit_color)),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(suit_table)
    story.append(Spacer(1, 0.18*inch))
    
    # Section 4: Behavior
    story.append(Paragraph("4. SOIL BEHAVIOR CHARACTERISTICS", heading_style))
    for behavior in result.get('behavior', []):
        story.append(Paragraph(f"• {behavior}", body_style))
    story.append(Spacer(1, 0.18*inch))
    
    # Section 5: Risks
    story.append(Paragraph("5. CONSTRUCTION RISKS", heading_style))
    for risk in result.get('risks', []):
        story.append(Paragraph(f"• {risk}", 
                     ParagraphStyle('Risk', parent=body_style, textColor=colors.HexColor('#c0392b'))))
    story.append(Spacer(1, 0.18*inch))
    
    # Section 6: Recommendations
    story.append(Paragraph("6. ENGINEERING RECOMMENDATIONS", heading_style))
    for i, rec in enumerate(result.get('recommendations', []), 1):
        story.append(Paragraph(f"<b>{i}.</b> {rec}", 
                     ParagraphStyle('Rec', parent=body_style, textColor=colors.HexColor('#2d6a4f'), leftIndent=15)))
    story.append(Spacer(1, 0.25*inch))
    
    # Professional Footer
    footer_data = [[
        Paragraph("<b>Geotechnical Analysis Platform</b>",
                 ParagraphStyle('FooterTitle', parent=styles['Normal'], fontSize=9, 
                 textColor=colors.HexColor('#1e3a5f'), alignment=TA_CENTER, fontName='Helvetica-Bold')),
    ], [
        Paragraph("This report is generated by automated analysis. For construction projects, consult a licensed geotechnical engineer.",
                 ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, 
                 textColor=colors.HexColor('#718096'), alignment=TA_CENTER))
    ]]
    footer_table = Table(footer_data, colWidths=[6.7*inch])
    footer_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f7fafc')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(footer_table)
    
    doc.build(story)
    return send_file(filepath, as_attachment=True, download_name=filename, mimetype='application/pdf')

@app.route('/api/my-reports', methods=['GET'])
def get_my_reports():
    # Verify token
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    user_data = verify_token(token)
    if not user_data:
        return jsonify({'error': 'Unauthorized'}), 401
    
    # Get user's reports
    reports = list(reports_collection.find(
        {'user_id': user_data['user_id']}
    ).sort('created_at', -1))
    
    # Convert ObjectId to string
    for report in reports:
        report['_id'] = str(report['_id'])
        report['created_at'] = report['created_at'].isoformat()
    
    return jsonify({'reports': reports}), 200

'''if __name__ == '__main__':
    app.run(debug=True, port=5000)'''

#for deployment
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)