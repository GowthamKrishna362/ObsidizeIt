import { useEffect, useState } from "react";
import { RUNTIME_MESSAGES } from "./constants";
import "./styles/App.scss";

type RuntimeMessage = {
  id: number;
  text: string;
  type: keyof typeof RUNTIME_MESSAGES;
};

type ThemeType = 'light' | 'dark';

function App() {
  const [input, setInput] = useState<string>("");
  const [theme, setTheme] = useState<ThemeType>('dark');

  useEffect(() => {
    // Set initial theme to dark
    document.documentElement.setAttribute('data-theme', 'dark');
    
    chrome.runtime.onMessage.addListener((message: RuntimeMessage) => {
      if (message.type === RUNTIME_MESSAGES.ADD_TO_OBSIDIZER) {
        setInput((prev) => prev + "\n" + message.text);
      }
    });
  }, []);

  const toggleTheme = () => {
    const newTheme = theme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
    document.documentElement.setAttribute('data-theme', newTheme);
  };

  const handleObsidize = async () => {
    if (!input.trim()) {
      return;
    }

    try {
       fetch("http://localhost:5000/obsidize", {
        method: "POST",
        body: JSON.stringify({
          input: input,
        }),
        headers: {
          "Content-Type": "application/json",
        },
      });
      setInput("");
    } catch (error) {
      console.error('Error obsidizing text:', error);
    }
  };

  const handleClear = () => {
    setInput("");
  };

  return (
    <div className="obsidize-app fade-in">
      <div className="obsidize-header">
        <div className="header-top">
          <div className="logo">📝</div>
          <button 
            className="theme-toggle"
            onClick={toggleTheme}
            aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} theme`}
          >
            {theme === 'light' ? '🌙' : '☀️'}
          </button>
        </div>
        <h1 className="title">ObsidizeIt</h1>
      </div>
      
      <div className="obsidize-content">
        <div className="input-container">
          <label className="input-label" htmlFor="text-input">
            Enter your text to obsidize:
          </label>
          <textarea
            id="text-input"
            className="text-input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Paste your text here or use the browser extension to add content..."
          />
        </div>
        
        <div className="action-buttons">
          <button
            className="obsidize-btn"
            onClick={handleObsidize}
            disabled={!input.trim()}
          >
            Obsidize
          </button>
          <button
            className="clear-btn"
            onClick={handleClear}
          >
            Clear
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
