import React, { useEffect, useRef } from "react";
import { Chart, ArcElement, Tooltip, Legend, Title, PieController } from 'chart.js';

// Register the required Chart.js components
Chart.register(ArcElement, Tooltip, Legend, Title, PieController);

const TextureChart = (props) => {
  const chartRefs = useRef([]);
  const chartInstances = useRef([]);
  
  const elements = ["Argile", "Lemon", "Sable"];
  console.log("props.selectedSample",props.selectedSample);
  
  // Handle both single sample and multiple samples
  const samples = Array.isArray(props.selectedSample) ? props.selectedSample : [props.selectedSample];
  
  console.log("samples", samples);

  useEffect(() => {
    // Destroy existing charts
    chartInstances.current.forEach(instance => {
      if (instance) {
        instance.destroy();
      }
    });
    chartInstances.current = [];

    // Create charts for each sample
    samples.forEach((sample, index) => {
      if (chartRefs.current[index]) {
        const texture = [
          sample?.texture?.Argile || 0,
          sample?.texture?.Lemon || 0,
          sample?.texture?.Sable || 0
        ];
        
        console.log(`texture for sample ${index}:`, texture);
        
        const ctx = chartRefs.current[index].getContext('2d');
        const chartInstance = new Chart(ctx, {
          type: 'pie',
          data: {
            labels: elements,
            datasets: [
              {
                label: "level (%)",
                data: texture,
                backgroundColor: [
                  "#FF6384",
                  "#36A2EB", 
                  "#FFCE56"
                ],
                borderColor: "#fff",
                borderWidth: 2,
                hoverBackgroundColor: [
                  "#FF6384",
                  "#36A2EB",
                  "#FFCE56"
                ],
                hoverBorderColor: "#fff",
                hoverBorderWidth: 3,
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            layout: {
              padding: {
                left: 0,
                right: 0,
                top: 0,
                bottom: 0,
              },
            },
            plugins: {
              legend: {
                display: true,
                onClick: null,
                position: 'bottom',
                labels: {
                  padding: 20,
                  usePointStyle: true,
                  font: {
                    size: 12
                  }
                }
              },
              title: {
                display: false,
              },
              tooltip: {
                callbacks: {
                  label: function(context) {
                    const label = context.label || '';
                    const value = context.parsed;
                    return `${label}: ${value} %`;
                  }
                }
              }
            },
            elements: {
              arc: {
                borderWidth: 2
              }
            }
          }
        });
        
        chartInstances.current[index] = chartInstance;
      }
    });

    // Cleanup function
    return () => {
      chartInstances.current.forEach(instance => {
        if (instance) {
          instance.destroy();
        }
      });
      chartInstances.current = [];
    };
  }, [samples, elements]);

  // Calculate grid layout
  const gridCols = samples.length === 1 ? 1 : samples.length === 2 ? 2 : 3;
  const gridRows = Math.ceil(samples.length / gridCols);

  return (
    <div className="w-full">
      <div className="p-4 bg-white border border-gray-200 rounded-lg shadow-sm">
        <h2 className="text-lg font-bold mb-4 text-center">Soil Composition</h2>
        <div className={`grid gap-6 ${
          samples.length === 1 
            ? 'grid-cols-1 max-w-md mx-auto' 
            : samples.length === 2 
              ? 'grid-cols-2 max-w-2xl mx-auto' 
              : 'grid-cols-3 max-w-4xl mx-auto'
        }`}>
          {samples.map((sample, index) => (
            <div key={index} className="relative bg-gray-50 rounded-lg p-3 border border-gray-100 h-64">
              <div className="text-center mb-2">
              {samples.length > 1 && (
                <h3 className="text-sm font-medium text-gray-700">
                  {sample?.Depth || `Sample ${index + 1}`}
                </h3>
              )}
              </div>
              <div className="relative h-48">
                <canvas 
                  ref={el => chartRefs.current[index] = el}
                  className="w-full h-full"
                ></canvas>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default TextureChart;
