import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { healthCheck, getProducts, getInvoices } from '../services/api';

const Dashboard = () => {
  const [stats, setStats] = useState({ products: 0, invoices: 0, status: 'loading' });

  useEffect(() => {
    const loadStats = async () => {
      try {
        const [healthRes, productsRes, invoicesRes] = await Promise.all([
          healthCheck().catch(() => ({ data: { status: 'offline' } })),
          getProducts(0, 1).catch(() => ({ data: { total: 0 } })),
          getInvoices(0, 1).catch(() => ({ data: { total: 0 } })),
        ]);
        setStats({
          status: healthRes.data.status === 'healthy' ? 'online' : 'offline',
          products: productsRes.data.total || 0,
          invoices: invoicesRes.data.total || 0,
        });
      } catch {
        setStats({ products: 0, invoices: 0, status: 'offline' });
      }
    };
    loadStats();
  }, []);

  return (
    <div className="min-h-screen bg-surface-light">
      {/* Hero */}
      <div className="bg-gradient-to-br from-primary via-primary-dark to-secondary-dark text-white">
        <div className="max-w-7xl mx-auto px-4 py-12 sm:py-24">
          <div className="text-center">
            <h1 className="text-3xl sm:text-6xl font-extrabold mb-4 tracking-tight">
              automatic<span className="text-secondary-light">CHECK</span>
            </h1>
            <p className="text-lg sm:text-2xl text-white/80 mb-2">
              Caisse Automatique Intelligente
            </p>
            <p className="text-xs sm:text-sm text-white/60 mb-8 max-w-2xl mx-auto">
              Détection de produits par IA en temps réel, facturation automatique
              et gestion intelligente de votre inventaire.
            </p>
            <div className="flex flex-col sm:flex-row gap-3 sm:gap-4 justify-center">
              <Link to="/checkout" className="bg-white text-primary font-bold py-3 px-8 rounded-xl hover:bg-gray-100 transition-all shadow-lg text-base sm:text-lg">
                <i className="fa-solid fa-cash-register mr-2"></i>Ouvrir la Caisse
              </Link>
              <Link to="/login" className="bg-white/10 backdrop-blur text-white font-bold py-3 px-8 rounded-xl hover:bg-white/20 transition-all border border-white/20 text-base sm:text-lg">
                <i className="fa-solid fa-lock mr-2"></i>Espace Admin
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Stats */}
      <div className="max-w-7xl mx-auto px-4 -mt-8">
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 sm:gap-6">
          <div className="card flex items-center gap-4">
            <div className={`w-12 h-12 sm:w-14 sm:h-14 rounded-2xl flex items-center justify-center ${
              stats.status === 'online' ? 'bg-primary/10' : 'bg-red-100'
            }`}>
              <i className={`fa-solid fa-circle text-lg ${stats.status === 'online' ? 'text-primary' : 'text-red-500'}`}></i>
            </div>
            <div>
              <p className="text-sm text-gray-500">Statut Système</p>
              <p className={`text-base sm:text-lg font-bold ${stats.status === 'online' ? 'text-primary' : 'text-red-500'}`}>
                {stats.status === 'loading' ? 'Vérification...' : stats.status === 'online' ? 'En ligne' : 'Hors ligne'}
              </p>
            </div>
          </div>

          <div className="card flex items-center gap-4">
            <div className="w-12 h-12 sm:w-14 sm:h-14 rounded-2xl bg-blue-50 flex items-center justify-center">
              <i className="fa-solid fa-box text-xl text-blue-500"></i>
            </div>
            <div>
              <p className="text-sm text-gray-500">Produits Enregistrés</p>
              <p className="text-base sm:text-lg font-bold text-gray-800">{stats.products}</p>
            </div>
          </div>

          <div className="card flex items-center gap-4">
            <div className="w-12 h-12 sm:w-14 sm:h-14 rounded-2xl bg-amber-50 flex items-center justify-center">
              <i className="fa-solid fa-file-invoice text-xl text-amber-500"></i>
            </div>
            <div>
              <p className="text-sm text-gray-500">Factures Générées</p>
              <p className="text-base sm:text-lg font-bold text-gray-800">{stats.invoices}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Features */}
      <div className="max-w-7xl mx-auto px-4 py-12 sm:py-16">
        <h2 className="text-xl sm:text-2xl font-bold text-center text-gray-800 mb-8 sm:mb-12">Comment ça marche ?</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 sm:gap-8">
          <div className="text-center">
            <div className="w-16 h-16 sm:w-20 sm:h-20 bg-primary/10 rounded-3xl flex items-center justify-center mx-auto mb-4">
              <i className="fa-solid fa-camera text-2xl sm:text-3xl text-primary"></i>
            </div>
            <h3 className="font-bold text-base sm:text-lg mb-2 text-gray-800">1. Détection IA</h3>
            <p className="text-gray-500 text-xs sm:text-sm">
              La caméra détecte automatiquement les produits et les identifie
              par comparaison d'embeddings (Few-Shot Learning).
            </p>
          </div>
          <div className="text-center">
            <div className="w-16 h-16 sm:w-20 sm:h-20 bg-secondary/10 rounded-3xl flex items-center justify-center mx-auto mb-4">
              <i className="fa-solid fa-cart-shopping text-2xl sm:text-3xl text-secondary-dark"></i>
            </div>
            <h3 className="font-bold text-base sm:text-lg mb-2 text-gray-800">2. Panier Automatique</h3>
            <p className="text-gray-500 text-xs sm:text-sm">
              Les articles détectés sont ajoutés automatiquement au panier avec leurs prix,
              quantités et calcul de la TVA en temps réel.
            </p>
          </div>
          <div className="text-center">
            <div className="w-16 h-16 sm:w-20 sm:h-20 bg-blue-100 rounded-3xl flex items-center justify-center mx-auto mb-4">
              <i className="fa-solid fa-file-invoice-dollar text-2xl sm:text-3xl text-blue-600"></i>
            </div>
            <h3 className="font-bold text-base sm:text-lg mb-2 text-gray-800">3. Facture Instantanée</h3>
            <p className="text-gray-500 text-xs sm:text-sm">
              Générez un ticket de caisse PDF en un clic, avec tous les détails
              de la transaction et le récapitulatif des articles.
            </p>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-white border-t border-surface-border py-6 text-center text-sm text-gray-400">
        <p>automaticCHECK v1.0 — Caisse Automatique Intelligente</p>
      </footer>
    </div>
  );
};

export default Dashboard;
