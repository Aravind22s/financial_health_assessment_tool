"""
Report Generator Service
Generates PDF reports using ReportLab
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from django.core.files.base import ContentFile
from datetime import datetime
import io
from ..models import Report, FinancialMetrics, CreditAssessment, Recommendation


class ReportGenerator:
    """Service for generating PDF reports"""
    
    def generate_report(self, company, report_type='comprehensive', language='en'):
        """Generate PDF report for a company"""
        
        # Create PDF buffer
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a237e'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#283593'),
            spaceAfter=12,
            spaceBefore=12
        )
        
        # Title
        title_text = f"Financial Health Report - {company.name}"
        if language == 'hi':
            title_text = f"वित्तीय स्वास्थ्य रिपोर्ट - {company.name}"
        
        story.append(Paragraph(title_text, title_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Company Information
        story.append(Paragraph("Company Information" if language == 'en' else "कंपनी की जानकारी", heading_style))
        company_data = [
            ['Industry' if language == 'en' else 'उद्योग', company.get_industry_display()],
            ['GST Number' if language == 'en' else 'जीएसटी नंबर', company.gst_number or 'N/A'],
            ['Report Date' if language == 'en' else 'रिपोर्ट तिथि', datetime.now().strftime('%d-%m-%Y')]
        ]
        
        company_table = Table(company_data, colWidths=[2*inch, 4*inch])
        company_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e3f2fd')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        story.append(company_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Financial Metrics
        metrics = FinancialMetrics.objects.filter(company=company).first()
        if metrics:
            story.append(Paragraph("Financial Health Score" if language == 'en' else "वित्तीय स्वास्थ्य स्कोर", heading_style))
            
            score_text = f"Overall Score: {metrics.health_score}/100"
            if language == 'hi':
                score_text = f"कुल स्कोर: {metrics.health_score}/100"
            
            score_para = Paragraph(f"<b><font size=14>{score_text}</font></b>", styles['Normal'])
            story.append(score_para)
            story.append(Spacer(1, 0.2*inch))
            
            # Key Ratios Table
            story.append(Paragraph("Key Financial Ratios" if language == 'en' else "मुख्य वित्तीय अनुपात", heading_style))
            
            ratios_data = [
                ['Metric' if language == 'en' else 'मेट्रिक', 'Value' if language == 'en' else 'मूल्य'],
                ['Current Ratio' if language == 'en' else 'करंट रेशियो', str(metrics.current_ratio) if metrics.current_ratio else 'N/A'],
                ['Quick Ratio' if language == 'en' else 'क्विक रेशियो', str(metrics.quick_ratio) if metrics.quick_ratio else 'N/A'],
                ['Gross Margin' if language == 'en' else 'सकल मार्जिन', f"{metrics.gross_margin}%" if metrics.gross_margin else 'N/A'],
                ['Net Margin' if language == 'en' else 'शुद्ध मार्जिन', f"{metrics.net_margin}%" if metrics.net_margin else 'N/A'],
                ['Debt to Equity' if language == 'en' else 'ऋण से इक्विटी', str(metrics.debt_to_equity) if metrics.debt_to_equity else 'N/A'],
                ['ROA' if language == 'en' else 'आरओए', f"{metrics.roa}%" if metrics.roa else 'N/A'],
                ['ROE' if language == 'en' else 'आरओई', f"{metrics.roe}%" if metrics.roe else 'N/A'],
            ]
            
            ratios_table = Table(ratios_data, colWidths=[3*inch, 2*inch])
            ratios_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a237e')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(ratios_table)
            story.append(Spacer(1, 0.3*inch))
        
        # Credit Assessment
        assessment = CreditAssessment.objects.filter(company=company).first()
        if assessment and report_type in ['lender', 'comprehensive']:
            story.append(Paragraph("Credit Assessment" if language == 'en' else "ऋण मूल्यांकन", heading_style))
            
            credit_data = [
                ['Credit Rating' if language == 'en' else 'क्रेडिट रेटिंग', assessment.credit_rating],
                ['Credit Score' if language == 'en' else 'क्रेडिट स्कोर', f"{assessment.credit_score}/100"],
                ['Recommended Loan' if language == 'en' else 'अनुशंसित ऋण', 
                 f"₹{assessment.recommended_loan_amount:,.2f}" if assessment.recommended_loan_amount else 'N/A'],
                ['Recommended Tenure' if language == 'en' else 'अनुशंसित अवधि', 
                 f"{assessment.recommended_tenure_months} months" if assessment.recommended_tenure_months else 'N/A'],
            ]
            
            credit_table = Table(credit_data, colWidths=[3*inch, 2*inch])
            credit_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e3f2fd')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey)
            ]))
            story.append(credit_table)
            story.append(Spacer(1, 0.3*inch))
        
        # Recommendations
        recommendations = Recommendation.objects.filter(company=company)[:5]
        if recommendations:
            story.append(Paragraph("Top Recommendations" if language == 'en' else "शीर्ष सिफारिशें", heading_style))
            
            for i, rec in enumerate(recommendations, 1):
                rec_text = f"<b>{i}. {rec.title}</b><br/>{rec.description}"
                story.append(Paragraph(rec_text, styles['Normal']))
                story.append(Spacer(1, 0.15*inch))
        
        # Build PDF
        doc.build(story)
        
        # Save to model
        pdf_content = buffer.getvalue()
        buffer.close()
        
        filename = f"{company.name.replace(' ', '_')}_{report_type}_{datetime.now().strftime('%Y%m%d')}.pdf"
        
        report = Report.objects.create(
            company=company,
            report_type=report_type,
            language=language
        )
        report.file.save(filename, ContentFile(pdf_content))
        
        return report
