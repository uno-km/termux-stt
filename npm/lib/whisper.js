/**
 * WhisperEngine for Node.js - wraps whisper.cpp via spawn or termux-stt CLI
 */

const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const { Engine, TranscriptResult, Segment } = require('./engine');

class WhisperEngine extends Engine {
  constructor(config = {}) {
    super(config);
    this.model = config.model || 'base';
    this.lang = config.lang || 'ko';
    this.device = config.device || 'auto';
    this.threads = config.threads || 4;

    try {
      const avr = require('@ameva/runtime');
      this.ctx = avr.getOrCreateContext({ device: this.device });
    } catch (e) {
      this.ctx = null;
    }
  }

  async transcribe(audioPath, options = {}) {
    return new Promise((resolve, reject) => {
      // Use termux-stt python CLI or direct whisper.cpp
      const args = [
        '-m', 'termux_stt.cli.main',
        'transcribe',
        '--engine', 'whisper',
        '--model', this.model,
        '--lang', this.lang,
        '--device', String(this.device),
        '--format', 'json',
        audioPath
      ];

      const proc = spawn('python', args, { env: process.env });
      let stdout = '';
      let stderr = '';

      proc.stdout.on('data', (d) => { stdout += d.toString(); });
      proc.stderr.on('data', (d) => { stderr += d.toString(); });

      proc.on('close', (code) => {
        if (code !== 0) {
          return reject(new Error(`whisper transcription failed (code ${code}): ${stderr}`));
        }
        try {
          const parsed = JSON.parse(stdout);
          const segments = (parsed.segments || []).map(
            s => new Segment(s.start, s.end, s.text, s.speaker, s.confidence)
          );
          resolve(new TranscriptResult(parsed.text, segments, parsed.language || this.lang, parsed.duration));
        } catch (e) {
          // Fallback if stdout was plain text
          resolve(new TranscriptResult(stdout.trim(), [new Segment(0, 0, stdout.trim())], this.lang));
        }
      });
    });
  }

  getInfo() {
    const info = {
      name: 'whisper.cpp (Node.js)',
      model: this.model,
      language: this.lang,
      device: this.device,
      threads: this.threads
    };
    if (this.ctx) {
      info.backendType = this.ctx.backendType;
      info.isGpu = this.ctx.isGpu;
      info.deviceName = this.ctx.deviceName;
    }
    return info;
  }
}

module.exports = { WhisperEngine };
