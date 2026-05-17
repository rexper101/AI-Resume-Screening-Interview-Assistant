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


