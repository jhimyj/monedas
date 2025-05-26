import React, { useState, useEffect } from 'react';
import { getUserFromStorage } from '../utils/StorageOps';
import { useNavigate } from 'react-router-dom';
import { FaPencilAlt } from 'react-icons/fa';
import {
  getUserCurrencies,
  getTransactionsByCurrency,
  createCurrency,
  updateCurrency
} from '../api';

function CurrencyScreen() {
  const [currencies, setCurrencies] = useState([]);
  const [transactionsByCurrency, setTransactionsByCurrency] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showTx, setShowTx] = useState({});
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [showEditForm, setShowEditForm] = useState({});
  const [form, setForm] = useState({ type: '', amount: '' });
  const [editForm, setEditForm] = useState({});
  const user = getUserFromStorage();
  const navigate = useNavigate();

  useEffect(() => {
    if (user && user.id) {
      fetchCurrencies(user.id);
    }
    // eslint-disable-next-line
  }, []);

  const fetchCurrencies = async (userId) => {
    setLoading(true);
    setError('');
    try {
      const res = await getUserCurrencies(userId);
      setCurrencies(res);
      const txs = {};
      for (const currency of res) {
        const txRes = await getTransactionsByCurrency(currency.id);
        txs[currency.id] = txRes;
      }
      setTransactionsByCurrency(txs);
    } catch (err) {
      setError('Error al cargar divisas o transacciones', err);
    } finally {
      setLoading(false);
    }
  };

  const toggleTx = (currencyId) => {
    setShowTx((prev) => ({ ...prev, [currencyId]: !prev[currencyId] }));
  };

  const handleCreateCurrency = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await createCurrency({
        user_id: user.id,
        type: form.type,
        amount: Number(form.amount)
      });
      setForm({ type: '', amount: '' });
      setShowCreateForm(false);
      fetchCurrencies(user.id);
    } catch (err) {
      setError('Error al crear divisa', err);
    } finally {
      setLoading(false);
    }
  };

  const handleEditCurrency = async (currencyId) => {
    setError('');
    setLoading(true);
    try {
      await updateCurrency(currencyId, {
        user_id: user.id,
        type: editForm.type,
        amount: Number(editForm.amount)
      });
      setShowEditForm((prev) => ({ ...prev, [currencyId]: false }));
      fetchCurrencies(user.id);
    } catch (err) {
      setError('Error al actualizar divisa', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <button onClick={() => navigate('/transaccion')} style={{ marginBottom: 16 }}>
        ← Atrás
      </button>
      <h2>Mis Divisas</h2>
      {!showCreateForm && (
        <button onClick={() => setShowCreateForm(true)} style={{ fontSize: 24, padding: '0.2em 0.7em', marginBottom: 12 }}>+</button>
      )}
      {showCreateForm && (
        <form onSubmit={handleCreateCurrency} style={{ marginBottom: 16 }}>
          <input
            type="text"
            name="type"
            placeholder="Tipo (ej: USD, PEN)"
            value={form.type}
            onChange={e => setForm({ ...form, type: e.target.value })}
            required
          />
          <input
            type="number"
            name="amount"
            placeholder="Monto inicial"
            value={form.amount}
            onChange={e => setForm({ ...form, amount: e.target.value })}
            required
          />
          <button type="submit" disabled={loading}>Crear</button>
          <button type="button" style={{ marginLeft: 8 }} onClick={() => setShowCreateForm(false)}>Cancelar</button>
        </form>
      )}
      {loading && <div>Cargando...</div>}
      {error && <div style={{ color: 'red' }}>{error}</div>}
      {currencies.length === 0 && !loading && <div>No tienes divisas registradas.</div>}
      {currencies.map(currency => (
        <div key={currency.id} style={{ border: '1px solid #ccc', borderRadius: 8, margin: '16px 0', padding: 12, position: 'relative' }}>
          <h3>{currency.type} (ID: {currency.id})
            <button
              style={{ background: 'none', border: 'none', cursor: 'pointer', marginLeft: 8 }}
              onClick={() => {
                setEditForm({ type: currency.type, amount: currency.amount });
                setShowEditForm((prev) => ({ ...prev, [currency.id]: !prev[currency.id] }));
              }}
              title="Editar divisa"
            >
              <FaPencilAlt />
            </button>
          </h3>
          {showEditForm[currency.id] && (
            <form
              onSubmit={e => {
                e.preventDefault();
                handleEditCurrency(currency.id);
              }}
              style={{ marginBottom: 12 }}
            >
              <input
                type="text"
                name="type"
                placeholder="Tipo (ej: USD, PEN)"
                value={editForm.type}
                onChange={e => setEditForm({ ...editForm, type: e.target.value })}
                required
              />
              <input
                type="number"
                name="amount"
                placeholder="Monto"
                value={editForm.amount}
                onChange={e => setEditForm({ ...editForm, amount: e.target.value })}
                required
              />
              <button type="submit" disabled={loading}>Actualizar</button>
              <button type="button" style={{ marginLeft: 8 }} onClick={() => setShowEditForm((prev) => ({ ...prev, [currency.id]: false }))}>Cancelar</button>
            </form>
          )}
          <div>Monto: {currency.amount}</div>
          <div style={{ marginTop: 8 }}>
            <button onClick={() => toggleTx(currency.id)} style={{ marginBottom: 8, display: 'block' }}>
              {showTx[currency.id] ? 'Ocultar transacciones' : 'Ver transacciones'}
            </button>
            {showTx[currency.id] && (
              <>
                <strong>Transacciones de esta divisa:</strong>
                {transactionsByCurrency[currency.id] && transactionsByCurrency[currency.id].length > 0 ? (
                  <ul>
                    {transactionsByCurrency[currency.id].map(tx => (
                      <li key={tx.id}>
                        #{tx.id} | De: {tx.currency_id_from} ({tx.amount_from}) → A: {tx.currency_id_to} ({tx.amount_to})
                      </li>
                    ))}
                  </ul>
                ) : (
                  <div style={{ color: '#888' }}>No hay transacciones para esta divisa.</div>
                )}
              </>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}

export default CurrencyScreen;
