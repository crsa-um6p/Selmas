import React, { useEffect, useRef } from "react";
import { 
  Chart,
  CategoryScale,
  LinearScale,
  BarElement,
  BarController,
  Tooltip,
  Legend,
  Title
} from 'chart.js';

// Register the required Chart.js components
Chart.register(
  CategoryScale,
  LinearScale,
  BarElement,
  BarController,
  Tooltip,
  Legend,
  Title
);

const QualityChart = (props) => {
  const chartRefs = useRef([]);
  const chartInstances = useRef([]);
  
  const elements = ["Ph_level", "Organic_matter", "Cu", "Zn"];
  
  // Handle both single sample and multiple samples
  const samples = Array.isArray(props.selectedSample) ? props.selectedSample : [props.selectedSample];
  

  useEffect(() => {
    // Function to create a chart
    const createChart = (canvas, index) => {
      if (!canvas) return null;

      const ctx = canvas.getContext('2d');
      
      // Extract quality values and handle NaN/null values
      const quality = elements.map(element => {
        const value = samples[index]?.quality?.[element];
        // Convert NaN, null, or undefined to 0
        return (!value || isNaN(value)) ? 0 : parseFloat(value);
      });
            
      return new Chart(ctx, {
        type: 'bar',
        data: {
          labels: elements,
          datasets: [
            {
              label: "Quality Measurements",
              data: quality,
              backgroundColor: [
                "#FF6384",
                "#36A2EB", 
                "#FFCE56",
                "#4BC0C0",
                "#9966FF",
                "#FF9F40"
              ],
              borderColor: [
                "#FF6384",
                "#36A2EB",
                "#FFCE56",
                "#4BC0C0",
                "#9966FF",
                "#FF9F40"
              ],
              borderWidth: 2,
              hoverBackgroundColor: [
                "#FF6384",
                "#36A2EB",
                "#FFCE56",
                "#4BC0C0",
                "#9966FF",
                "#FF9F40"
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
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                callback: function(value) {
                  return value;
                }
              }
            }
          },
          plugins: {
            legend: {
              display: false,
              position: 'top',
              onClick: null,
              labels: {
                padding: 20,
                usePointStyle: true,
                font: {
                  size: 12
                }
              }
            },
            title: {
              display: samples.length > 1,
            },
            tooltip: {
              callbacks: {
                label: function(context) {
                  const label = context.label || '';
                  const value = context.parsed.y;
                  return `${label}: ${value}`;
                }
              }
            }
          }
        }
      });
    };

    // Cleanup function to destroy all chart instances
    const cleanup = () => {
      chartInstances.current.forEach((instance, index) => {
        if (instance) {
          instance.destroy();
          chartInstances.current[index] = null;
        }
      });
    };

    // Clean up existing charts
    cleanup();

    // Create new charts
    chartInstances.current = chartRefs.current.map((ref, index) => {
      return createChart(ref, index);
    });

    // Cleanup on component unmount or when samples change
    return cleanup;
  }, [samples, elements]); // Only re-run if samples or elements change

  // Calculate grid layout
  const gridCols = samples.length === 1 ? 1 : samples.length === 2 ? 2 : 3;
  const gridRows = Math.ceil(samples.length / gridCols);

  return (
    <div className="w-full">
      <div className="p-4 bg-white border border-gray-200 rounded-lg shadow-sm">
          <h2 className="text-lg font-bold mb-4 text-center">Soil Analysis</h2>
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

export default QualityChart;
