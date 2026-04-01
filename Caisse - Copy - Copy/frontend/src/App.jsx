import React from 'react';
import { BrowserRouter, Routes, Route, useLocation } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { AuthProvider } from './context/AuthContext';
import Navbar from './components/Navbar';
import ProtectedRoute from './components/ProtectedRoute';
import Dashboard from './pages/Dashboard';
import Checkout from './pages/Checkout';
import Login from './pages/Login';
import AdminProducts from './pages/AdminProducts';
import AddProduct from './pages/AddProduct';
import InvoiceHistory from './pages/InvoiceHistory';

function AppLayout() {
  const location = useLocation();
  const hideNavbar = location.pathname === '/login';

  return (
    <div className="min-h-screen bg-surface-light">
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 3000,
          style: {
            borderRadius: '12px',
            background: '#333',
            color: '#fff',
            fontSize: '14px',
          },
          success: { iconTheme: { primary: '#16881c', secondary: '#fff' } },
        }}
      />
      
      {!hideNavbar && <Navbar />}
      
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/login" element={<Login />} />
        <Route path="/checkout" element={<Checkout />} />
        <Route path="/invoices" element={<InvoiceHistory />} />
        <Route path="/admin/products" element={
          <ProtectedRoute><AdminProducts /></ProtectedRoute>
        } />
        <Route path="/admin/add-product" element={
          <ProtectedRoute><AddProduct /></ProtectedRoute>
        } />
      </Routes>
    </div>
  );
}

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <AppLayout />
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
