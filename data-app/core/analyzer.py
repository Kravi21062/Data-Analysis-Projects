import pandas as pd
import numpy as np

class DataAnalyzer:
    def __init__(self, df):
        self.df = df
    
    def get_missing_summary(self):
        """Get summary of missing values"""
        missing = self.df.isnull().sum()
        missing_pct = (missing / len(self.df)) * 100
        
        summary = pd.DataFrame({
            'column': missing.index,
            'missing_count': missing.values,
            'missing_percentage': missing_pct.values
        })
        
        return summary[summary['missing_count'] > 0].sort_values('missing_percentage', ascending=False)
    
    def get_column_info(self):
        """Get detailed column information"""
        info_list = []
        
        for col in self.df.columns:
            info = {
                'Column': col,
                'Type': str(self.df[col].dtype),
                'Non-Null': self.df[col].count(),
                'Null': self.df[col].isnull().sum(),
                'Unique': self.df[col].nunique()
            }
            
            if pd.api.types.is_numeric_dtype(self.df[col]):
                info['Mean'] = f"{self.df[col].mean():.2f}"
                info['Min'] = f"{self.df[col].min():.2f}"
                info['Max'] = f"{self.df[col].max():.2f}"
            else:
                info['Mean'] = '-'
                info['Min'] = '-'
                info['Max'] = '-'
            
            info_list.append(info)
        
        return pd.DataFrame(info_list)
    
    def auto_detect_issues(self):
        """Automatically detect data quality issues and return recommendations"""
        issues = []
        recommendations = {}
        
        # Check for duplicates
        duplicates = self.df.duplicated().sum()
        if duplicates > 0:
            issues.append({
                'type': 'duplicates',
                'severity': 'high' if duplicates > len(self.df) * 0.05 else 'medium',
                'count': duplicates,
                'message': f"Found {duplicates} duplicate rows ({duplicates/len(self.df)*100:.1f}%)",
                'recommendation': 'Remove duplicate rows',
                'action': 'remove_duplicates'
            })
            recommendations['remove_duplicates'] = True
        
        # Check for missing values
        missing_total = self.df.isnull().sum().sum()
        if missing_total > 0:
            missing_pct = (missing_total / (len(self.df) * len(self.df.columns))) * 100
            severity = 'high' if missing_pct > 10 else 'medium' if missing_pct > 5 else 'low'
            
            issues.append({
                'type': 'missing_values',
                'severity': severity,
                'count': missing_total,
                'message': f"Found {missing_total} missing values ({missing_pct:.1f}%)",
                'recommendation': 'Handle missing values with appropriate strategy',
                'action': 'handle_missing'
            })
            recommendations['handle_missing'] = True
            
            # Suggest best strategy based on data
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                recommendations['missing_strategy'] = 'Fill with median'
            else:
                recommendations['missing_strategy'] = 'Drop rows'
        
        # Check for outliers in numeric columns
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        outlier_cols = []
        for col in numeric_cols:
            if len(self.df[col].dropna()) > 0:
                z_scores = np.abs((self.df[col] - self.df[col].mean()) / self.df[col].std())
                outliers = (z_scores > 3).sum()
                if outliers > 0:
                    outlier_cols.append((col, outliers))
        
        if outlier_cols:
            total_outliers = sum([count for _, count in outlier_cols])
            issues.append({
                'type': 'outliers',
                'severity': 'medium',
                'count': total_outliers,
                'message': f"Found outliers in {len(outlier_cols)} numeric columns",
                'recommendation': 'Remove or handle outliers',
                'action': 'remove_outliers',
                'details': outlier_cols
            })
            recommendations['remove_outliers'] = True
        
        # Check for text inconsistencies
        text_cols = self.df.select_dtypes(include=['object']).columns
        text_issues = []
        for col in text_cols:
            sample = self.df[col].dropna().head(100)
            if len(sample) > 0:
                # Check for leading/trailing spaces
                has_spaces = sample.str.strip().ne(sample).any()
                # Check for mixed case
                has_mixed_case = (sample.str.lower() != sample).any() and (sample.str.upper() != sample).any()
                
                if has_spaces or has_mixed_case:
                    text_issues.append(col)
        
        if text_issues:
            issues.append({
                'type': 'text_inconsistency',
                'severity': 'low',
                'count': len(text_issues),
                'message': f"Found text inconsistencies in {len(text_issues)} columns",
                'recommendation': 'Standardize text (trim spaces, normalize case)',
                'action': 'standardize_text',
                'details': text_issues
            })
            recommendations['standardize_text'] = True
        
        # Check for wrong data types
        type_issues = []
        for col in self.df.columns:
            if self.df[col].dtype == 'object':
                # Try to detect if it should be numeric
                sample = self.df[col].dropna().head(100)
                if len(sample) > 0:
                    try:
                        pd.to_numeric(sample)
                        type_issues.append((col, 'numeric'))
                    except:
                        # Try to detect if it should be datetime
                        try:
                            pd.to_datetime(sample)
                            type_issues.append((col, 'datetime'))
                        except:
                            pass
        
        if type_issues:
            issues.append({
                'type': 'wrong_types',
                'severity': 'medium',
                'count': len(type_issues),
                'message': f"Found {len(type_issues)} columns with potentially wrong data types",
                'recommendation': 'Convert to appropriate data types',
                'action': 'convert_types',
                'details': type_issues
            })
            recommendations['convert_types'] = True
        
        return issues, recommendations
    
    def get_data_quality_score(self):
        """Calculate overall data quality score (0-100)"""
        score = 100
        
        # Deduct for missing values
        missing_pct = (self.df.isnull().sum().sum() / (len(self.df) * len(self.df.columns))) * 100
        score -= min(missing_pct * 2, 30)
        
        # Deduct for duplicates
        dup_pct = (self.df.duplicated().sum() / len(self.df)) * 100
        score -= min(dup_pct * 2, 20)
        
        # Deduct for outliers
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            outlier_count = 0
            for col in numeric_cols:
                if len(self.df[col].dropna()) > 0:
                    z_scores = np.abs((self.df[col] - self.df[col].mean()) / self.df[col].std())
                    outlier_count += (z_scores > 3).sum()
            outlier_pct = (outlier_count / len(self.df)) * 100
            score -= min(outlier_pct, 15)
        
        return max(0, min(100, score))
