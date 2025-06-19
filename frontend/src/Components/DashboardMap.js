import React from 'react'
import { MapContainer, TileLayer, Marker, GeoJSON   } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import "leaflet-draw/dist/leaflet.draw.css";
import L, { latLng, icon } from "leaflet";
import MarkerClusterGroup from 'react-leaflet-markercluster';
import { Tooltip } from 'react-leaflet';


const maxBounds = [
    [28.76159, -10.020428],
    [35.952755, -1.790656],
  ];


  

  
const DashboardMap = (props) => {

  let activeLayer = null

  // Define a green marker icon
  const greenIcon = L.icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
  });

  // Group samples by coordinates
  const groupSamplesByLocation = (features) => {
    const groupedSamples = {};
    
    features.forEach(feature => {
      if (feature.geometry && feature.geometry.type === "Point" && Array.isArray(feature.geometry.coordinates)) {
        const [lon, lat] = feature.geometry.coordinates;
        const locationKey = `${lat},${lon}`;
        
        if (!groupedSamples[locationKey]) {
          groupedSamples[locationKey] = {
            coordinates: [lat, lon],
            samples: []
          };
        }
        
        groupedSamples[locationKey].samples.push(feature.properties);
      }
    });
    
    return groupedSamples;
  };

  const groupedSamples = props.GeoData ? groupSamplesByLocation(props.GeoData.features) : {};

return (
    <div>
        <MapContainer
          className='min-h-[68vh] '
          center={[32.1, -7.7]}
          zoom={10}
          minZoom={6}
          scrollWheelZoom={true}
          maxBounds={maxBounds}
        >
          <TileLayer key={'e'} url={"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"} attribution={'Tiles © <a href="https://services.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer">ArcGIS</a> | <a href="https://crsa.um6p.ma/">Selmas project - CRSA @ UM6P</a>'} />
          { props.GeoData && (
            <MarkerClusterGroup
              iconCreateFunction={cluster => {
                const count = cluster.getChildCount();
                return L.divIcon({
                  html: `<div style="
                    background-color: #1976d2;
                    color: white;
                    border-radius: 50%;
                    width: 40px;
                    height: 40px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 16px;
                    border: 2px solid #fff;
                    box-shadow: 0 0 10px rgba(0,0,0,0.3);
                  ">${count}</div>`,
                  className: 'custom-cluster-icon',
                  iconSize: [40, 40]
                });
              }}
            >
              {Object.entries(groupedSamples).map(([locationKey, locationData], idx) => {
                const { coordinates, samples } = locationData;
                const sampleCount = samples.length;
                
                return (
                  <Marker
                    key={locationKey}
                    position={coordinates}
                    icon={greenIcon}
                    eventHandlers={{
                      click: (e) => {
                        // Set only the Code_labo values as a list
                        props.setSelectedSample(samples);
                        console.log("sampleCodes",samples);
                      },
                      mouseover: (e) => {
                        e.target.openTooltip();
                      },
                      mouseout: (e) => {
                        e.target.closeTooltip();
                      }
                    }}
                  >
                    <Tooltip
                      direction="auto"
                      className="custom-tooltip"
                      permanent={false}
                    >
                      <span>
                        {sampleCount} soil sample{sampleCount > 1 ? 's' : ''}<br />
                        Location: {coordinates[0].toFixed(4)}, {coordinates[1].toFixed(4)}
                      </span>
                    </Tooltip>
                  </Marker>
                );
              })}
            </MarkerClusterGroup>
          )}

          {props.stationCoordonates && props.stationCoordonates.lat && props.stationCoordonates.lon}
          {/* <Popup>
            A pretty CSS3 popup. <br /> Easily customizable.
          </Popup> */}
          
          
      </MapContainer>
    </div>
)
}

export default DashboardMap