import React, { useState } from 'react';
import './Sidebar.css';

function Sidebar({ currentPage, onNavigate }) {
  const [collapsed, setCollapsed] = useState(false);

  const topMenuItems = ['Echo of Delphi', 'Echo Forge'];
  const bottomMenuItem = 'Rekindle the Echoes';

  return (
    <div className={`sidebar ${collapsed ? 'collapsed' : ''}`}>
      <button className="toggle-btn" onClick={() => setCollapsed(!collapsed)}>
        {collapsed ? '☰' : '×'}
      </button>

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
              {bottomMenuItem}
            </li>
          </div>
        </>
      )}
    </div>
  );
}

export default Sidebar;
