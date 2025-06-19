import React from "react";
import { Line } from "react-chartjs-2";



const SurfaceChart = (props) => {
  const months = props.metadata.month_names;
  const dam = props.surface.find((sb) => sb[0] === props.damName);
  let surface = dam[1].surface;


  return (
    <div className="">
      <div className="h-[33vh] p-3 bg-white border border-gray-200 rounded-lg shadow ">
        <Line
          data={{
            labels: months,
            datasets: [
              {
                label: "surface (km²)",
                data: surface,
                backgroundColor: surface.map((elem) =>
                  elem < 0 ? "#FF0000" : "#61c9fc"
                ),
                borderColor: "#61c9fc",
                borderWidth: 2,
                pointBackgroundColor: surface.map((elem) =>
                  elem < 0 ? "#FF0000" : "#61c9fc"
                ),
                pointBorderColor: "#fff",
                pointRadius: 4,
                pointHoverRadius: 6,
                tension: 0.4,
                fill: false,
              },
            ],
          }}
          options={{
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
            tooltips: {
              enabled: true,
            },

            plugins: {
              legend: {
                display: false,
              },

              title: {
                display: true,
                text: `surface ${props.damName}`,
                font: {
                  size: 10,
                },
                color: "#333",
                padding: {
                  top: 5,
                  bottom: 5,
                },
              },
            },
            scales: {
              x: {
                display: true,
                grid: {
                  display: false,
                  drawBorder: true,
                  zeroLineColor: "rgba(255, 0, 0, 1)",
                  color: "rgba(142, 156, 173,0.1)",
                },
                scaleLabel: {
                  display: true,
                },
                ticks: {
                  beginAtZero: true,
                  stepSize: 10,
                  suggestedMin: -20,
                  suggestedMax: 30,
                  fontColor: "#8492a6",
                  // userCallback: function(tick) {
                  //     return tick.toString() + '%';
                  // }
                },
              },
              y: {
                title: {
                  display: true,
                  text: `surface (km²)`,
                },
                display: true,
                barPercentage: 0.5,
                barValueSpacing: 0,
                barDatasetSpacing: 0,
                // barRadius: 50,
                stacked: false,
                ticks: {
                  beginAtZero: true,
                  fontColor: "#8492a6",
                },
                grid: {
                  display: true,
                  // color: "rgba(255, 0, 0, 1)",
                },
              },
            },
            legend: {
              display: false,
            },
            elements: {
              point: {
                radius: 0,
              },
            },
          }}
        />
      </div>
    </div>
  );
};

export default SurfaceChart;
