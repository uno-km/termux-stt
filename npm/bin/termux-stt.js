#!/usr/bin/env node

/**
 * termux-stt CLI for Node.js / npx
 */

const { spawn, spawnSync } = require('child_process');

const args = process.argv.slice(2);

function getPythonExecutable() {
  const candidates = ['python3', 'python'];
  for (const cmd of candidates) {
    try {
      const res = spawnSync(cmd, ['--version'], { stdio: 'ignore' });
      if (res.status === 0) return cmd;
    } catch (_) {}
  }
  return 'python3';
}

const pythonExe = getPythonExecutable();
const pythonArgs = ['-m', 'termux_stt.cli.main', ...args];

const proc = spawn(pythonExe, pythonArgs, {
  stdio: 'inherit',
  env: process.env
});

proc.on('close', (code) => {
  process.exit(code || 0);
});
