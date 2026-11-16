"""
Skills Taxonomy and Semantic Knowledge Base.
Contains curated technical skills, soft skills, certifications, and synonym mappings.
Academic context: Unit 1 & Unit 2 (Information Extraction & Lexical Taxonomies).
"""

from typing import Dict, List, Set, Optional

SKILLS_TAXONOMY = {
    "Machine Learning & AI": [
        "Machine Learning", "Deep Learning", "Natural Language Processing", "NLP", 
        "Computer Vision", "Reinforcement Learning", "Generative AI", "LLMs", 
        "Large Language Models", "Prompt Engineering", "Fine-Tuning", "RAG", 
        "Retrieval-Augmented Generation", "Transformers", "BERT", "GPT", "Gemini", 
        "LLaMA", "LangChain", "LlamaIndex", "Hugging Face", "PyTorch", "TensorFlow", 
        "Keras", "Scikit-Learn", "XGBoost", "LightGBM", "CatBoost", "FastAI", 
        "Spacy", "NLTK", "OpenCV", "Gensim", "FAISS", "ChromaDB", "Pinecone", "Milvus",
        "Vector Databases", "Embeddings", "Sentence-BERT", "Diffusion Models", "GANs"
    ],
    "Data Science & Analytics": [
        "Python", "R", "SQL", "Pandas", "NumPy", "SciPy", "Matplotlib", "Seaborn", 
        "Plotly", "Statistics", "Probability", "Hypothesis Testing", "A/B Testing", 
        "Exploratory Data Analysis", "EDA", "Data Cleaning", "Feature Engineering", 
        "Dimensionality Reduction", "PCA", "t-SNE", "Tableau", "Power BI", "Excel", 
        "Apache Spark", "PySpark", "Hadoop", "Airflow", "ETL", "Data Pipelines", "BigQuery"
    ],
    "Software Development & Backend": [
        "Python", "Java", "C++", "C#", "C", "Go", "Golang", "Rust", "Node.js", 
        "FastAPI", "Flask", "Django", "Spring Boot", "REST APIs", "GraphQL", 
        "Microservices", "Object-Oriented Programming", "OOP", "Data Structures", 
        "Algorithms", "Design Patterns", "Unit Testing", "PyTest", "gRPC"
    ],
    "Frontend & Web": [
        "JavaScript", "TypeScript", "React", "React.js", "Next.js", "Vue.js", "Angular", 
        "HTML", "HTML5", "CSS", "CSS3", "Tailwind CSS", "Bootstrap", "Redux", "Webpack", 
        "Streamlit", "Gradio", "WebSockets"
    ],
    "Database & Cloud Infrastructure": [
        "PostgreSQL", "MySQL", "SQLite", "MongoDB", "Redis", "Cassandra", "Neo4j", 
        "Oracle", "DynamoDB", "AWS", "Amazon Web Services", "Azure", "Google Cloud", 
        "GCP", "Docker", "Kubernetes", "K8s", "CI/CD", "GitHub Actions", "Jenkins", 
        "Terraform", "Linux", "Git", "Bash", "Shell Scripting"
    ],
    "Soft Skills & Management": [
        "Agile", "Scrum", "Problem Solving", "Critical Thinking", "Team Leadership", 
        "Cross-functional Collaboration", "Communication", "Project Management", 
        "Code Review", "Mentorship", "Documentation"
    ]
}

# Synonyms and Canonical Mapping
SKILL_SYNONYMS = {
    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",
    "psql": "PostgreSQL",
    "sklearn": "Scikit-Learn",
    "scikit learn": "Scikit-Learn",
    "scikit-learn": "Scikit-Learn",
    "tf": "TensorFlow",
    "tensorflow": "TensorFlow",
    "pytorch": "PyTorch",
    "torch": "PyTorch",
    "sbert": "Sentence-BERT",
    "sentence transformers": "Sentence-BERT",
    "sentence-transformers": "Sentence-BERT",
    "nlp": "Natural Language Processing",
    "natural language processing": "Natural Language Processing",
    "llm": "Large Language Models",
    "llms": "Large Language Models",
    "large language models": "Large Language Models",
    "genai": "Generative AI",
    "generative ai": "Generative AI",
    "rag": "Retrieval-Augmented Generation",
    "retrieval augmented generation": "Retrieval-Augmented Generation",
    "retrieval-augmented generation": "Retrieval-Augmented Generation",
    "k8s": "Kubernetes",
    "kubernetes": "Kubernetes",
    "gcp": "Google Cloud",
    "google cloud platform": "Google Cloud",
    "aws": "Amazon Web Services",
    "amazon web services": "Amazon Web Services",
    "js": "JavaScript",
    "javascript": "JavaScript",
    "ts": "TypeScript",
    "typescript": "TypeScript",
    "py": "Python",
    "python": "Python",
    "relational database": "SQL",
    "relational databases": "SQL",
    "rdbms": "SQL",
    "nosql": "MongoDB",
    "cv": "Computer Vision",
    "computer vision": "Computer Vision",
    "eda": "Exploratory Data Analysis",
    "bi": "Business Intelligence",
    "powerbi": "Power BI",
    "power bi": "Power BI"
}

# Educational Degrees Mapping
EDUCATION_PATTERNS = {
    "phd": "Doctorate / Ph.D.",
    "doctor of philosophy": "Doctorate / Ph.D.",
    "ph.d": "Doctorate / Ph.D.",
    "master": "Master's Degree",
    "masters": "Master's Degree",
    "m.tech": "Master's Degree",
    "mtech": "Master's Degree",
    "m.s": "Master's Degree",
    "ms": "Master's Degree",
    "msc": "Master's Degree",
    "m.sc": "Master's Degree",
    "mca": "Master's Degree",
    "bachelor": "Bachelor's Degree",
    "bachelors": "Bachelor's Degree",
    "b.tech": "Bachelor's Degree",
    "btech": "Bachelor's Degree",
    "b.e": "Bachelor's Degree",
    "be": "Bachelor's Degree",
    "b.s": "Bachelor's Degree",
    "bs": "Bachelor's Degree",
    "bsc": "Bachelor's Degree",
    "b.sc": "Bachelor's Degree",
    "bca": "Bachelor's Degree"
}

# All flat skills in a lookup set (lowercased)
FLAT_SKILLS_MAP: Dict[str, str] = {}
for category, skills in SKILLS_TAXONOMY.items():
    for s in skills:
        FLAT_SKILLS_MAP[s.lower()] = s

for syn, canon in SKILL_SYNONYMS.items():
    FLAT_SKILLS_MAP[syn.lower()] = canon


def get_canonical_skill(skill_str: str) -> Optional[str]:
    """Return the standardized canonical name of a skill if recognized."""
    cleaned = skill_str.strip().lower()
    return FLAT_SKILLS_MAP.get(cleaned, skill_str.strip().title())
