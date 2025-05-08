import React, { useState } from 'react';
import SearchInput from './features/SearchInput';

function App() {
  const [query, setQuery] = useState('');

  const handleSearch = (message: string) => {
    console.log('User query:', message);
    setQuery(message);
  }

  return (
    <main className="min-h-screen bg-gray-100 p-6">
      <h1 className="text-2xl font-bold mb-4">Restaurant Finder</h1>
      <SearchInput onSubmit={handleSearch} />
      {query && (
        <div className="mt-6 text-center text-gray-700">
          <p>Searching for: <strong>{query}</strong></p>
        </div>
      )}
    </main>
  );
}

export default App;