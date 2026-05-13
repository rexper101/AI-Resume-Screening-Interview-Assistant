"""
Sample job descriptions dataset for the AI Resume Screening system.
Each job role includes required skills, description, and metadata.
"""

JOB_ROLES = {
    "Data Scientist": {
        "description": """
        We are looking for a Data Scientist with strong expertise in machine learning,
        statistical analysis, and data visualization. The candidate should have experience
        with Python, TensorFlow or PyTorch, and SQL. Knowledge of deep learning, NLP,
        and cloud platforms like AWS or GCP is highly preferred.
        Requirements: Python, Machine Learning, Deep Learning, TensorFlow, SQL, Statistics,
        Data Visualization, Pandas, NumPy, Scikit-learn, Jupyter, R, Tableau, Power BI,
        NLP, AWS, Azure, Big Data, Spark, Feature Engineering, Model Deployment.
        """,
        "required_skills": [
            "python", "machine learning", "deep learning", "tensorflow", "sql",
            "statistics", "data visualization", "pandas", "numpy", "scikit-learn",
            "nlp", "aws", "spark", "feature engineering"
        ],
        "nice_to_have": ["pytorch", "r", "tableau", "power bi", "azure", "gcp", "docker"],
        "experience_years": "2-5 years",
        "salary_range": "$90,000 - $150,000",
        "category": "Data Science"
    },

    "Data Analyst": {
        "description": """
        We are seeking a Data Analyst to interpret data, analyze results using statistical
        techniques, and provide ongoing reports. The ideal candidate has strong SQL skills,
        experience with Excel, and proficiency in visualization tools like Tableau or Power BI.
        Requirements: SQL, Excel, Tableau, Power BI, Python, Statistics, Data Analysis,
        Data Cleaning, Reporting, Business Intelligence, Dashboard, ETL, PostgreSQL, MySQL.
        """,
        "required_skills": [
            "sql", "excel", "tableau", "power bi", "python", "statistics",
            "data analysis", "data cleaning", "reporting", "business intelligence",
            "postgresql", "mysql"
        ],
        "nice_to_have": ["r", "pandas", "numpy", "matplotlib", "looker", "snowflake"],
        "experience_years": "1-3 years",
        "salary_range": "$60,000 - $95,000",
        "category": "Analytics"
    },

    "ML Engineer": {
        "description": """
        We need a Machine Learning Engineer to design, build, and deploy ML models at scale.
        Strong Python programming, experience with MLOps, Docker, Kubernetes, and cloud
        platforms are required. Knowledge of model optimization, A/B testing, and CI/CD pipelines.
        Requirements: Python, Machine Learning, TensorFlow, PyTorch, MLOps, Docker, Kubernetes,
        AWS, CI/CD, REST API, FastAPI, Flask, Model Deployment, Feature Engineering,
        Scikit-learn, Deep Learning, GPU Computing.
        """,
        "required_skills": [
            "python", "machine learning", "tensorflow", "pytorch", "docker", "kubernetes",
            "aws", "mlops", "rest api", "fastapi", "flask", "scikit-learn", "deep learning",
            "ci/cd", "feature engineering"
        ],
        "nice_to_have": ["gcp", "azure", "spark", "airflow", "mlflow", "kubeflow", "redis"],
        "experience_years": "3-6 years",
        "salary_range": "$110,000 - $170,000",
        "category": "Machine Learning"
    },

    "Python Developer": {
        "description": """
        We are hiring a Python Developer with strong backend development experience.
        The ideal candidate is proficient in Django or FastAPI, understands RESTful APIs,
        databases, and has experience with cloud deployment. Docker and CI/CD knowledge preferred.
        Requirements: Python, Django, FastAPI, Flask, REST API, PostgreSQL, MySQL, Redis,
        Docker, Git, Linux, AWS, CI/CD, Unit Testing, Celery, SQLAlchemy.
        """,
        "required_skills": [
            "python", "django", "fastapi", "flask", "rest api", "postgresql",
            "mysql", "docker", "git", "linux", "aws", "unit testing", "celery", "sql"
        ],
        "nice_to_have": ["redis", "rabbitmq", "kubernetes", "graphql", "microservices", "mongodb"],
        "experience_years": "2-4 years",
        "salary_range": "$80,000 - $130,000",
        "category": "Backend Development"
    },

    "Backend Developer": {
        "description": """
        We are looking for a Backend Developer with expertise in server-side development.
        Experience with Java, Python, or Node.js is required. Strong understanding of
        databases, API design, microservices architecture, and cloud technologies.
        Requirements: Java, Python, Node.js, SQL, NoSQL, MongoDB, PostgreSQL, REST API,
        Microservices, Docker, Kubernetes, AWS, Spring Boot, CI/CD, Git, Linux.
        """,
        "required_skills": [
            "java", "python", "node.js", "sql", "nosql", "mongodb", "postgresql",
            "rest api", "microservices", "docker", "kubernetes", "aws", "spring boot",
            "ci/cd", "git", "linux"
        ],
        "nice_to_have": ["graphql", "redis", "kafka", "grpc", "terraform", "azure"],
        "experience_years": "3-5 years",
        "salary_range": "$95,000 - $145,000",
        "category": "Backend Development"
    },

    "AI Engineer": {
        "description": """
        Seeking an AI Engineer to develop and deploy cutting-edge AI solutions. Must have
        expertise in LLMs, prompt engineering, RAG architectures, and AI APIs. Experience
        with OpenAI, Anthropic, or Hugging Face models required. MLOps and cloud experience needed.
        Requirements: Python, LLM, Prompt Engineering, OpenAI API, Hugging Face, RAG,
        LangChain, Vector Databases, Machine Learning, Deep Learning, TensorFlow, PyTorch,
        AWS, Docker, FastAPI, NLP, Transformers.
        """,
        "required_skills": [
            "python", "machine learning", "deep learning", "nlp", "transformers",
            "llm", "openai", "hugging face", "langchain", "vector database",
            "pytorch", "tensorflow", "aws", "docker", "fastapi", "prompt engineering"
        ],
        "nice_to_have": ["rag", "fine-tuning", "rlhf", "kubernetes", "mlflow", "chroma", "pinecone"],
        "experience_years": "2-5 years",
        "salary_range": "$120,000 - $180,000",
        "category": "AI/ML"
    },

    "Frontend Developer": {
        "description": """
        We need a Frontend Developer with strong expertise in React.js, JavaScript/TypeScript,
        and modern CSS frameworks. Experience building responsive, accessible web applications.
        Knowledge of state management, testing, and performance optimization required.
        Requirements: React, JavaScript, TypeScript, HTML, CSS, Tailwind CSS, Redux,
        REST API, Git, Webpack, Jest, Responsive Design, Figma, Node.js.
        """,
        "required_skills": [
            "react", "javascript", "typescript", "html", "css", "tailwind css",
            "redux", "rest api", "git", "jest", "responsive design", "node.js"
        ],
        "nice_to_have": ["next.js", "vue.js", "graphql", "webpack", "docker", "figma", "storybook"],
        "experience_years": "2-4 years",
        "salary_range": "$80,000 - $130,000",
        "category": "Frontend Development"
    },

    "DevOps Engineer": {
        "description": """
        We are seeking a DevOps Engineer to build and maintain CI/CD pipelines, manage
        cloud infrastructure, and ensure system reliability. Experience with AWS/GCP/Azure,
        Kubernetes, Terraform, and monitoring tools required.
        Requirements: Docker, Kubernetes, AWS, Terraform, CI/CD, Jenkins, Linux,
        Python, Bash, Monitoring, Prometheus, Grafana, Git, Ansible, Security.
        """,
        "required_skills": [
            "docker", "kubernetes", "aws", "terraform", "ci/cd", "jenkins",
            "linux", "python", "bash", "prometheus", "grafana", "git", "ansible"
        ],
        "nice_to_have": ["gcp", "azure", "helm", "vault", "argocd", "elk stack", "istio"],
        "experience_years": "3-6 years",
        "salary_range": "$100,000 - $155,000",
        "category": "DevOps"
    }
}

