import React, { useState, useRef } from 'react';
import '../stylesheets/App.css';

const Search = ({ submitSearch }) => {
  const [query, setQuery] = useState('');
  const searchInput = useRef(null);

  const getInfo = (event) => {
    event.preventDefault();
    submitSearch(query);
  };

  const handleInputChange = () => {
    setQuery(searchInput.current.value);
  };

  return (
    <form onSubmit={getInfo} className='search-form'>
      <input
        type='text'
        placeholder='Search questions...'
        ref={searchInput}
        onChange={handleInputChange}
      />
      <input type='submit' value='Submit' />
    </form>
  );
};

export default Search;