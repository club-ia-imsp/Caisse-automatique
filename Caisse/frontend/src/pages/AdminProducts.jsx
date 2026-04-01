import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getProducts, deleteProduct } from '../services/api';
import toast from 'react-hot-toast';

const AdminProducts = () => {
  const [products, setProducts] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);

  const loadProducts = async () => {
    try {
      const res = await getProducts();
      setProducts(res.data.products);
      setTotal(res.data.total);
    } catch {
      toast.error('Erreur de chargement des produits');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadProducts();
  }, []);

  const handleDelete = async (id, name) => {
    if (!window.confirm(`Supprimer "${name}" ? Cette action est irréversible.`)) return;
    
    try {
      await deleteProduct(id);
      toast.success(`"${name}" supprimé`);
      loadProducts();
    } catch {
      toast.error('Erreur de suppression');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-surface-light flex items-center justify-center">
        <div className="w-10 h-10 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-surface-light p-3 sm:p-4 lg:p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between mb-6 sm:mb-8 gap-3 sm:gap-4">
          <div>
            <h1 className="text-xl sm:text-2xl font-bold text-gray-800">
              <i className="fa-solid fa-boxes-stacked mr-2 text-primary"></i>Gestion des Produits
            </h1>
            <p className="text-xs sm:text-sm text-gray-500 mt-1">{total} produit(s) enregistré(s)</p>
          </div>
          <Link to="/admin/add-product" className="btn-primary text-sm sm:text-base">
            <i className="fa-solid fa-plus mr-2"></i>Ajouter un Produit
          </Link>
        </div>

        {/* Products Grid */}
        {products.length === 0 ? (
          <div className="card text-center py-12 sm:py-16">
            <i className="fa-solid fa-box-open text-5xl sm:text-6xl text-gray-300 mb-4 block"></i>
            <h3 className="text-lg sm:text-xl font-bold text-gray-700 mb-2">Aucun produit</h3>
            <p className="text-gray-500 mb-6 text-sm">Commencez par ajouter vos premiers produits au catalogue</p>
            <Link to="/admin/add-product" className="btn-primary inline-block">
              <i className="fa-solid fa-plus mr-2"></i>Ajouter un Produit
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
            {products.map((product) => (
              <div key={product.id} className="card group hover:border-primary/30">
                {/* Product Image */}
                <div className="h-32 sm:h-40 bg-surface rounded-xl mb-4 overflow-hidden flex items-center justify-center">
                  {product.image_url ? (
                    <img
                      src={product.image_url}
                      alt={product.name}
                      className="h-full w-full object-cover"
                    />
                  ) : (
                    <i className="fa-solid fa-box text-4xl sm:text-5xl text-gray-300"></i>
                  )}
                </div>

                {/* Product Info */}
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <h3 className="font-bold text-gray-800 text-base sm:text-lg">{product.name}</h3>
                    {product.category && (
                      <span className="badge-success text-xs mt-1">{product.category}</span>
                    )}
                  </div>
                  <span className="text-lg sm:text-xl font-bold text-primary">{product.price.toFixed(0)} <span className="text-xs">FCFA</span></span>
                </div>

                {/* Stats */}
                <div className="flex items-center gap-3 sm:gap-4 text-xs sm:text-sm text-gray-500 mb-4">
                  <span><i className="fa-solid fa-chart-bar mr-1"></i>Stock: {product.stock_quantity}</span>
                  <span className={product.embedding_count > 0 ? 'text-primary' : 'text-amber-500'}>
                    <i className="fa-solid fa-brain mr-1"></i>{product.embedding_count}/5 embeddings
                  </span>
                </div>

                {/* Training Status */}
                <div className="mb-4">
                  <div className="flex justify-between text-xs mb-1">
                    <span className="text-gray-500">Apprentissage</span>
                    <span className="font-medium">{Math.min(product.embedding_count, 5)}/5</span>
                  </div>
                  <div className="w-full bg-surface rounded-full h-2">
                    <div
                      className={`h-2 rounded-full transition-all ${
                        product.embedding_count >= 5 ? 'bg-primary' : product.embedding_count > 0 ? 'bg-amber-400' : 'bg-gray-300'
                      }`}
                      style={{ width: `${Math.min((product.embedding_count / 5) * 100, 100)}%` }}
                    ></div>
                  </div>
                </div>

                {/* Actions */}
                <div className="flex gap-2">
                  <Link
                    to={`/admin/add-product?edit=${product.id}`}
                    className="flex-1 text-center py-2 text-xs sm:text-sm font-medium text-primary bg-primary/10 rounded-lg hover:bg-primary/20 transition-all"
                  >
                    <i className="fa-solid fa-pen mr-1"></i>Modifier
                  </Link>
                  <Link
                    to={`/admin/add-product?train=${product.id}&name=${encodeURIComponent(product.name)}`}
                    className="flex-1 text-center py-2 text-xs sm:text-sm font-medium text-secondary-dark bg-secondary/10 rounded-lg hover:bg-secondary/20 transition-all"
                  >
                    <i className="fa-solid fa-brain mr-1"></i>Entraîner
                  </Link>
                  <button
                    onClick={() => handleDelete(product.id, product.name)}
                    className="px-3 py-2 text-xs sm:text-sm text-red-500 bg-red-50 rounded-lg hover:bg-red-100 transition-all"
                  >
                    <i className="fa-solid fa-trash"></i>
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default AdminProducts;
