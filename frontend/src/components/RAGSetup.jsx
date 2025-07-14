import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './RAGSetup.css';


function RAGSetup({ onSuccess }) {

    const [modelChat, setModelChat] = useState('llama3.1:8b');
    const [modelEmbed, setModelEmbed] = useState('mxbai-embed-large');
    const [mdSource, setMdSource] = useState('C:\\Users\\shive\\OneDrive\\Documents\\DnD\\Adventures\\Stone-Heart Hollow');

    const [error, setError] = useState(null);

    const [loading, setLoading] = useState(false);

    const apiSetup = async () => {
        try {
            setError(null); // Clear previous errors
            const response = await axios.post('http://localhost:5000/setup', {
                modelChat,
                modelEmbed,
                mdSource
            });
            console.log('Setup response:', response.status);
            if (response.status === 200) {
                alert('RAG setup successful!');
                if (onSuccess) onSuccess(); 
            } else {
                setError(response.data.error || 'Setup failed.');
            }
        } catch (error) {
            setError(error.message || 'An error occurred during setup.');
        }
    };

    const handleSubmit = async (event) => {

        event.preventDefault(); // Prevent default form submission behavior

        setError(''); 
        if (!modelChat || !modelEmbed || !mdSource) {
            setError('Please provide all inputs.');
            return;
        };

        setLoading(true); // Start loading

        try {
            await apiSetup();
            console.log('Current error:', error);
        } finally {
            setLoading(false); // Always stop loading, even on error
        }

    };

    
    return (
        <div className="api-setup-container">
            <h1>At the Foothills of Parnassus</h1>
            <p>
            Echoes stir within your soul as the mist parts before you. The path to Mount Parnassus reveals itself... a sacred summit that yields only to purpose.
            </p>
            <h2>Awaken your Echo Source</h2>
            {error && <p className="error-message">{error}</p>}
            <form onSubmit={handleSubmit}>
                <div className="api-setup-group">
                    <label htmlFor="modelChat">Model for Chat:</label>
                    <input
                        type="text"
                        id="modelChat"
                        value={modelChat}
                        onChange={(e) => setModelChat(e.target.value)}
                        required
                    />
                </div>
                <div className="api-setup-group">
                    <label htmlFor="modelEmbed">Model for Embedding:</label>
                    <input
                        type="text"
                        id="modelEmbed"
                        value={modelEmbed}
                        onChange={(e) => setModelEmbed(e.target.value)}
                        required
                    />
                </div>
                <div className="api-setup-group">
                    <label htmlFor="mdSource">Markdown Files Location:</label>
                    <input
                        type="text"
                        id="mdSource"
                        value={mdSource}
                        onChange={(e) => setMdSource(e.target.value)}
                        required
                    />
                </div>
                <button type="submit" disabled={loading} className="api-button">
                    {loading ? "Awakening..." : "Awake"}
                </button>
            </form>
        </div>
    );
}

export default RAGSetup;