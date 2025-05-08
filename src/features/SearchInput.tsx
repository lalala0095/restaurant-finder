import React, { useState } from 'react';

type SearchInputProps = {
  onSubmit: (message: string) => void;
};

const SearchInput: React.FC<SearchInputProps> = ({ onSubmit }) => {
  const [message, setMessage] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!message.trim()) return;
    onSubmit(message);
    setMessage('');
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="w-full max-w-xl mx-auto flex gap-2 items-center"
    >
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="e.g. Find me a cheap sushi place in LA."
        className="flex-1 p-3 rounded-xl border border-gray-300 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
    <button 
    type="submit"
    className="px-4 py-2 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition"
    >Search</button>
        </form>
    );
};

export default SearchInput;
