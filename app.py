from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
import PyPDF2
import spacy
import pickle
import re
import nltk
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from flask_cors import CORS
import sys
from joblib import load  # Ensure this import for joblib

app = Flask(__name__)
CORS(app)

# Load models with absolute paths and protocol handling
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def load_model_safe(file_name):
    """Universal loader with protocol fallback"""
    file_path = os.path.join(BASE_DIR, file_name)
    try:
        # Try standard joblib load first
        from joblib import load
        return load(file_path)
    except Exception as e:
        print(f"Joblib load failed for {file_name}, attempting pickle5: {str(e)}")
        try:
            # Fallback to pickle5 with proper import
            import pickle5 as pickle
            with open(file_path, 'rb') as f:
                return pickle.load(f)
        except ModuleNotFoundError:
            print("ERROR: Required package 'pickle5' not installed. Run:")
            print("pip install pickle5")
            sys.exit(1)
        except Exception as pe:
            print(f"Failed to load {file_name} with pickle5: {str(pe)}")
            sys.exit(1)

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = " ".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
    return text

# Function to clean text
def clean_text(text):
    if text is None:
        return ''
    text = re.sub(r'\W', ' ', text)  # Remove special characters
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
    text = text.lower()  # Convert to lowercase
    return text

# Function to evaluate CV
def evaluate_cv(job_desc, cv_path):
    job_desc_clean = clean_text(job_desc)
    cv_text = extract_text_from_pdf(cv_path)
    cv_text_clean = clean_text(cv_text)

    # Vectorize and calculate similarity score
    job_desc_vec = vectorizer.transform([job_desc_clean])
    cv_vec = vectorizer.transform([cv_text_clean])
    similarity_score = cosine_similarity(job_desc_vec, cv_vec)[0][0]

    # Extract key roles (sample logic, you can customize it)
    doc = nlp(cv_text)
    key_roles = [ent.text for ent in doc.ents if ent.label_ in ["ORG", "WORK_OF_ART"]]

    # Extract experience
    experience_pattern = r"(\d+)\+?\s?(years?|yrs?)\s?(of\s?)?(experience)?"
    experience_matches = re.findall(experience_pattern, cv_text, re.IGNORECASE)
    total_experience = sum(int(match[0]) for match in experience_matches) if experience_matches else 0
    avg_experience = total_experience / len(experience_matches) if experience_matches else 0

    # Predict job category
    job_category = model.predict(cv_vec)
    job_category_label = label_encoder.inverse_transform(job_category)[0]

    return {
        "similarity_score": similarity_score,
        "key_roles": key_roles,
        "avg_experience": avg_experience,
        "job_category": job_category_label
    }

# Route for uploading job description and resume
@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        job_desc = request.form.get('job_desc')
        resume_file = request.files.get('resume')

        if not resume_file or not job_desc:
            return jsonify({"error": "Missing file or job description"}), 400

        # Create upload directory if it doesn't exist
        upload_dir = 'uploads'
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        # Save the uploaded file
        filename = secure_filename(resume_file.filename)
        resume_path = os.path.join(upload_dir, filename)
        resume_file.save(resume_path)

        # Process the resume
        result = evaluate_cv(job_desc, resume_path)

        # Delete the uploaded file after processing
        os.remove(resume_path)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
