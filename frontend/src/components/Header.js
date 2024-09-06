import React, { useCallback } from 'react';
import '../stylesheets/Header.css';

const Header = () => {
  const navTo = useCallback((uri) => {
    window.location.href = window.location.origin + uri;
  }, []);

  return (
    <div className='App-header'>
      <h1 className='clickable' onClick={() => navTo('')}>Udacitrivia</h1>
      <h2 className='clickable' onClick={() => navTo('')}>List</h2>
      <h2 className='clickable' onClick={() => navTo('/add')}>Add</h2>
      <h2 className='clickable' onClick={() => navTo('/play')}>Play</h2>
    </div>
  );
};

export default Header;