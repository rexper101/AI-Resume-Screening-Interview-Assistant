"""
role_predictor.py - ML classification model for predicting suitable job roles.
Trains on synthetic resume data using TF-IDF + Logistic Regression.
"""

import numpy as np
import warnings
warnings.filterwarnings('ignore')

from typing import Dict, List, Tuple, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

import sys
sys.path.insert(0, os.path.dirname(__file__))
from datasets.job_descriptions import JOB_ROLES


# ── Synthetic training data generation ────────────────────────────────────────
TRAINING_TEMPLATES = {
    "Data Scientist": [
        "python machine learning deep learning tensorflow scikit-learn pandas numpy statistics data visualization NLP AWS spark feature engineering data science",
        "data science machine learning python SQL statistics R tensorflow keras scikit-learn jupyter pandas data analysis predictive modeling",
        "python tensorflow pytorch deep learning neural networks NLP transformers BERT data preprocessing feature engineering model deployment AWS",
        "machine learning python statistics scikit-learn pandas numpy matplotlib seaborn plotly data visualization SQL postgres jupyter",
        "data scientist python R machine learning statistical analysis hypothesis testing A/B testing feature engineering random forest XGBoost",
        "deep learning computer vision NLP transformer models pytorch tensorflow python docker kubernetes AWS model deployment MLOps",
        "python machine learning scikit-learn TF-IDF recommendation system collaborative filtering content-based filtering pandas SQL",
        "data science python pandas scikit-learn matplotlib power bi tableau SQL statistical modeling regression classification clustering",
    ],
    "Data Analyst": [
        "SQL Excel Tableau Power BI python pandas data analysis business intelligence reporting ETL data cleaning postgresql",
        "SQL data analysis Excel Tableau Power BI reporting business intelligence KPI metrics dashboards data visualization MySQL",
        "excel SQL Tableau data analysis business intelligence reporting stakeholder management data cleaning ETL data modeling",
        "python pandas SQL data analysis visualization matplotlib seaborn plotly Excel Power BI reporting business analysis",
        "SQL MySQL PostgreSQL data analysis reporting Excel Power BI Tableau looker business intelligence data warehouse ETL",
        "data analyst SQL Excel Python business intelligence reporting metrics KPI dashboard Tableau Looker data visualization",
        "SQL python data analysis Power BI Excel reporting stakeholder communication business analytics data modeling statistics",
    ],
    "ML Engineer": [
        "python machine learning MLOps docker kubernetes AWS FastAPI model deployment scikit-learn tensorflow CI/CD REST API",
        "MLOps docker kubernetes AWS machine learning model serving FastAPI python TensorFlow PyTorch CI/CD GitHub Actions",
        "python tensorflow pytorch model deployment docker kubernetes AWS SageMaker mlflow feature engineering REST API",
        "machine learning engineering python docker kubernetes CI/CD model monitoring A/B testing FastAPI microservices AWS",
        "ML engineer python scikit-learn tensorflow pytorch model deployment AWS docker kubernetes mlflow experiment tracking",
        "python machine learning model deployment FastAPI docker kubernetes AWS CI/CD model monitoring drift detection",
        "ML pipeline python airflow spark feature store model registry mlflow kubeflow tensorflow serving kubernetes",
    ],
    "Python Developer": [
        "python django FastAPI Flask REST API SQL postgresql celery redis docker git CI/CD linux backend development",
        "python backend django REST API postgresql MySQL docker kubernetes AWS git unit testing celery SQLAlchemy",
        "python Flask django REST API microservices docker postgresql AWS CI/CD git linux celery redis backend",
        "python FastAPI docker postgresql redis REST API authentication JWT testing CI/CD GitHub Actions git linux",
        "python django ORM REST API unit testing PostgreSQL celery docker AWS deployment git CI/CD backend web",
        "python backend development Flask REST API SQLAlchemy MySQL docker git linux unit testing pytest CI/CD",
        "python microservices FastAPI docker kubernetes REST API postgresql redis message queue kafka git CI/CD",
    ],
    "Backend Developer": [
        "java python node.js SQL NoSQL MongoDB PostgreSQL REST API microservices docker kubernetes AWS Spring Boot",
        "java Spring Boot REST API microservices docker kubernetes AWS postgresql MySQL CI/CD git linux backend",
        "node.js javascript Express.js REST API MongoDB PostgreSQL docker AWS microservices CI/CD git backend",
        "python java backend microservices REST API docker kubernetes AWS SQL NoSQL cache Redis Kafka CI/CD",
        "java Spring Boot microservices REST API docker kubernetes MySQL AWS CI/CD git linux backend development",
        "node.js express REST API MongoDB SQL docker kubernetes AWS CI/CD microservices authentication JWT",
        "backend development python java node.js SQL NoSQL docker microservices REST API cloud AWS Azure",
    ],
    "AI Engineer": [
        "python LLM GPT OpenAI langchain RAG vector database NLP machine learning deep learning pytorch transformers",
        "AI engineer python LLM fine-tuning RLHF prompt engineering OpenAI Hugging Face langchain vector database NLP",
        "generative AI python LLM RAG langchain openai hugging face transformers pytorch NLP embedding search",
        "python AI LLM prompt engineering langchain openai GPT vector database chroma pinecone RAG NLP transformers",
        "AI engineer python deep learning NLP transformers BERT GPT fine-tuning hugging face pytorch langchain",
        "LLM applications python openai anthropic langchain RAG vector search embeddings NLP machine learning docker AWS",
        "generative AI python LLM fine-tuning RLHF alignment safety hugging face pytorch transformers NLP",
    ],
    "Frontend Developer": [
        "react javascript typescript HTML CSS tailwind redux REST API git jest responsive design node.js",
        "react.js javascript typescript HTML5 CSS3 tailwind CSS Redux next.js REST API git webpack jest",
        "javascript react typescript next.js HTML CSS tailwind responsive design redux REST API testing git",
        "frontend react javascript HTML CSS node.js npm webpack jest typescript tailwind CSS responsive",
        "react.js typescript javascript HTML5 CSS3 styled-components redux REST API git jest CI/CD next.js",
        "javascript react next.js typescript CSS HTML REST API git unit testing node.js webpack tailwind",
        "frontend development react javascript HTML CSS typescript redux REST API git responsive mobile-first",
    ],
    "DevOps Engineer": [
        "docker kubernetes AWS terraform ansible CI/CD jenkins linux python bash prometheus grafana git security",
        "kubernetes docker AWS terraform ansible CI/CD GitHub Actions linux monitoring prometheus grafana ELK",
        "AWS kubernetes docker terraform CI/CD jenkins ansible linux bash python monitoring grafana prometheus",
        "DevOps docker kubernetes terraform AWS CI/CD linux python bash ansible monitoring Prometheus grafana helm",
        "AWS infrastructure kubernetes terraform docker CI/CD GitHub Actions ansible linux bash security monitoring",
        "Kubernetes docker AWS GCP terraform CI/CD argocd helm ansible linux python bash prometheus grafana",
        "DevOps engineer docker kubernetes AWS terraform ansible CI/CD jenkins linux monitoring security python",
    ],
}


