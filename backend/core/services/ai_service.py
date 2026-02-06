"""
AI Service using Gemini API
Generates narratives and enhances recommendations
"""
import google.generativeai as genai
from django.conf import settings
from typing import List


class AIService:
    """Service for AI-powered features using Gemini"""
    
    def __init__(self):
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            self.model = None
    
    def enhance_recommendations(self, company, recommendations, language='en'):
        """Enhance recommendations with AI-generated insights"""
        if not self.model:
            return recommendations
        
        # For now, return as-is if AI not configured
        # In production, would enhance with Gemini
        return recommendations
    
    def generate_financial_narrative(self, company, metrics, language='en'):
        """Generate plain-language financial narrative"""
        if not self.model:
            return self._generate_simple_narrative(company, metrics, language)
        
        try:
            prompt = self._build_narrative_prompt(company, metrics, language)
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            # Fallback to simple narrative
            return self._generate_simple_narrative(company, metrics, language)
    
    def _build_narrative_prompt(self, company, metrics, language):
        """Build prompt for narrative generation"""
        lang_instruction = "in Hindi" if language == 'hi' else "in English"
        
        prompt = f"""
You are a financial advisor explaining a company's financial health to a non-technical business owner {lang_instruction}.

Company: {company.name}
Industry: {company.industry}
Financial Health Score: {metrics.health_score}/100

Key Metrics:
- Current Ratio: {metrics.current_ratio}
- Net Margin: {metrics.net_margin}%
- Debt to Equity: {metrics.debt_to_equity}
- Receivables Days: {metrics.receivables_days}

Generate a clear, simple explanation of the company's financial health. Use simple language, avoid jargon, and provide actionable insights. Keep it under 200 words.
"""
        return prompt
    
    def _generate_simple_narrative(self, company, metrics, language='en'):
        """Generate simple narrative without AI"""
        if language == 'hi':
            return self._generate_hindi_narrative(company, metrics)
        
        narrative = f"Financial Health Summary for {company.name}\n\n"
        
        if metrics.health_score:
            if metrics.health_score >= 75:
                narrative += f"Your business is in excellent financial health with a score of {metrics.health_score}/100. "
            elif metrics.health_score >= 60:
                narrative += f"Your business is in good financial health with a score of {metrics.health_score}/100. "
            elif metrics.health_score >= 45:
                narrative += f"Your business has moderate financial health with a score of {metrics.health_score}/100. "
            else:
                narrative += f"Your business needs attention with a financial health score of {metrics.health_score}/100. "
        
        if metrics.current_ratio:
            if metrics.current_ratio >= 1.5:
                narrative += "You have strong liquidity to meet short-term obligations. "
            elif metrics.current_ratio >= 1.0:
                narrative += "Your liquidity is adequate but could be improved. "
            else:
                narrative += "You may face challenges meeting short-term obligations. "
        
        if metrics.net_margin:
            narrative += f"Your net profit margin is {metrics.net_margin}%, "
            if metrics.net_margin >= 15:
                narrative += "which is excellent. "
            elif metrics.net_margin >= 10:
                narrative += "which is good. "
            else:
                narrative += "which has room for improvement. "
        
        return narrative
    
    def _generate_hindi_narrative(self, company, metrics):
        """Generate simple Hindi narrative"""
        narrative = f"{company.name} की वित्तीय स्थिति\n\n"
        
        if metrics.health_score:
            if metrics.health_score >= 75:
                narrative += f"आपका व्यवसाय उत्कृष्ट वित्तीय स्वास्थ्य में है, स्कोर {metrics.health_score}/100 है। "
            elif metrics.health_score >= 60:
                narrative += f"आपका व्यवसाय अच्छी वित्तीय स्थिति में है, स्कोर {metrics.health_score}/100 है। "
            else:
                narrative += f"आपके व्यवसाय को ध्यान देने की आवश्यकता है, स्कोर {metrics.health_score}/100 है। "
        
        if metrics.net_margin:
            narrative += f"आपका शुद्ध लाभ मार्जिन {metrics.net_margin}% है। "
        
        return narrative
    
    def translate_text(self, text, target_language='hi'):
        """Translate text to target language"""
        if not self.model or target_language == 'en':
            return text
        
        try:
            prompt = f"Translate the following text to Hindi, maintaining financial terminology accuracy:\n\n{text}"
            response = self.model.generate_content(prompt)
            return response.text
        except:
            return text
