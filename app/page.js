'use client'
// pages/index.js

import { useState, useEffect } from 'react';
import axios from 'axios';

export default function Home() {

  const [message, setMessage] = useState('');

  useEffect(() => {
    async function fetchData() {
      const response = await axios.get('http://localhost:5328/api/hello');
      setMessage(response.data); 
    }
    fetchData();
  }, []);

  return <div>{message}</div>;

}