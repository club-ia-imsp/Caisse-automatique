import React, { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Navbar = () => {
  const { user, logout, isAuthenticated } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();
  const [mobileOpen, setMobileOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const navLinks = [
    { path: '/', label: 'Accueil', icon: 'fa-solid fa-house' },
    { path: '/checkout', label: 'Caisse', icon: 'fa-solid fa-cash-register' },
  ];

  const adminLinks = [
    { path: '/admin/products', label: 'Produits', icon: 'fa-solid fa-box' },
    { path: '/admin/add-product', label: 'Ajouter', icon: 'fa-solid fa-plus' },
    { path: '/invoices', label: 'Factures', icon: 'fa-solid fa-file-invoice' },
  ];

  const isActive = (path) => location.pathname === path;

  return (
    <nav className="bg-white shadow-sm border-b border-surface-border sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          {/* Logo */}
          <div className="flex items-center">
            <Link to="/" className="flex items-center gap-2">
              <div className="w-10 h-10 bg-primary rounded-xl flex items-center justify-center">
                <span className="text-white font-bold text-lg">F</span>
              </div>
              <span className="text-xl font-bold text-primary hidden sm:block">automaticCHECK</span>
            </Link>
          </div>

          {/* Desktop Nav */}
          <div className="hidden md:flex items-center gap-1">
            {navLinks.map((link) => (
              <Link
                key={link.path}
                to={link.path}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                  isActive(link.path)
                    ? 'bg-primary/10 text-primary'
                    : 'text-gray-600 hover:bg-surface hover:text-gray-900'
                }`}
              >
                <i className={`${link.icon} mr-1.5 text-xs`}></i>
                {link.label}
              </Link>
            ))}

            {isAuthenticated && (
              <>
                <div className="w-px h-6 bg-surface-border mx-2"></div>
                {adminLinks.map((link) => (
                  <Link
                    key={link.path}
                    to={link.path}
                    className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                      isActive(link.path)
                        ? 'bg-primary/10 text-primary'
                        : 'text-gray-600 hover:bg-surface hover:text-gray-900'
                    }`}
                  >
                    <i className={`${link.icon} mr-1.5 text-xs`}></i>
                    {link.label}
                  </Link>
                ))}
              </>
            )}
          </div>

          {/* Auth buttons */}
          <div className="flex items-center gap-3">
            {isAuthenticated ? (
              <div className="flex items-center gap-3">
                <span className="hidden sm:block text-sm text-gray-600">
                  <i className="fa-solid fa-user mr-1"></i> {user?.username}
                </span>
                <button onClick={handleLogout} className="btn-danger text-sm !py-2 !px-4">
                  Déconnexion
                </button>
              </div>
            ) : (
              <Link to="/login" className="btn-primary text-sm !py-2 !px-4">
                Admin
              </Link>
            )}

            {/* Mobile menu button */}
            <button
              onClick={() => setMobileOpen(!mobileOpen)}
              className="md:hidden p-2 rounded-lg hover:bg-surface"
            >
              <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                {mobileOpen ? (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                ) : (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                )}
              </svg>
            </button>
          </div>
        </div>
      </div>

      {/* Mobile menu */}
      {mobileOpen && (
        <div className="md:hidden border-t border-surface-border bg-white animate-fade-in">
          <div className="px-4 py-3 space-y-1">
            {navLinks.map((link) => (
              <Link
                key={link.path}
                to={link.path}
                onClick={() => setMobileOpen(false)}
                className={`block px-4 py-2.5 rounded-lg text-sm font-medium ${
                  isActive(link.path) ? 'bg-primary/10 text-primary' : 'text-gray-600'
                }`}
              >
                <i className={`${link.icon} mr-2 text-xs`}></i>{link.label}
              </Link>
            ))}
            {isAuthenticated && adminLinks.map((link) => (
              <Link
                key={link.path}
                to={link.path}
                onClick={() => setMobileOpen(false)}
                className={`block px-4 py-2.5 rounded-lg text-sm font-medium ${
                  isActive(link.path) ? 'bg-primary/10 text-primary' : 'text-gray-600'
                }`}
              >
                <i className={`${link.icon} mr-2 text-xs`}></i>{link.label}
              </Link>
            ))}
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
