import React, { useState } from "react";
import './EchoForge.css';

const generatorOptions = [
  { label: "NPC", value: "npc" },
  { label: "Location", value: "location" },
  { label: "Puzzle", value: "puzzle" },
  { label: "Item", value: "item" },
  { label: "Rumour", value: "rumour" },
  { label: "Name", value: "name" },
];

function Generators() {
  const [generator, setGenerator] = useState("npc");
  const [numResults, setNumResults] = useState(1);
  const [echoes, setEchoes] = useState(3);
  const [queryText, setQueryText] = useState(""); // textarea input
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleGenerate = async () => {
    setLoading(true);
    setError(null);
    setResults([]);

    try {
      const response = await fetch(`http://localhost:5000/gen/${generator}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          top_k: numResults,
          // num_results: echoes,
          query: queryText,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.error || "Something went wrong.");
      } else {
        const key = Object.keys(data)[0];
        const value = data[key];
        setResults(Array.isArray(value) ? value : [value]);
      }
    } catch (err) {
      setError("Failed to connect to server.");
    } finally {
      setLoading(false);
    }

  };

  return (
    <div className="echo-container">
      <h1>Echo Forge</h1>
      <p className="page_description">You wander into the Echo Forge, deep beneath Mount Parnassus, where Hephaestus’s eternal fires blaze.<br />
      Sparks fly as the divine smith molds new life, while the Fates thread their needles into it.<br />
      Oval shapes of blue energy radiate before you...</p>

      <div className="form-header inline-form">
        <div className="form-block">
          <label>
            <span className="label-text">Cast your desire into the flame</span>
            <select
              value={generator}
              onChange={(e) => setGenerator(e.target.value)}
            >
              {generatorOptions.map((opt) => (
                <option key={opt.value} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
          </label>
        </div>

        <div className="form-block small">
          <label>
            <span className="label-text">Past Echoes</span>
            <input
              type="number"
              value={echoes}
              onChange={(e) => setEchoes(parseInt(e.target.value))}
              min={1}
              max={20}
            />
          </label>
        </div>
      </div>

      <div className="form-group">
        <label htmlFor="query">Let your words strike the anvil, and that the fates may hear...</label>
        <textarea
          id="query"
          value={queryText}
          onChange={(e) => setQueryText(e.target.value)}
          placeholder="Call forth what lies hidden in the embers..."
          rows={4}
        />
      </div>

      <button
        type="submit"
        onClick={handleGenerate}
        disabled={loading}
      >
        {loading ? "Threads wave from the fates as they sprial around the hammer of the almighty Hephaestus..." : "Forge!"}
      </button>

      {error && <div className="error-message">{error}</div>}

      {results.length > 0 && (
        <div className="response-container">
          <h3>🜂 Your creations await</h3>
          {results.map((res, idx) => (
            <div key={idx} className="oracle-answer-card">
              {typeof res === "string" ? (
                <p>{res}</p>
              ) : res && typeof res === "object" ? (
                Object.entries(res).map(([key, value]) => (
                  <div key={key} className="oracle-row">
                    <span className="oracle-key">{key}:</span>
                    <span className="oracle-value">
                      {typeof value === "string" && value.includes("\n") ? (
                        <ReactMarkdown>{value}</ReactMarkdown>
                      ) : (
                        value.toString()
                      )}
                    </span>
                  </div>
                ))
              ) : (
                <pre>{JSON.stringify(res, null, 2)}</pre>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );

}

export default Generators;
