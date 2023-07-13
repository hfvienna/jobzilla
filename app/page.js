// pages/index.js
'use client'

import { useEffect } from 'react';

export default function Home() {

  useEffect(() => {
    if (typeof window !== 'undefined') {
      console.log(window.location); 
    }

    async function callPython() {
      const resp = await fetch('/api/python'); 
      const data = await resp.json();
      console.log(data);
    }

    callPython();  // This should be inside the useEffect hook.
  }, []); 

  return <div>Welcome!</div>
}