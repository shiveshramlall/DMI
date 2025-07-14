import React, { useState } from 'react';
import RAGSetup from './components/RAGSetup';
import Sidebar from './components/Sidebar';
import EchoOfDelphi from './components/EchoOfDelphi';
import EchoForge from './components/EchoForge';
import './App.css';

function App() {
    const [setupComplete, setSetupComplete] = useState(false);

    const [currentPage, setCurrentPage] = useState('Echo of Delphi'); // Default page

    const renderContent = () => {
        switch (currentPage) {
            case 'Echo of Delphi':
                return <EchoOfDelphi />;
            case 'Echo Forge':
                return <EchoForge />;
            case 'Rekindle the Echoes':
                return <RAGSetup onSuccess={() => setSetupComplete(true)} />;
            default:
                return <p>Welcome!</p>;
        }
    };

    return (
        <div className="app-root">

            {!setupComplete || currentPage === 'Rekindle the Echoes' ? (
                <div className="modal-overlay">
                    <div className="modal-content">
                        <RAGSetup onSuccess={() => {
                            setSetupComplete(true);
                            setCurrentPage('Echo of Delphi'); 
                        }} />
                    </div>
                </div>
            ) : setupComplete && (
                <>
                    <Sidebar currentPage={currentPage} onNavigate={setCurrentPage} />
                    <div className="main-content">
                        {renderContent()}
                    </div>
                </>
            )}

        </div>
    );
}

export default App;
