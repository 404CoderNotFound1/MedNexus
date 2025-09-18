import { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [phone, setPhone] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [token, setToken] = useState<string | null>(() => localStorage.getItem('token'));
  const [error, setError] = useState<string | null>(null);
  const [mode, setMode] = useState<'normal' | 'dyslexia' | 'adhd'>('normal');

  useEffect(() => {
    // Keep token in localStorage for simple session persistence
    if (token) {
      localStorage.setItem('token', token);
    } else {
      localStorage.removeItem('token');
    }
  }, [token]);

  const validatePhone = (val: string) => /^\d{10}$/.test(val);

  const register = async () => {
    setError(null);
    if (!validatePhone(phone)) {
      setError('Phone must be a 10-digit number');
      return;
    }
    if (!password) {
      setError('Password is required');
      return;
    }
    try {
      const res = await axios.post('/api/auth/register', { phone, password });
      setToken(res.data.token);
    } catch (e: any) {
      const msg = e?.response?.data?.detail || 'Registration failed';
      setError(msg);
    }
  };

  const login = async () => {
    setError(null);
    if (!validatePhone(phone)) {
      setError('Phone must be a 10-digit number');
      return;
    }
    if (!password) {
      setError('Password is required');
      return;
    }
    try {
      const res = await axios.post('/api/auth/login', { phone, password });
      setToken(res.data.token);
    } catch (e: any) {
      const msg = e?.response?.data?.detail || 'Login failed';
      setError(msg);
    }
  };

  const logout = () => {
    setToken(null);
    setPhone('');
    setPassword('');
  };

  const story = `It was a cold, moonless night when the whisper first floated through the hallway.
The house, with its peeling wallpaper and crooked doorframes, breathed like a sleeping creature.
Somewhere between the ticking clock and the restless wind, a floorboard sighed—then another.
I told myself it was just the old wood settling.
But the whispers kept returning, closer each time, curling around my ears like frost.
When I finally turned the corner, the hallway stretched longer than it should have, the end swallowed by shadow.
And from that shadow, something began to hum my name.`;

  return (
    <div className={`app font-${mode}`}>
      <header className="header">
        <h1>Horror Tales</h1>
      </header>
      <main>
        {!token ? (
          <section className="auth">
            <h2>Sign In</h2>
            <div className="form">
              <label>
                <span>Phone (10 digits)</span>
                <input
                  type="tel"
                  inputMode="numeric"
                  pattern="\d{10}"
                  placeholder="1234567890"
                  value={phone}
                  onChange={(e) => setPhone(e.target.value)}
                />
              </label>
              <label>
                <span>Password</span>
                <input
                  type="password"
                  placeholder="••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </label>
              {error && <div className="error">{error}</div>}
              <div className="actions">
                <button onClick={login}>Login</button>
                <button className="secondary" onClick={register}>Register</button>
              </div>
            </div>
          </section>
        ) : (
          <>
            <section className="toolbar">
              <div className="font-toggle">
                <span>Font:</span>
                <button
                  className={mode === 'normal' ? 'active' : ''}
                  onClick={() => setMode('normal')}
                >
                  Normal
                </button>
                <button
                  className={mode === 'dyslexia' ? 'active' : ''}
                  onClick={() => setMode('dyslexia')}
                >
                  Dyslexia
                </button>
                <button
                  className={mode === 'adhd' ? 'active' : ''}
                  onClick={() => setMode('adhd')}
                >
                  ADHD
                </button>
              </div>
              <button onClick={logout}>Logout</button>
            </section>
            <section className="story">
              <h2>The Whisper in the Hall</h2>
              <p>{story}</p>
            </section>
          </>
        )}
      </main>
    </div>
  );
}

export default App;
