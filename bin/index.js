#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');

// Point this directly to your root 'hwfinance' Python script
const scriptPath = path.join(__dirname, '../hwfinance');

// Spawn python3 to run your script, passing along any trailing terminal arguments
const pythonProcess = spawn('python3', [scriptPath, ...process.argv.slice(2)], {
    stdio: 'inherit' // Passes terminal inputs and color outputs straight to the user
});

pythonProcess.on('error', (err) => {
    console.error('Failed to run hwfinance core engine:', err);
});
