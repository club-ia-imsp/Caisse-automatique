import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { createProduct, updateProduct, getProduct, trainProduct } from '../services/api';
import toast from 'react-hot-toast';

const AddProduct = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const editId = searchParams.get('edit');
  const trainId = searchParams.get('train');
  const trainName = searchParams.get('name');

  const [mode, setMode] = useState(trainId ? 'train' : editId ? 'edit' : 'create');
  const [loading, setLoading] = useState(false);
  const [product, setProduct] = useState({
    name: '',
    price: '',
    category: '',
    stock_quantity: '',
  });

  // Training images
  const [images, setImages] = useState([]);
  const [previews, setPreviews] = useState([]);
  const [trainingProgress, setTrainingProgress] = useState(0);

  useEffect(() => {
    if (editId) {
      loadProduct(editId);
    }
  }, [editId]);

  const loadProduct = async (id) => {
    try {
      const res = await getProduct(id);
      const p = res.data;
      setProduct({
        name: p.name,
        price: String(p.price),
        category: p.category || '',
        stock_quantity: String(p.stock_quantity),
      });
    } catch {
      toast.error('Produit non trouvé');
      navigate('/admin/products');
    }
  };

  const handleProductSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    const data = {
      name: product.name,
      price: parseFloat(product.price),
      category: product.category || null,
      stock_quantity: parseInt(product.stock_quantity) || 0,
    };

    try {
      if (editId) {
        await updateProduct(editId, data);
        toast.success('Produit mis à jour!');
      } else {
        const res = await createProduct(data);
        toast.success('Produit créé! Ajoutez des images pour l\'entraînement.');
        navigate(`/admin/add-product?train=${res.data.id}&name=${encodeURIComponent(res.data.name)}`);
        return;
      }
      navigate('/admin/products');
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Erreur');
    } finally {
      setLoading(false);
    }
  };

  const handleImageChange = (e, slotIdx) => {
    const file = e.target.files[0];
    if (!file) return;

    const currentCount = images.filter(Boolean).length;
    if (currentCount >= 5 && !images[slotIdx]) {
      toast.error('Maximum 5 images');
      return;
    }

    setImages((prev) => {
      const next = [...prev];
      while (next.length <= slotIdx) next.push(null);
      next[slotIdx] = file;
      return next;
    });

    const reader = new FileReader();
    reader.onloadend = () => {
      setPreviews((prev) => {
        const next = [...prev];
        while (next.length <= slotIdx) next.push(null);
        next[slotIdx] = reader.result;
        return next;
      });
    };
    reader.readAsDataURL(file);
  };

  const removeImage = (idx) => {
    setImages((prev) => {
      const next = [...prev];
      next[idx] = null;
      return next;
    });
    setPreviews((prev) => {
      const next = [...prev];
      next[idx] = null;
      return next;
    });
  };

  const handleTrain = async () => {
    const validImages = images.filter(Boolean);
    if (validImages.length === 0) {
      toast.error('Ajoutez au moins une image');
      return;
    }

    setLoading(true);
    setTrainingProgress(10);

    const formData = new FormData();
    validImages.forEach((img) => {
      formData.append('images', img);
    });

    try {
      setTrainingProgress(30);
      const res = await trainProduct(trainId, formData);
      setTrainingProgress(100);
      toast.success(res.data.message);
      setTimeout(() => navigate('/admin/products'), 1500);
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Erreur d\'entraînement');
      setTrainingProgress(0);
    } finally {
      setLoading(false);
    }
  };

  const viewAngles = ['Face', 'Dessus', 'Gauche', 'Droite', 'Arrière'];

  // Training Mode
  if (mode === 'train' && trainId) {
    return (
      <div className="min-h-screen bg-surface-light p-3 sm:p-4 lg:p-6">
        <div className="max-w-3xl mx-auto">
          <button onClick={() => navigate('/admin/products')} className="text-sm text-gray-500 hover:text-gray-700 mb-4 flex items-center gap-1">
            <i className="fa-solid fa-arrow-left mr-1"></i> Retour aux produits
          </button>

          <div className="card">
            <div className="text-center mb-8">
              <div className="w-16 h-16 bg-primary/10 rounded-2xl flex items-center justify-center mx-auto mb-3">
                <i className="fa-solid fa-brain text-2xl text-primary"></i>
              </div>
              <h1 className="text-2xl font-bold text-gray-800">Entraînement IA</h1>
              <p className="text-gray-500 mt-1">
                Uploadez 5 images de <span className="font-bold text-primary">{trainName || 'ce produit'}</span> pour l'apprentissage Few-Shot
              </p>
            </div>

            {/* Image Upload Area */}
            <div className="grid grid-cols-3 sm:grid-cols-5 gap-2 sm:gap-3 mb-6">
              {[0, 1, 2, 3, 4].map((idx) => (
                <div key={idx} className="relative">
                  <div
                    className={`aspect-square rounded-xl border-2 border-dashed flex flex-col items-center justify-center cursor-pointer transition-all overflow-hidden ${
                      previews[idx]
                        ? 'border-primary bg-primary/5'
                        : 'border-surface-border hover:border-primary/50 bg-surface-light'
                    }`}
                    onClick={() => !previews[idx] && document.getElementById(`img-input-${idx}`).click()}
                  >
                    {previews[idx] ? (
                      <>
                        <img src={previews[idx]} alt={`Vue ${idx + 1}`} className="w-full h-full object-cover" />
                        <button
                          onClick={(e) => { e.stopPropagation(); removeImage(idx); }}
                          className="absolute top-1 right-1 w-6 h-6 bg-red-500 text-white rounded-full text-xs flex items-center justify-center hover:bg-red-600"
                        >
                          ✕
                        </button>
                      </>
                    ) : (
                      <>
                        <i className="fa-solid fa-camera text-xl mb-1 text-gray-400"></i>
                        <span className="text-[10px] text-gray-400">{viewAngles[idx]}</span>
                      </>
                    )}
                  </div>
                  <input
                    id={`img-input-${idx}`}
                    type="file"
                    accept="image/*"
                    className="hidden"
                    onChange={(e) => handleImageChange(e, idx)}
                  />
                </div>
              ))}
            </div>

            {/* Or drag-and-drop */}
            {images.filter(Boolean).length < 5 && (
              <label className="block mb-6">
                <div className="border-2 border-dashed border-surface-border rounded-xl py-8 text-center cursor-pointer hover:border-primary/50 transition-all">
                  <i className="fa-solid fa-folder-open text-2xl mb-2 block text-gray-400"></i>
                  <p className="text-sm text-gray-500">
                    Cliquez ou glissez-déposez vos images ici
                  </p>
                  <p className="text-xs text-gray-400 mt-1">
                    {images.filter(Boolean).length}/5 images • JPG, PNG, WEBP
                  </p>
                </div>
                <input
                  type="file"
                  accept="image/*"
                  multiple
                  className="hidden"
                  onChange={(e) => {
                    const files = Array.from(e.target.files);
                    files.forEach((file) => {
                      const nextSlot = [0,1,2,3,4].find(i => !images[i] && !previews[i]);
                      if (nextSlot !== undefined) {
                        handleImageChange({ target: { files: [file] } }, nextSlot);
                      }
                    });
                  }}
                />
              </label>
            )}

            {/* Progress bar */}
            {trainingProgress > 0 && (
              <div className="mb-6">
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-gray-500">Progression</span>
                  <span className="font-medium">{trainingProgress}%</span>
                </div>
                <div className="w-full bg-surface rounded-full h-3">
                  <div
                    className="h-3 rounded-full bg-primary transition-all duration-500"
                    style={{ width: `${trainingProgress}%` }}
                  ></div>
                </div>
              </div>
            )}

            {/* Train button */}
            <button
              onClick={handleTrain}
              disabled={images.length === 0 || loading}
              className="w-full btn-primary text-lg !py-4 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <span className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
                  Entraînement en cours...
                </span>
              ) : (
                `<i className="fa-solid fa-rocket mr-2"></i>Lancer l'entraînement (${images.length} image${images.length > 1 ? 's' : ''})`
              )}
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Create/Edit Mode
  return (
    <div className="min-h-screen bg-surface-light p-3 sm:p-4 lg:p-6">
      <div className="max-w-2xl mx-auto">
        <button onClick={() => navigate('/admin/products')} className="text-sm text-gray-500 hover:text-gray-700 mb-4 flex items-center gap-1">
          <i className="fa-solid fa-arrow-left mr-1"></i> Retour aux produits
        </button>

        <div className="card">
          <div className="text-center mb-8">
            <div className="w-16 h-16 bg-primary/10 rounded-2xl flex items-center justify-center mx-auto mb-3">
              <span className="text-3xl">{editId ? <i className="fa-solid fa-pen-to-square text-2xl text-primary"></i> : <i className="fa-solid fa-plus-circle text-2xl text-primary"></i>}</span>
            </div>
            <h1 className="text-2xl font-bold text-gray-800">
              {editId ? 'Modifier le Produit' : 'Nouveau Produit'}
            </h1>
            <p className="text-gray-500 mt-1">
              {editId ? 'Modifiez les informations du produit' : 'Ajoutez un nouveau produit au catalogue'}
            </p>
          </div>

          <form onSubmit={handleProductSubmit} className="space-y-5">
            <div>
              <label className="block text-sm font-medium text-gray-600 mb-1.5">Nom du produit *</label>
              <input
                type="text"
                className="input-field"
                placeholder="ex: Jus d'orange 1L"
                value={product.name}
                onChange={(e) => setProduct({ ...product, name: e.target.value })}
                required
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-600 mb-1.5">Prix (FCFA) *</label>
                <input
                  type="number"
                  step="0.01"
                  min="0"
                  className="input-field"
                  placeholder="0.00"
                  value={product.price}
                  onChange={(e) => setProduct({ ...product, price: e.target.value })}
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-600 mb-1.5">Stock</label>
                <input
                  type="number"
                  min="0"
                  className="input-field"
                  placeholder="0"
                  value={product.stock_quantity}
                  onChange={(e) => setProduct({ ...product, stock_quantity: e.target.value })}
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-600 mb-1.5">Catégorie</label>
              <input
                type="text"
                className="input-field"
                placeholder="ex: Boissons, Fruits, Fournitures..."
                value={product.category}
                onChange={(e) => setProduct({ ...product, category: e.target.value })}
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full btn-primary text-lg !py-3.5 disabled:opacity-50"
            >
              {loading ? 'Enregistrement...' : editId ? 'Mettre à jour' : 'Créer le produit'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default AddProduct;
