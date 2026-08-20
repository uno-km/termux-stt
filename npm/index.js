/**
 * termux-stt Node.js entry point
 */

function createEngine(engineName, options = {}) {
    return {
        transcribe: async (audioPath) => {
            console.log(`[Stub] Transcribing ${audioPath} using ${engineName} engine...`);
            return {
                text: "Stub transcription result",
                segments: []
            };
        }
    };
}

module.exports = {
    createEngine
};
