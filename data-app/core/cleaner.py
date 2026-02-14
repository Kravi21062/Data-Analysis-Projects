import pandas as pd
import numpy as np

class DataCleaner:
    def __init__(self, df):
        self.df = df
    
    def remove_duplicates(self, df):
        """Remove duplicate rows"""
        return df.drop_duplicates()
    
    def handle_missing(self, df, strategy="Drop rows"):
        """Handle missing values based on strategy"""
        if strategy == "Drop rows":
            return df.dropna()
        elif strategy == "Fill with mean":
            return df.fillna(df.mean(numeric_only=True))
        elif strategy == "Fill with median":
            return df.fillna(df.median(numeric_only=True))
        elif strategy == "Fill with mode":
            return df.fillna(df.mode().iloc[0])
        elif strategy == "Forward fill":
            return df.fillna(method='ffill')
        return df
    
    def remove_outliers(self, df, threshold=3):
        """Remove outliers using Z-score method"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df_clean = df.copy()
        
        for col in numeric_cols:
            z_scores = np.abs((df_clean[col] - df_clean[col].mean()) / df_clean[col].std())
            df_clean = df_clean[z_scores < threshold]
        
        return df_clean
    
    def standardize_text(self, df):
        """Standardize text columns"""
        df_clean = df.copy()
        text_cols = df_clean.select_dtypes(include=['object']).columns
        
        for col in text_cols:
            df_clean[col] = df_clean[col].str.strip().str.lower()
        
        return df_clean
    
    def convert_types(self, df):
        """Auto-convert data types"""
        df_clean = df.copy()
        
        for col in df_clean.columns:
            # Try to convert to numeric
            try:
                df_clean[col] = pd.to_numeric(df_clean[col])
            except:
                # Try to convert to datetime
                try:
                    df_clean[col] = pd.to_datetime(df_clean[col])
                except:
                    pass
        
        return df_clean
