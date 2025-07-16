import React, { useState } from 'react';
import RAGSetup from './components/RAGSetup';
import Sidebar from './components/Sidebar';
import EchoOfDelphi from './components/EchoOfDelphi';
import EchoForge from './components/EchoForge';
import './App.css';

function App() {
    const [setupComplete, setSetupComplete] = useState(false);

    const [currentPage, setCurrentPage] = useState('Echo of Delphi'); // Default page

    const [mdSource, setMdSource] = useState('');

    const renderContent = () => {
        switch (currentPage) {
            case 'Echo of Delphi':
                return <EchoOfDelphi />;
            case 'Echo Forge':
                return <EchoForge />;
            default:
                return <p>A wrong slip and now you find yourself in Tartarus...!</p>;
        }
    };

    const getFolderName = (fullPath) => {
        if (!fullPath) return '';
        const parts = fullPath.split(/[/\\]+/); // handles both \ and /
        return parts[parts.length - 1];
    };

    return (
        <div className="app-root">

            {!setupComplete || currentPage === 'Rekindle the Echoes' ? (
                <div className="load-config-overlay">
                    <div className="load-config-content">
                        <RAGSetup onSuccess={(mdSource) => {
                            setSetupComplete(true);
                            setMdSource(getFolderName(mdSource));
                            console.log('RAG setup successful, source path:', mdSource);
                            setCurrentPage('Echo of Delphi');
                        }} />
                    </div>
                </div>
            ) : setupComplete && (
                <>
                    <Sidebar
                        currentPage={currentPage}
                        onNavigate={setCurrentPage}
                        markdownSource={mdSource}
                    />
                    <div className="current-page-content">
                        {renderContent()}
                    </div>
                </>
            )}

        </div>
    );
}

export default App;
