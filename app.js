const express = require('express');
const fileUpload = require('express-fileupload');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 3001;

app.use(fileUpload());
app.use(express.json());
app.use(express.static('public'));

// Serve index.html at the root URL
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

app.post('/upload', (req, res) => {
    if (!req.files?.resume || !req.body.jobDesc) {
        return res.status(400).json({ error: 'Missing resume file or job description' });
    }

    const resume = req.files.resume;
    const jobDesc = req.body.jobDesc;
    const tempFilePath = path.join(__dirname, 'uploads', resume.name);

    resume.mv(tempFilePath, (err) => {
        if (err) {
            console.error('Error moving file:', err);
            return res.status(500).send(err);
        }

        const pythonProcess = spawn('python', ['python_predictor.py']);
        const dataToSend = JSON.stringify({
            job_desc: jobDesc,
            resume_path: tempFilePath
        });

        pythonProcess.stdin.write(dataToSend);
        pythonProcess.stdin.end();

        let result = '';
        pythonProcess.stdout.on('data', (data) => {
            result += data.toString();
        });

        pythonProcess.stderr.on('data', (data) => {
            console.error(`Error from Python script: ${data}`);
        });

        pythonProcess.on('close', (code) => {
            if (code !== 0) {
                return res.status(500).json({ error: 'Processing failed' });
            }
            try {
                const processedData = JSON.parse(result);
                res.json(processedData);
            } catch (e) {
                console.error('Error parsing JSON:', e);
                res.status(500).json({ error: 'Invalid processing output' });
            }

            // Clean up temporary file
            fs.unlink(tempFilePath, (err) => {
                if (err) console.error('Error deleting temp file:', err);
            });
        });
    });
});

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
    if (!fs.existsSync(path.join(__dirname, 'uploads'))) {
        fs.mkdirSync(path.join(__dirname, 'uploads'));
    }
});