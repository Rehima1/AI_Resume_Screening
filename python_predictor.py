import sys
import json
import joblib
import spacy
import re
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
import nltk
import PyPDF2

nltk.download('stopwords')
nlp = spacy.load("en_core_web_sm")

# Load models
tfidf_vectorizer = joblib.load('tfidf_vectorizer.pkl')
label_encoder = joblib.load('label_encoder.pkl')
model = joblib.load('resume_screening_model.pkl')

stop_words = set(stopwords.words('english'))

def clean_text(text):
    if text is None:
        return ''
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.lower()
    text = ' '.join([word for word in text.split() if word not in stop_words])
    return text

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = " ".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
    return text

def predict_category(cv_text):
    cv_text_cleaned = clean_text(cv_text)
    cv_vector = tfidf_vectorizer.transform([cv_text_cleaned])
    predicted_label = model.predict(cv_vector)[0]
    category = label_encoder.inverse_transform([predicted_label])[0]
    return category

def extract_key_roles_and_experience(text):
    doc = nlp(text)
    key_roles = [ent.text for ent in doc.ents if ent.label_ in ["ORG", "WORK_OF_ART"]]

    experience_pattern = r"(\d+)\+?\s?(years?|yrs?)\s?(of\s?)?(experience)?"
    experience_matches = re.findall(experience_pattern, text, re.IGNORECASE)
    
    total_experience = sum(int(match[0]) for match in experience_matches) if experience_matches else 0
    avg_experience = total_experience / len(experience_matches) if experience_matches else 0
    
    return key_roles, avg_experience

def evaluate_cv(job_desc, cv_text):
    job_desc_cleaned = clean_text(job_desc)
    cv_text_cleaned = clean_text(cv_text)

    job_vec = tfidf_vectorizer.transform([job_desc_cleaned])
    cv_vec = tfidf_vectorizer.transform([cv_text_cleaned])

    similarity = cosine_similarity(job_vec, cv_vec).flatten()[0]

    doc = nlp(cv_text)
    key_roles = [ent.text for ent in doc.ents if ent.label_ in ["ORG", "WORK_OF_ART"]]
    key_roles, avg_experience = extract_key_roles_and_experience(cv_text)

    return {
        "similarity_score": similarity,
        "key_roles": key_roles,
        "avg_experience": avg_experience
    }

def evaluate_cv_enhanced(job_desc, cv_path):
    cv_text = extract_text_from_pdf(cv_path)
    result = evaluate_cv(job_desc, cv_text)
    
    # Ensure similarity_score is scaled to percentage
    result['similarity_score'] = round(result['similarity_score'] * 100, 2)
    
    return result

if __name__ == "__main__":
    input_data = json.loads(sys.stdin.read())
    resume_path = input_data['resume_path']
    job_desc = input_data['job_desc']
    
    resume_text = extract_text_from_pdf(resume_path)
    category = predict_category(resume_text)
    evaluation = evaluate_cv_enhanced(job_desc, resume_path)
    
    result = {
        'category': category,
        'evaluation': evaluation
    }
    
    print(json.dumps(result))

    # Print the results as requested
    print("\nMatch Score:", result['evaluation']['similarity_score'])
    print("Key Roles Identified:", result['evaluation']['key_roles'])
    print("Average Years of Experience:", result['evaluation']['avg_experience'])