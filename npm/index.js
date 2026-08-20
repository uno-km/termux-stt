/**
 * termux-stt Node.js entry point
 */

const { Engine, TranscriptResult, Segment, formatTime } = require('./lib/engine');
const { WhisperEngine } = require('./lib/whisper');
const { VoskEngine } = require('./lib/vosk');
const { HybridEngine } = require('./lib/hybrid');

function createEngine(engineName = 'whisper', options = {}) {
  const name = String(engineName).toLowerCase();
  switch (name) {
    case 'whisper':
      return new WhisperEngine(options);
    case 'vosk':
      return new VoskEngine(options);
    case 'hybrid':
      return new HybridEngine(options);
    default:
      throw new Error(`Unknown engine: ${engineName}. Available: whisper, vosk, hybrid`);
  }
}

module.exports = {
  createEngine,
  Engine,
  TranscriptResult,
  Segment,
  WhisperEngine,
  VoskEngine,
  HybridEngine,
  formatTime
};
