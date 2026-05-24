#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');

const scriptPath = path.join(__dirname, '../hwfinance');

const pythonProcess = spawn('python3', [scriptPath, ...process.argv.slice(2)], {
    stdio: 'inherit'
});

pythonProcess.on('error', (err) => {
    console.error('CRITICAL: Failed to initialize hwfinance core engine.');
    console.error('Ensure python3 is installed and accessible in your system PATH.');
    process.exit(1);
});

pythonProcess.on('close', (code) => {
    process.exit(code);
});
