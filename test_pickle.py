import pickle

def load_pickle_file(file_path):
    try:
        with open(file_path, 'rb') as file:
            return pickle.load(file)
    except pickle.UnpicklingError as e:
        print(f"Unpickling error loading {file_path}: {e}")
    except Exception as e:
        print(f"Error loading {file_path}: {e}")

# Test loading the pickle file
model = load_pickle_file('resume_screening_model.pkl')
if model:
    print("Model loaded successfully")
else:
    print("Failed to load model")
