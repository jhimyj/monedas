import React, { useState, useEffect } from 'react';
import { getUserTransactions, createTransaction } from '../api';
import { getUserFromStorage, removeUserFromStorage } from '../utils/StorageOps';
import { useNavigate } from 'react-router-dom';

function TransaccionScreen() {
  const [user, setUser] = useState('');
  const [transactions, setTransactions] = useState([]);
  const [form, setForm] = useState({
    currency_id_from: '',
    currency_id_to: '',
    amount_from: '',
    amount_to: ''
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);
  const [showTransactions, setShowTransactions] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const storedUser = getUserFromStorage();
    setUser(storedUser);
    if (storedUser && storedUser.id) {
      fetchTransactions(storedUser.id);
    }
  }, []);

  const fetchTransactions = async (userId) => {
    setError('');
    setSuccess('');
    setLoading(true);
    try {
      const data = await getUserTransactions(userId);
      setTransactions(data);
      setShowTransactions(true);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleFetch = async () => {
    if (showTransactions) {
      setShowTransactions(false);
      setTransactions([]);
      setSuccess('');
      setError('');
      return;
    }
    if (user && user.id) {
      fetchTransactions(user.id);
    }
  };

  const handleChange = e => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleCreate = async e => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setLoading(true);
    try {
      await createTransaction({
        currency_id_from: Number(form.currency_id_from),
        currency_id_to: Number(form.currency_id_to),
        amount_from: Number(form.amount_from),
        amount_to: Number(form.amount_to)
      });
      setSuccess('Transacción creada correctamente.');
      setForm({ currency_id_from: '', currency_id_to: '', amount_from: '', amount_to: '' });
      handleFetch();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h2>Transacciones de Usuario</h2>
      <div style={{ marginBottom: 16 }}>
        <button onClick={() => navigate('/currency')} style={{ marginRight: 8 }}>
          Mis Divisas
        </button>
        <button onClick={handleFetch} disabled={loading || !user.id}>
          {loading ? 'Cargando...' : showTransactions ? 'Ocultar transacciones' : 'Ver transacciones'}
        </button>
        <button onClick={() => { removeUserFromStorage(); navigate('/login'); }} style={{ marginLeft: 8 }}>
          Cerrar sesión
        </button>
      </div>
      {error && <div style={{ color: 'red', marginTop: 8 }}>{error}</div>}
      {success && <div style={{ color: 'green', marginTop: 8 }}>{success}</div>}
      {showTransactions && (
        <ul>
          {transactions.map(tx => (
            <li key={tx.id}>
              #{tx.id} | De: {tx.currency_id_from} ({tx.amount_from}) → A: {tx.currency_id_to} ({tx.amount_to})
            </li>
          ))}
        </ul>
      )}
      <h3>Crear nueva transacción</h3>
      {!showForm && (
        <button onClick={() => setShowForm(true)} style={{ fontSize: 24, padding: '0.2em 0.7em', marginBottom: 12 }}>+</button>
      )}
      {showForm && (
        <form onSubmit={handleCreate} style={{ marginTop: 12 }}>
          <input
            type="number"
            name="currency_id_from"
            placeholder="ID moneda origen"
            value={form.currency_id_from}
            onChange={handleChange}
            required
          />
          <input
            type="number"
            name="currency_id_to"
            placeholder="ID moneda destino"
            value={form.currency_id_to}
            onChange={handleChange}
            required
          />
          <input
            type="number"
            name="amount_from"
            placeholder="Monto origen (negativo)"
            value={form.amount_from}
            onChange={handleChange}
            required
          />
          <input
            type="number"
            name="amount_to"
            placeholder="Monto destino (positivo)"
            value={form.amount_to}
            onChange={handleChange}
            required
          />
          <div style={{ marginTop: 8 }}>
            <button type="submit" disabled={loading}>
              {loading ? 'Cargando...' : 'Crear transacción'}
            </button>
            <button type="button" style={{ marginLeft: 8 }} onClick={() => setShowForm(false)}>
              Cancelar
            </button>
          </div>
        </form>
      )}
    </div>
  );
}

export default TransaccionScreen;
