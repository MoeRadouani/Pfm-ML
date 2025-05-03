// client/src/App.js
import React, { useState } from 'react';
import PredictionForm from './components/PredictionForm';
import PredictionResult from './components/PredictionResult';

const App = () => {
  const [predictedPrice, setPredictedPrice] = useState(null);

  return (
    <div>
      <h1>Car Price Prediction</h1>
      <PredictionForm onPrediction={setPredictedPrice} />
      <PredictionResult price={predictedPrice} />
    </div>
  );
};

export default App;