# Skills taxonomy for extraction
SKILLS_TAXONOMY = {
    "programming_languages": [
        "python", "java", "javascript", "typescript", "c++", "c#", "r", "scala",
        "go", "rust", "kotlin", "swift", "php", "ruby", "matlab", "bash", "shell"
    ],
    "ml_ai": [
        "machine learning", "deep learning", "neural networks", "nlp",
        "natural language processing", "computer vision", "reinforcement learning",
        "generative ai", "llm", "transformers", "bert", "gpt", "stable diffusion",
        "feature engineering", "model deployment", "mlops", "a/b testing",
        "statistical modeling", "predictive modeling", "time series"
    ],
    "frameworks_libraries": [
        "tensorflow", "pytorch", "keras", "scikit-learn", "pandas", "numpy",
        "matplotlib", "seaborn", "plotly", "opencv", "hugging face", "langchain",
        "django", "fastapi", "flask", "spring boot", "react", "next.js", "vue.js",
        "angular", "node.js", "express.js", "celery", "sqlalchemy", "pydantic"
    ],
    "databases": [
        "sql", "mysql", "postgresql", "sqlite", "mongodb", "redis", "elasticsearch",
        "cassandra", "dynamodb", "snowflake", "bigquery", "oracle", "neo4j",
        "pinecone", "chroma", "weaviate", "vector database"
    ],
    "cloud_devops": [
        "aws", "azure", "gcp", "google cloud", "docker", "kubernetes", "terraform",
        "ansible", "jenkins", "github actions", "ci/cd", "helm", "argocd",
        "mlflow", "kubeflow", "airflow", "spark", "hadoop", "kafka"
    ],
    "tools": [
        "git", "github", "gitlab", "jira", "confluence", "tableau", "power bi",
        "excel", "jupyter", "vscode", "linux", "rest api", "graphql", "figma",
        "postman", "swagger", "prometheus", "grafana", "elk stack"
    ]
}

