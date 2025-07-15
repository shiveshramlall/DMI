import { useState } from 'react';
import './Sidebar.css';
import { Menu, PanelLeftClose, ScrollText } from 'lucide-react';

function Sidebar({ currentPage, onNavigate, markdownSource }) {
  const [collapsed, setCollapsed] = useState(false);

  const topMenuItems = ['Echo of Delphi', 'Echo Forge'];
  const bottomMenuItem = 'Rekindle the Echoes';

  return (
    <div className={`sidebar ${collapsed ? 'collapsed' : 'expanded'}`}>
      <div className="sidebar-header">
        <div className="sidebar-logo">
          <ScrollText size={24} />
          {!collapsed && <span className="logo-text">DMI</span>}
        </div>
        <button className="toggle-sidebar-btn" onClick={() => setCollapsed(!collapsed)}>
          {collapsed ? <Menu /> : <PanelLeftClose />}
        </button>
      </div>

      {!collapsed && (
        <>
          <ul className="sidebar-items">
            {topMenuItems.map(item => (
              <li
                key={item}
                className={item === currentPage ? 'active' : ''}
                onClick={() => onNavigate(item)}
                style={{ cursor: 'pointer' }}
              >
                {item}
              </li>
            ))}
          </ul>

          <div className="sidebar-bottom">
            <li
              className={bottomMenuItem === currentPage ? 'active' : ''}
              onClick={() => onNavigate(bottomMenuItem)}
              style={{ cursor: 'pointer', listStyle: 'none' }}
            >
              <div style={{ display: 'flex', flexDirection: 'column', gap: '2px' }}>
                {markdownSource && (
                  <div className="markdown-source">
                    <small>📄 {markdownSource}</small>
                  </div>
                )}
                <div className="bottom-label">{bottomMenuItem}</div>
              </div>
            </li>

          </div>
        </>
      )}
    </div>
  );
}

export default Sidebar;
