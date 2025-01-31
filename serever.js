const express = require('express');
const multer = require('multer');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();
app.use(cors());
app.use(express.json());

// Configure file storage
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, 'uploads/');
  },
  filename: (req, file, cb) => {
    cb(null, `${Date.now()}-${file.originalname}`);
  }
});

const upload = multer({ storage });

// Store resume data in memory (replace with database in production)
let resumes = [];

// API Endpoints
app.post('/upload', upload.single('resume'), (req, res) => {
  // Here you would add resume parsing logic
  const newResume = {
    id: Date.now(),
    filename: req.file.originalname,
    path: req.file.path,
    status: 'new',
    skills: ['Sample Skill 1', 'Sample Skill 2'], // Parse from file
    experience: 3 // Extract from file
  };
  
  resumes.push(newResume);
  res.status(201).json(newResume);
});

app.get('/resumes', (req, res) => {
  res.json(resumes);
});

app.get('/metrics', (req, res) => {
  const metrics = {
    total: resumes.length,
    avgExperience: resumes.reduce((sum, r) => sum + r.experience, 0) / resumes.length || 0,
    matchRate: (resumes.filter(r => r.status === 'approved').length / resumes.length * 100) || 0
  };
  res.json(metrics);
});

app.listen(3001, () => {
  console.log('Server running on port 3001');
});