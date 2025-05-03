import React, { useState } from 'react';
import './App.css'; // optional if you add any custom styles

const App = () => {
  const [formData, setFormData] = useState({
    Marque: '',
    Modèle: '',
    Année: '',
    'Type de carburant': '',
    'Puissance fiscale': '',
    Kilométrage: '',
    'Nombre de portes': '',
    'Première main': '',
    État: '',
    'Boîte à vitesses': '',
    Origine: ''
  });

  const [price, setPrice] = useState(null);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    fetch('http://localhost:5000/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(formData)
    })
      .then(res => res.json())
      .then(data => setPrice(data.predicted_price))
      .catch(err => console.error('Prediction error:', err));
  };

  const scrollToForm = () => {
    document.getElementById('predict-form').scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <>
      {/* Header */}
      <header className="header_area">
        <div className="top_bar">
          <div className="container">
            <div className="d-flex justify-content-between">
              <div className="contact_info">
                <span>📞 (+71) 8522369417</span>
                <span>✉️ demo@gmail.com</span>
              </div>
              <div className="logo">
                <h2 style={{ color: 'white' }}>Trator</h2>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Hero section */}
      <section className="home_banner_area" style={{ backgroundColor: '#f97316', padding: '100px 0' }}>
        <div className="container">
          <div className="row align-items-center justify-content-between">
            <div className="col-lg-6">
              <h1 className="text-white">Predict Your Car Price</h1>
              <p className="text-white mt-4">
                Enter your vehicle information and get an estimated price instantly.
              </p>
              <button className="btn btn-dark mt-3" onClick={scrollToForm}>Predict</button>
            </div>
            <div className="col-lg-6">
              <img src="/trator_template/images/car.png" alt="car" style={{ maxWidth: '100%' }} />
            </div>
          </div>
        </div>
      </section>

      {/* Prediction Form */}
      <section id="predict-form" className="container py-5">
        <h2>Enter Car Details</h2>
        <form onSubmit={handleSubmit} className="row g-3">
          {Object.entries(formData).map(([key, value]) => (
            <div className="col-md-6" key={key}>
              <input
                type={key === 'Année' || key.includes('Kilométrage') || key.includes('Puissance') ? 'number' : 'text'}
                name={key}
                value={value}
                onChange={handleChange}
                placeholder={key}
                className="form-control"
                required
              />
            </div>
          ))}
          <div className="col-12">
            <button type="submit" className="btn btn-primary">Submit</button>
          </div>
        </form>
        {price && (
          <div className="mt-4">
            <h3>Estimated Price: {price} MAD</h3>
          </div>
        )}
      </section>
    </>
  );
};

export default App;
