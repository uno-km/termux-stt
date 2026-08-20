/**
 * VoskEngine for Node.js
 */

const { spawn } = require('child_process');
const { Engine, TranscriptResult, Segment } = require('./engine');

class VoskEngine extends Engine {
  constructor(config = {}) {
    super(config);
    this.model = config.model || 'small-ko-0.22';
    this.lang = config.lang || 'ko';
  }

  async transcribe(audioPath, options = {}) {
    return new Promise((resolve, reject) => {
      const args = [
        '-m', 'termux_stt.cli.main',
        'transcribe',
        '--engine', 'vosk',
        '--model', this.model,
        '--lang', this.lang,
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
          return reject(new Error(`Vosk transcription failed (code ${code}): ${stderr}`));
        }
        try {
          const parsed = JSON.parse(stdout);
          const segments = (parsed.segments || []).map(
            s => new Segment(s.start, s.end, s.text, s.speaker, s.confidence)
          );
          resolve(new TranscriptResult(parsed.text, segments, parsed.language || this.lang, parsed.duration));
        } catch (e) {
          resolve(new TranscriptResult(stdout.trim(), [new Segment(0, 0, stdout.trim())], this.lang));
        }
      });
    });
  }

  getInfo() {
    return {
      name: 'Vosk (Node.js)',
      model: this.model,
      language: this.lang
    };
  }
}

module.exports = { VoskEngine };
