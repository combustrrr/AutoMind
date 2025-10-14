#!/usr/bin/env python3
"""Machine learning model for augmenting the expert system.

This module trains a simple classifier to predict a car's price segment based
on its features. The model's predictions can be used as a source of evidence
by the inference engine, demonstrating a hybrid AI/ML approach.
"""

from __future__ import annotations

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib
import os

class CarPriceClassifier:
    """A classifier to predict the price segment of a car."""

    def __init__(self, data_path="data/car_data_enriched.csv", model_path="ml_model.joblib"):
        self.data_path = data_path
        self.model_path = model_path
        self.model = None
        self.encoders = {}

    def train(self):
        """Trains the model and saves it to disk.
        
        Time Complexity: O(n * log(n) * m) for Random Forest training
        where n is samples, m is features
        """
        df = self._load_and_prepare_data()
        X, y = self._extract_features_and_target(df)
        self._train_and_save_model(X, y)
    
    def _load_and_prepare_data(self) -> pd.DataFrame:
        """Load data and derive price_segment if missing."""
        df = pd.read_csv(self.data_path)
        
        if 'price_segment' not in df.columns:
            df['price_segment'] = df['price_range'].apply(self._map_price_to_segment)
        
        return df.dropna(subset=['price_segment'])
    
    def _map_price_to_segment(self, price_range: str) -> str:
        """Map price range to price segment category."""
        mapping = {
            'under_10l': 'budget',
            '10-20l': 'value',
            'under_20l': 'value',
            '20-30l': 'upper',
        }
        return mapping.get(price_range, 'premium')
    
    def _extract_features_and_target(self, df: pd.DataFrame) -> tuple:
        """Extract and encode features and target variable."""
        features = ['body_type', 'fuel_type', 'luxury', 'engine_cc']
        target = 'price_segment'
        
        # Encode categorical features
        for col in features:
            if df[col].dtype == 'object' or df[col].dtype == 'bool':
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col])
                self.encoders[col] = le
        
        return df[features], df[target]
    
    def _train_and_save_model(self, X: pd.DataFrame, y: pd.Series):
        """Train the Random Forest model and save to disk."""
        X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)
        
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)
        
        joblib.dump((self.model, self.encoders), self.model_path)

    def load(self):
        """Loads a pre-trained model from disk."""
        if os.path.exists(self.model_path):
            self.model, self.encoders = joblib.load(self.model_path)
        else:
            self.train()

    def predict(self, car_features: dict) -> str | None:
        """Predicts the price segment for a given set of car features."""
        if not self.model:
            self.load()

        try:
            df = pd.DataFrame([car_features])
            for col, le in self.encoders.items():
                if col in df.columns:
                    # Handle unseen labels
                    df[col] = df[col].apply(lambda x: x if x in le.classes_ else -1)
                    df[col] = le.transform(df[col])

            prediction = self.model.predict(df)
            return prediction[0]
        except Exception:
            return None

if __name__ == '__main__':
    # Train the model if the script is run directly
    classifier = CarPriceClassifier()
    classifier.train()
    print(f"Model trained and saved to {classifier.model_path}")
