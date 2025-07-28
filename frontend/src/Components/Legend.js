import { useEffect } from 'react';
import L from 'leaflet';
import { useMap } from 'react-leaflet';

const iconed = (color, name) => {

  return `
    <div style="display: flex; align-items: center; margin: 4px;">
      <svg height="20" width="20" xmlns="http://www.w3.org/2000/svg" style="flex-shrink: 0;">
        <circle r="8" cx="10" cy="10" fill="${color}" />
      </svg>
      <span style="margin-left: 8px;">${name}</span>
    </div>`;
    
  }
  


function Legend(props) {    
    const map = useMap()
    useEffect(() => {
        if (map){
            const legend = L.control({ position: "topright" });
    
            legend.onAdd = () => {
                const div = L.DomUtil.create('div', 'info legend');
                div.innerHTML += iconed("#39ba30", "Soil samples");
                div.innerHTML += iconed("#1976d2", "Water samples");

                     return div;
            }
    
            legend.addTo(map);
            return () => {
                map.removeControl(legend);
              };
        }
    },[props.layers]);
    return null
}

export default Legend