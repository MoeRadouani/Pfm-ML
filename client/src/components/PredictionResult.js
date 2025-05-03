// client/src/components/PredictionResult.js
import React from 'react';

const PredictionResult = ({ price }) => {
  return (
    <div>
      <h3>Predicted Price: {price ? `${price} MAD` : 'N/A'}</h3>
    </div>
  );
};

export default PredictionResult;