# Certifications by role
CERTIFICATIONS = {
    "Data Scientist": [
        "Google Professional Data Engineer",
        "AWS Certified Machine Learning Specialty",
        "IBM Data Science Professional Certificate",
        "Coursera Deep Learning Specialization",
        "TensorFlow Developer Certificate"
    ],
    "Data Analyst": [
        "Google Data Analytics Certificate",
        "Microsoft Power BI Data Analyst",
        "Tableau Desktop Specialist",
        "IBM Data Analyst Professional Certificate",
        "AWS Certified Cloud Practitioner"
    ],
    "ML Engineer": [
        "AWS Certified Machine Learning Specialty",
        "Google Professional ML Engineer",
        "MLOps Specialization (Coursera)",
        "Kubeflow Certification",
        "Deep Learning Specialization"
    ],
    "Python Developer": [
        "Python Institute PCEP/PCAP",
        "AWS Certified Developer Associate",
        "Django REST Framework Course",
        "Docker Certified Associate",
        "FastAPI Advanced Course"
    ],
    "AI Engineer": [
        "DeepLearning.AI LangChain Course",
        "OpenAI API Developer Course",
        "AWS Certified AI Practitioner",
        "Hugging Face NLP Course",
        "Vector Database Fundamentals"
    ],
    "Backend Developer": [
        "AWS Certified Developer Associate",
        "Docker Certified Associate",
        "Kubernetes CKA Certification",
        "Spring Professional Certification",
        "MongoDB Developer Certification"
    ],
    "Frontend Developer": [
        "Meta Front-End Developer Certificate",
        "AWS Certified Cloud Practitioner",
        "React Advanced Patterns Course",
        "TypeScript Deep Dive",
        "Google UX Design Certificate"
    ],
    "DevOps Engineer": [
        "AWS Solutions Architect Associate",
        "Certified Kubernetes Administrator (CKA)",
        "HashiCorp Terraform Associate",
        "Docker Certified Associate",
        "Linux Foundation LFCS"
    ]
}
