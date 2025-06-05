import axios from 'axios';

const API_URL = 'http://localhost:8000'; // Cambia si tu backend corre en otro puerto

export const loginUser = async ({ email, password }) => {
  try {
    const response = await axios.post(`${API_URL}/user/login/`, {
      email,
      password,
    });
    return response.data;
  } catch (error) {
    if (error.response) {
      throw new Error(error.response.data.detail || 'Error al iniciar sesión');
    } else {
      throw new Error('Error de red');
    }
  }
}

export const registerUser = async ({ name, email, password }) => {
  try {
    const response = await axios.post(`${API_URL}/user/`, {
      name,
      email,
      password,
    });
    return response.data;
  } catch (error) {
    if (error.response) {
      throw new Error(error.response.data.detail || 'Error al registrar usuario');
    } else {
      throw new Error('Error de red');
    }
  }
}

export const getUserTransactions = async (userId) => {
  try {
    const response = await axios.get(`${API_URL}/transaction/user/${userId}`);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Error al obtener transacciones');
  }
};

export const createTransaction = async (transaction) => {
  try {
    const response = await axios.post(`${API_URL}/transaction/`, transaction);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Error al crear transacción');
  }
};

export const getUserCurrencies = async (userId) => {
  const response = await axios.get(`${API_URL}/currency/user/${userId}`);
  return response.data;
};

export const getTransactionsByCurrency = async (currencyId) => {
  const response = await axios.get(`${API_URL}/transaction/currency/${currencyId}`);
  return response.data;
};

export const createCurrency = async (currency) => {
  const response = await axios.post(`${API_URL}/currency/`, currency);
  return response.data;
};

export const updateCurrency = async (currencyId, currency) => {
  const response = await axios.put(`${API_URL}/currency/${currencyId}`, currency);
  return response.data;
};

export const getExchangeRate = async (exchangerName, fromCurrency, toCurrency) => {
  try {
    const response = await axios.get(`${API_URL}/exchange/${exchangerName}/${fromCurrency}/${toCurrency}`);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Error al obtener tipo de cambio');
  }
};

