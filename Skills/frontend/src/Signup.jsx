import React, { useState } from 'react';
export function Signup({ onSubmit }) {
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  return <form onSubmit={e => { e.preventDefault(); if (!email.includes('@')) { setError('Enter a valid email'); return; } setError(''); onSubmit(email); }} noValidate>
    <label htmlFor="email">Email</label><input id="email" value={email} onChange={e => setEmail(e.target.value)} />
    {error && <p role="alert">{error}</p>}<button type="submit">Join</button>
  </form>;
}
