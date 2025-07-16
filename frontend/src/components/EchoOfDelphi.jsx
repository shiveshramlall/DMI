import React, { useState } from 'react';
import axios from 'axios';
import './EchoOfDelphi.css';
import ReactMarkdown from 'react-markdown'

function EchoOfDelphi() {
    const [query, setQuery] = useState('');
    const [topK, setTopK] = useState(5);

    const [response, setResponse] = useState(null);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleAsk = async (e) => {
        e.preventDefault();

        if (!query.trim()) {
            setError('Please enter a query.');
            setResponse(null);
            return;
        }

        setLoading(true);
        setError(null);
        setResponse(null);

        try {
            const res = await axios.post('http://localhost:5000/ask', {
                query,
                top_k: topK,
            });

            setResponse(res.data);
        } catch (err) {

            setError(err.response?.data?.error || err.message || 'Error asking query.');
        } finally {
            setLoading(false);
        }

    };

    return (
        <div className="query-container">

            <h1>Echo of Delphi</h1>
            <p className="page_description">
                You ascend the slopes of Mount Parnassus, where white marble columns rise from crumbling, forgotten temples.<br />
                Amid the ruins, you find the Echo of Delphi. A still, luminous pool of ancient knowledge.<br />
                As you gaze into its depths, distant voices stir… whispering of all that has been forgotten,<br />
                and all that has yet to be revealed...
            </p>

            <form onSubmit={handleAsk}>
                <div className="query-form-header">
                    <label htmlFor="query">What wisdom do you seek?</label>
                    <div className="topk-inline">
                        <label htmlFor="topK">Echoes to Consult:</label>
                        <input
                            type="number"
                            id="topK"
                            value={topK}
                            min={1}
                            max={30}
                            onChange={(e) => setTopK(Number(e.target.value))}
                            required
                        />
                    </div>
                </div>

                <div className="query-form-text">
                    <textarea
                        id="query"
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        rows={4}
                        placeholder="Cast your thoughts into the pool, that the Oracle may stir."
                        required
                    />
                </div>

                <button type="submit" disabled={loading}>
                    {loading ? 'The water funnels upward, rising with the Oracle’s swirling echoes....' : 'Invoke the Oracle'}
                </button>
            </form>

            {error && <p className="error-message">{error}</p>}

            {response && (
                <div className="query-response-container">
                    <h3>🜄 Oracle’s Insight</h3>

                    <div className="query-answer">
                        <ReactMarkdown>{response.answer}</ReactMarkdown>
                    </div>

                    {response.references && response.references.length > 0 && (
                        <div className="query-references">
                            <h4>↳ Echoes:</h4>
                            <ul>
                                {response.references.map((ref, index) => (
                                    <li key={index}>
                                        <ReactMarkdown>{ref}</ReactMarkdown>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}

export default EchoOfDelphi;
