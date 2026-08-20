export interface EngineOptions {
  model?: string;
  lang?: string;
  threads?: number;
  vad?: boolean;
  vadThreshold?: number;
  quantization?: string;
  numSpeakers?: number;
  customModelPath?: string;
  [key: string]: any;
}

export interface Segment {
  start: number;
  end: number;
  text: string;
  speaker?: string;
  confidence?: number;
}

export class TranscriptResult {
  text: string;
  segments: Segment[];
  language?: string;
  duration?: number;
  speakers?: string[];

  toJson(): string;
  toSrt(): string;
  toVtt(): string;
  toRttm(fileId?: string): string;
}

export abstract class Engine {
  options: EngineOptions;
  constructor(options?: EngineOptions);
  abstract transcribe(audioPath: string, options?: any): Promise<TranscriptResult>;
  abstract diarize(audioPath: string, numSpeakers?: number): Promise<TranscriptResult>;
  getInfo(): Record<string, any>;
}

export class WhisperEngine extends Engine {
  transcribe(audioPath: string, options?: any): Promise<TranscriptResult>;
  diarize(audioPath: string, numSpeakers?: number): Promise<TranscriptResult>;
}

export class VoskEngine extends Engine {
  transcribe(audioPath: string, options?: any): Promise<TranscriptResult>;
  diarize(audioPath: string, numSpeakers?: number): Promise<TranscriptResult>;
}

export class HybridEngine extends Engine {
  transcribe(audioPath: string, options?: any): Promise<TranscriptResult>;
  diarize(audioPath: string, numSpeakers?: number): Promise<TranscriptResult>;
}

export function createEngine(
  engineName?: 'whisper' | 'vosk' | 'hybrid' | string,
  options?: EngineOptions
): Engine;

export function formatTime(seconds: number, separator?: string): string;
