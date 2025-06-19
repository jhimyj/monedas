import React, { useState, useEffect } from 'react';
import { getUserTransactions, createTransaction, getUserCurrencies, getExchangeRate, getCurrencyById } from '../api';
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
  const [userCurrencies, setUserCurrencies] = useState([]);
  const [rate, setRate] = useState(null);
  const [exchanger, setExchanger] = useState('currency_api');

  const navigate = useNavigate();

  useEffect(() => {
    const storedUser = getUserFromStorage();
    setUser(storedUser);
    if (storedUser && storedUser.id) {
      fetchTransactions(storedUser.id);
    }
  }, []);

  useEffect(() => {
    if (user && user.id) {
      getUserCurrencies(user.id).then(setUserCurrencies);
    }
  }, [user]);

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

  // Cuando cambian los IDs, busca los tipos de moneda usando getCurrencyById y consulta el rate
  useEffect(() => {
    const fetchRate = async () => {
      if (form.currency_id_from && form.currency_id_to && form.currency_id_from !== form.currency_id_to) {
        try {
          const fromCurrency = await getCurrencyById(form.currency_id_from);
          const toCurrency = await getCurrencyById(form.currency_id_to);
          if (fromCurrency && toCurrency && fromCurrency.type !== toCurrency.type) {
            const res = await getExchangeRate(exchanger, fromCurrency.type, toCurrency.type);
            setRate(res.rate);
          } else if (fromCurrency && toCurrency && fromCurrency.type === toCurrency.type) {
            setRate(1);
          } else {
            setRate(null);
          }
        } catch {
          setRate(null);
        }
      } else {
        setRate(null);
      }
    };
    fetchRate();
  }, [form.currency_id_from, form.currency_id_to, exchanger]);

  // Calcula el monto destino automáticamente
  useEffect(() => {
    if (rate && form.amount_from) {
      const rounded = Math.round(Math.abs(Number(form.amount_from)) * rate * 100) / 100;
      setForm(f => ({ ...f, amount_to: rounded }));
    } else {
      setForm(f => ({ ...f, amount_to: '' }));
    }
  }, [rate, form.amount_from]);

  const handleCreate = async e => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setLoading(true);
    try {
      const amountFrom = Math.round(Number(form.amount_from) * 100) / 100;
      const amountTo = Math.round(Math.abs(Number(form.amount_from)) * rate * 100) / 100;
      const payload = {
        currency_id_from: Number(form.currency_id_from),
        currency_id_to: Number(form.currency_id_to),
        amount_from: amountFrom,
        amount_to: amountTo
      };
      console.log('[DEBUG] Payload enviado a createTransaction:', payload);
      await createTransaction(payload);
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
            placeholder="Monto origen (positivo)"
            value={form.amount_from}
            onChange={handleChange}
            required
          />
          {/* El input de monto destino se elimina, solo se muestra el valor calculado */}
          <div style={{ margin: '8px 0', color: '#1976d2' }}>
            {rate && form.amount_from && form.currency_id_from && form.currency_id_to && (
              <>
                Monto destino: {Math.abs(Number(form.amount_from)) * rate}
              </>
            )}
            {rate && ` Rate: ${rate}`}
          </div>
          <div style={{ marginBottom: 8 }}>
            <label>Proveedor de tipo de cambio: </label>
            <select value={exchanger} onChange={e => setExchanger(e.target.value)}>
              <option value="currency_api">CurrencyAPI</option>
              <option value="frankfurter">Frankfurter</option>
            </select>
          </div>
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