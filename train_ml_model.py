#!/usr/bin/env python3
"""
ML Model Trainer for AutoMind
Trains TF-IDF + RandomForest classifier for car prediction
"""

import json
import pickle
import random
from typing import List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score


class MLModelTrainer:
    """Train ML model for car classification."""
    
    def __init__(self, training_data_file: str = "data/training_data.json"):
        self.training_data_file = training_data_file
        self.vectorizer = None
        self.model = None
        self.class_names = []
        
    def load_training_data(self) -> Tuple[List[str], List[str]]:
        """Load training data from JSON file."""
        with open(self.training_data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        texts = [sample['text'] for sample in data['samples']]
        labels = [sample['label'] for sample in data['samples']]
        
        print(f"[Trainer] Loaded {len(texts)} samples with {data['num_classes']} classes")
        return texts, labels
    
    def train(self, test_size: float = 0.2, random_state: int = 42):
        """
        Train the ML model.
        
        Args:
            test_size: Proportion of data to use for testing
            random_state: Random seed for reproducibility
        """
        print("\n" + "=" * 70)
        print("  TRAINING ML MODEL")
        print("=" * 70)
        
        # Load data
        texts, labels = self.load_training_data()
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            texts, labels, test_size=test_size, random_state=random_state, stratify=labels
        )
        
        print(f"\n[Trainer] Train samples: {len(X_train)}")
        print(f"[Trainer] Test samples: {len(X_test)}")
        
        # Train TF-IDF vectorizer
        print("\n[Trainer] Training TF-IDF vectorizer...")
        self.vectorizer = TfidfVectorizer(
            max_features=500,  # Limit features for efficiency
            ngram_range=(1, 2),  # Unigrams and bigrams
            lowercase=True,
            stop_words='english'
        )
        X_train_vec = self.vectorizer.fit_transform(X_train)
        X_test_vec = self.vectorizer.transform(X_test)
        
        print(f"[Trainer] Vocabulary size: {len(self.vectorizer.vocabulary_)}")
        
        # Train Random Forest classifier
        print("\n[Trainer] Training RandomForest classifier...")
        self.model = RandomForestClassifier(
            n_estimators=100,  # Number of trees
            max_depth=20,  # Prevent overfitting
            random_state=random_state,
            n_jobs=-1  # Use all CPU cores
        )
        self.model.fit(X_train_vec, y_train)
        
        # Evaluate
        print("\n[Trainer] Evaluating model...")
        y_pred = self.model.predict(X_test_vec)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"\n{'=' * 70}")
        print(f"  MODEL PERFORMANCE")
        print(f"{'=' * 70}")
        print(f"\nAccuracy: {accuracy:.2%}")
        
        # Show detailed report for a subset of classes
        unique_labels = sorted(set(y_test))
        print(f"\nTotal classes: {len(unique_labels)}")
        
        # Show per-class metrics
        print("\n" + classification_report(y_test, y_pred, target_names=unique_labels, zero_division=0))
        
        self.class_names = self.model.classes_.tolist()
        
        return accuracy
    
    def save_model(self, model_file: str = "data/ml_model.pkl", vectorizer_file: str = "data/vectorizer.pkl"):
        """Save trained model and vectorizer."""
        if self.model is None or self.vectorizer is None:
            raise ValueError("Model not trained yet. Call train() first.")
        
        # Save model
        with open(model_file, 'wb') as f:
            pickle.dump(self.model, f)
        print(f"\n[Trainer] Saved model to {model_file}")
        
        # Save vectorizer
        with open(vectorizer_file, 'wb') as f:
            pickle.dump(self.vectorizer, f)
        print(f"[Trainer] Saved vectorizer to {vectorizer_file}")
        
        # Save metadata
        metadata = {
            'num_classes': len(self.class_names),
            'class_names': self.class_names,
            'vocab_size': len(self.vectorizer.vocabulary_)
        }
        
        with open("data/ml_metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)
        print(f"[Trainer] Saved metadata to data/ml_metadata.json")
    
    def test_predictions(self, test_queries: List[str]):
        """Test model with sample queries."""
        if self.model is None or self.vectorizer is None:
            raise ValueError("Model not trained yet. Call train() first.")
        
        print("\n" + "=" * 70)
        print("  SAMPLE PREDICTIONS")
        print("=" * 70)
        
        for query in test_queries:
            query_vec = self.vectorizer.transform([query])
            probabilities = self.model.predict_proba(query_vec)[0]
            
            # Get top 3 predictions
            top_3_idx = probabilities.argsort()[-3:][::-1]
            top_3 = [(self.model.classes_[idx], probabilities[idx] * 100) for idx in top_3_idx]
            
            print(f"\nQuery: '{query}'")
            print("Predictions:")
            for i, (car, confidence) in enumerate(top_3, 1):
                print(f"  {i}. {car.replace('_', ' ').title()} ({confidence:.1f}%)")


def main():
    """Train and save ML model."""
    print("=" * 70)
    print("  AUTOMIND ML - MODEL TRAINING")
    print("=" * 70)
    
    # Train model
    trainer = MLModelTrainer()
    accuracy = trainer.train()
    
    # Save model
    trainer.save_model()
    
    # Test with sample queries
    test_queries = [
        "electric SUV with third row seating",
        "reliable sedan with good gas mileage",
        "sporty coupe fast acceleration",
        "luxury sedan quiet ride comfortable",
        "affordable family hatchback under 10 lakhs",
        "premium BMW sedan",
        "Toyota SUV",
        "cheap Maruti car",
    ]
    
    trainer.test_predictions(test_queries)
    
    print("\n" + "=" * 70)
    print("✅ MODEL TRAINING COMPLETE!")
    print("=" * 70)
    print(f"\nModel accuracy: {accuracy:.2%}")
    print("\nNext steps:")
    print("  1. Test model: python test_ml_model.py")
    print("  2. Integrate: Update guessing_engine.py to use ML predictions")


if __name__ == "__main__":
    main()
