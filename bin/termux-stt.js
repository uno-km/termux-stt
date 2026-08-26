#!/usr/bin/env node

/**
 * termux-stt CLI for Node.js / npx
 */

const { spawn } = require('child_process');

const args = process.argv.slice(2);

// Forward to Python CLI
const pythonArgs = ['-m', 'termux_stt.cli.main', ...args];
const proc = spawn('python', pythonArgs, {
  stdio: 'inherit',
  env: process.env
});

proc.on('close', (code) => {
  process.exit(code || 0);
});
