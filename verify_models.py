import os
import sys
from joblib import load
import pickle

def verify_model(file_path):
    try:
        print(f"\nVerifying {os.path.basename(file_path)}:")
        # Try joblib first
        try:
            obj = load(file_path)
            print("✅ Loaded successfully with joblib")
            return
        except:
            pass
        
        # Try pickle with different protocols
        with open(file_path, 'rb') as f:
            for proto in range(5, 0, -1):
                try:
                    obj = pickle.load(f)
                    print(f"✅ Loaded successfully with pickle protocol {proto}")
                    return
                except:
                    f.seek(0)
        print("❌ All loading attempts failed")
    except Exception as e:
        print(f"🚨 Verification failed: {str(e)}")

if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.dirname(__file__))
    files = [
        'resume_screening_model.pkl',
        'tfidf_vectorizer.pkl',
        'label_encoder.pkl'
    ]
    
    for file in files:
        verify_model(os.path.join(base_dir, file))