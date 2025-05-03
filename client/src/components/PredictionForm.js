// client/src/components/PredictionForm.js
import React, { useState } from 'react';
import axios from 'axios';

const PredictionForm = ({ onPrediction }) => {
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

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // Post data to the Flask API
    axios.post('http://127.0.0.1:5000/predict', formData)
      .then(response => {
        onPrediction(response.data.predicted_price);
      })
      .catch(error => {
        console.error("Error fetching data: ", error);
      });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        name="Marque"
        value={formData.Marque}
        onChange={handleChange}
        placeholder="Marque"
        required
      />
      <input
        type="text"
        name="Modèle"
        value={formData.Modèle}
        onChange={handleChange}
        placeholder="Modèle"
        required
      />
      <input
        type="number"
        name="Année"
        value={formData.Année}
        onChange={handleChange}
        placeholder="Année"
        required
      />
      <input
        type="text"
        name="Type de carburant"
        value={formData['Type de carburant']}
        onChange={handleChange}
        placeholder="Type de carburant"
        required
      />
      <input
        type="number"
        name="Puissance fiscale"
        value={formData['Puissance fiscale']}
        onChange={handleChange}
        placeholder="Puissance fiscale"
        required
      />
      <input
        type="number"
        name="Kilométrage"
        value={formData.Kilométrage}
        onChange={handleChange}
        placeholder="Kilométrage"
        required
      />
      <input
        type="number"
        name="Nombre de portes"
        value={formData['Nombre de portes']}
        onChange={handleChange}
        placeholder="Nombre de portes"
        required
      />
      <input
        type="text"
        name="Première main"
        value={formData['Première main']}
        onChange={handleChange}
        placeholder="Première main"
        required
      />
      <input
        type="text"
        name="État"
        value={formData['État']}
        onChange={handleChange}
        placeholder="État"
        required
      />
      <input
        type="text"
        name="Boîte à vitesses"
        value={formData['Boîte à vitesses']}
        onChange={handleChange}
        placeholder="Boîte à vitesses"
        required
      />
      <input
        type="text"
        name="Origine"
        value={formData['Origine']}
        onChange={handleChange}
        placeholder="Origine"
        required
      />
      <button type="submit">Predict Price</button>
    </form>
  );
};

export default PredictionForm;
