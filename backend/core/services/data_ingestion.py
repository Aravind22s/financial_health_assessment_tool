"""
Data Ingestion Service
Handles file upload, validation, and normalization
"""
import pandas as pd
import pdfplumber
from decimal import Decimal
from datetime import datetime
from typing import Dict, Any
import json


class DataIngestionService:
    """Service for processing uploaded financial data files"""
    
    def process_file(self, financial_data):
        """Process uploaded file based on type"""
        file_type = financial_data.file_type
        file_path = financial_data.file.path
        
        if file_type == 'csv':
            return self._process_csv(file_path)
        elif file_type == 'xlsx':
            return self._process_excel(file_path)
        elif file_type == 'pdf':
            return self._process_pdf(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
    
    def _process_csv(self, file_path: str) -> Dict[str, Any]:
        """Process CSV file"""
        try:
            df = pd.read_csv(file_path)
            return self._normalize_dataframe(df)
        except Exception as e:
            raise ValueError(f"Error processing CSV: {str(e)}")
    
    def _process_excel(self, file_path: str) -> Dict[str, Any]:
        """Process Excel file"""
        try:
            df = pd.read_excel(file_path)
            return self._normalize_dataframe(df)
        except Exception as e:
            raise ValueError(f"Error processing Excel: {str(e)}")
    
    def _process_pdf(self, file_path: str) -> Dict[str, Any]:
        """Process PDF file - extract tables"""
        try:
            data = {
                'balance_sheet': {},
                'income_statement': {},
                'cash_flow': {}
            }
            
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    tables = page.extract_tables()
                    for table in tables:
                        # Simple extraction - can be enhanced
                        if table and len(table) > 0:
                            # Try to identify statement type from headers
                            header = str(table[0]).lower()
                            if 'balance' in header or 'asset' in header:
                                data['balance_sheet'] = self._parse_table(table)
                            elif 'income' in header or 'revenue' in header:
                                data['income_statement'] = self._parse_table(table)
                            elif 'cash' in header:
                                data['cash_flow'] = self._parse_table(table)
            
            return data
        except Exception as e:
            raise ValueError(f"Error processing PDF: {str(e)}")
    
    def _normalize_dataframe(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Normalize DataFrame to standard format"""
        # Convert DataFrame to dictionary
        data = {
            'balance_sheet': {},
            'income_statement': {},
            'cash_flow': {},
            'raw_rows': []
        }
        
        # Store raw rows for reference
        for idx, row in df.iterrows():
            row_dict = row.to_dict()
            data['raw_rows'].append({k: str(v) for k, v in row_dict.items()})
        
        # Get column names (lowercase for matching)
        columns = {col: col.lower().strip() for col in df.columns}
        
        # Process columns and aggregate data
        for col_name, col_lower in columns.items():
            # Skip date/period columns
            if col_lower in ['date', 'period', 'month', 'year']:
                continue
            
            # Calculate average or latest value for the column
            try:
                # Get numeric values only
                values = pd.to_numeric(df[col_name], errors='coerce').dropna()
                if len(values) == 0:
                    continue
                
                # Use the latest value (last row) or average
                latest_value = float(values.iloc[-1])
                avg_value = float(values.mean())
                
                # Categorize based on column name
                # Balance Sheet items
                if any(term in col_lower for term in ['asset', 'cash', 'inventory', 'receivable', 'equipment', 'property']):
                    data['balance_sheet'][col_name] = latest_value
                elif any(term in col_lower for term in ['liability', 'liabilities', 'payable', 'debt', 'loan', 'equity', 'capital']):
                    data['balance_sheet'][col_name] = latest_value
                
                # Income Statement items (use average for flow items)
                elif any(term in col_lower for term in ['revenue', 'sales', 'income', 'expense', 'cost', 'profit', 'loss']):
                    data['income_statement'][col_name] = avg_value
                
                # Cash Flow items
                elif any(term in col_lower for term in ['cash flow', 'operating', 'investing', 'financing']):
                    data['cash_flow'][col_name] = avg_value
                else:
                    # Default: if it's a number, put it in income statement
                    data['income_statement'][col_name] = avg_value
                    
            except Exception as e:
                # Skip columns that can't be converted to numbers
                continue
        
        return data

    
    def _parse_table(self, table: list) -> Dict[str, float]:
        """Parse extracted table from PDF"""
        result = {}
        for row in table[1:]:  # Skip header
            if len(row) >= 2:
                try:
                    key = str(row[0]).strip()
                    value = str(row[1]).replace(',', '').replace('₹', '').strip()
                    result[key] = float(value)
                except:
                    continue
        return result
    
    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate normalized data"""
        # Check if we have at least some financial data
        has_data = (
            len(data.get('balance_sheet', {})) > 0 or
            len(data.get('income_statement', {})) > 0 or
            len(data.get('cash_flow', {})) > 0
        )
        return has_data
    
    def detect_anomalies(self, data: Dict[str, Any]) -> list:
        """Detect anomalies in financial data"""
        anomalies = []
        
        # Check for negative values where they shouldn't be
        balance_sheet = data.get('balance_sheet', {})
        for key, value in balance_sheet.items():
            if 'asset' in key.lower() and value < 0:
                anomalies.append(f"Negative asset value: {key}")
        
        # Check for missing critical items
        income_statement = data.get('income_statement', {})
        if not any('revenue' in k.lower() or 'sales' in k.lower() for k in income_statement.keys()):
            anomalies.append("Missing revenue/sales data")
        
        return anomalies