class RolePredictor:
    """
    ML classification model for predicting job roles from resume text.
    Uses TF-IDF vectorization with multiple classifier options.
    """

    def __init__(self, model_type: str = "logistic_regression"):
        """
        Initialize the role predictor.

        Args:
            model_type: "logistic_regression", "random_forest", or "naive_bayes"
        """
        self.model_type = model_type
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=3000,
            stop_words='english',
            min_df=1
        )
        self.label_encoder = LabelEncoder()
        self.model = self._create_model(model_type)
        self.is_trained = False
        self.training_accuracy = 0.0
        self.classes = []

    def _create_model(self, model_type: str):
        """Create the specified ML model."""
        models = {
            "logistic_regression": LogisticRegression(
                max_iter=1000,
                C=1.0,
                solver='lbfgs',
                random_state=42
            ),
            "random_forest": RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                n_jobs=-1
            ),
            "naive_bayes": MultinomialNB(alpha=0.1)
        }
        return models.get(model_type, models["logistic_regression"])

    def generate_training_data(self) -> Tuple[List[str], List[str]]:
        """
        Generate synthetic training data from templates.

        Returns:
            Tuple of (texts, labels)
        """
        texts = []
        labels = []

        for role, templates in TRAINING_TEMPLATES.items():
            for template in templates:
                texts.append(template)
                labels.append(role)

                # Data augmentation: shuffle words in template
                words = template.split()
                for _ in range(2):  # 2 augmented versions per template
                    np.random.shuffle(words)
                    texts.append(' '.join(words))
                    labels.append(role)

        return texts, labels

    def train(self) -> Dict:
        """
        Train the model on synthetic data.

        Returns:
            Training metrics dict
        """
        texts, labels = self.generate_training_data()

        # Encode labels
        encoded_labels = self.label_encoder.fit_transform(labels)
        self.classes = list(self.label_encoder.classes_)

        # Split for evaluation
        X_train, X_test, y_train, y_test = train_test_split(
            texts, encoded_labels, test_size=0.2, random_state=42, stratify=encoded_labels
        )

        # Vectorize
        X_train_vec = self.vectorizer.fit_transform(X_train)
        X_test_vec = self.vectorizer.transform(X_test)

        # For Naive Bayes, values must be non-negative (TF-IDF is already non-negative)
        # Train model
        self.model.fit(X_train_vec, y_train)

        # Evaluate
        y_pred = self.model.predict(X_test_vec)
        accuracy = accuracy_score(y_test, y_pred)

        self.is_trained = True
        self.training_accuracy = accuracy

        return {
            "accuracy": round(accuracy * 100, 1),
            "model_type": self.model_type,
            "training_samples": len(X_train),
            "test_samples": len(X_test),
            "num_classes": len(self.classes),
            "classes": self.classes
        }

    def predict(self, resume_text: str, skills: List[str]) -> Dict:
        """
        Predict the most suitable role for a resume.

        Args:
            resume_text: Full resume text
            skills: Extracted skills list

        Returns:
            Prediction result with probabilities
        """
        if not self.is_trained:
            self.train()

        # Prepare input: combine resume text with skills (weighted)
        input_text = f"{resume_text.lower()} {' '.join(skills * 3)}"

        # Vectorize
        input_vec = self.vectorizer.transform([input_text])

        # Get prediction and probabilities
        predicted_label = self.model.predict(input_vec)[0]
        predicted_role = self.label_encoder.inverse_transform([predicted_label])[0]

        # Get probabilities
        if hasattr(self.model, 'predict_proba'):
            probabilities = self.model.predict_proba(input_vec)[0]
        else:
            # For models without predict_proba
            probabilities = np.zeros(len(self.classes))
            probabilities[predicted_label] = 1.0

        # Build probability map
        prob_map = {}
        for i, role in enumerate(self.classes):
            prob_map[role] = round(float(probabilities[i]) * 100, 1)

        # Sort by probability
        sorted_probs = dict(sorted(prob_map.items(), key=lambda x: x[1], reverse=True))

        return {
            "predicted_role": predicted_role,
            "confidence": round(float(probabilities[predicted_label]) * 100, 1),
            "all_probabilities": sorted_probs,
            "top_3_roles": list(sorted_probs.items())[:3],
            "model_type": self.model_type,
            "model_accuracy": self.training_accuracy * 100
        }

    def get_feature_importance(self, resume_text: str, skills: List[str], top_n: int = 10) -> List[Dict]:
        """
        Get the most influential features (skills/keywords) for the prediction.
        Implements Explainable AI for the recommendation.

        Args:
            resume_text: Resume text
            skills: Extracted skills
            top_n: Number of top features to return

        Returns:
            List of feature importance dicts
        """
        if not self.is_trained:
            return []

        input_text = f"{resume_text.lower()} {' '.join(skills * 3)}"
        input_vec = self.vectorizer.transform([input_text])

        feature_names = self.vectorizer.get_feature_names_out()
        input_array = input_vec.toarray()[0]

        # Get non-zero features
        non_zero_indices = np.where(input_array > 0)[0]

        # For Logistic Regression: use coefficient magnitude
        if hasattr(self.model, 'coef_') and self.model_type == "logistic_regression":
            predicted_class = self.model.predict(input_vec)[0]
            coefficients = self.model.coef_[predicted_class]
            importance_scores = input_array * np.abs(coefficients)
        else:
            # Fall back to TF-IDF scores
            importance_scores = input_array

        # Get top features
        top_indices = np.argsort(importance_scores)[-top_n:][::-1]

        features = []
        for idx in top_indices:
            if idx < len(feature_names) and importance_scores[idx] > 0:
                features.append({
                    "feature": feature_names[idx],
                    "score": round(float(importance_scores[idx]), 4),
                    "is_skill": feature_names[idx] in [s.lower() for s in skills]
                })

        return features


def get_role_predictor(model_type: str = "logistic_regression") -> RolePredictor:
    """
    Factory function to get a trained RolePredictor instance.

    Args:
        model_type: Model type to use

    Returns:
        Trained RolePredictor
    """
    predictor = RolePredictor(model_type=model_type)
    predictor.train()
    return predictor
