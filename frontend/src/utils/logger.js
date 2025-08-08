const levels = { log: 0, warn: 1, error: 2, silent: 3 };

const envLevel = import.meta.env.VITE_LOG_LEVEL || (import.meta.env.PROD ? 'silent' : 'log');
const currentLevel = levels[envLevel] ?? levels.log;

function createLogger(level, method) {
  return (message, details) => {
    if (level < currentLevel) return;
    if (details !== undefined) {
      method(message, details);
    } else {
      method(message);
    }
  };
}

export const log = createLogger(levels.log, console.log);
export const warn = createLogger(levels.warn, console.warn);
export const error = createLogger(levels.error, console.error);

export default { log, warn, error };
