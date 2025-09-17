import { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';

interface Item {
  id: number;
  name: string;
  description?: string;
}

function App() {
  const [items, setItems] = useState<Item[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchItems = async () => {
      try {
        const response = await axios.get('/api/items');
        setItems(response.data);
        setLoading(false);
      } catch (err) {
        setError('Failed to fetch items');
        setLoading(false);
        console.error('Error fetching data:', err);
      }
    };

    fetchItems();
  }, []);

  if (loading) return <div className="loading">Loading...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="app">
      <header className="header">
        <h1>Fullstack React + FastAPI App</h1>
      </header>
      <main>
        <section className="items">
          <h2>Items from Backend</h2>
          <div className="item-list">
            {items.map((item) => (
              <div key={item.id} className="item-card">
                <h3>{item.name}</h3>
                <p>{item.description || 'No description available'}</p>
              </div>
            ))}
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
