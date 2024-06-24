import {useMapEvents} from "react-leaflet";

export default function LeafletEventListener({setCenter, setZoom}) {
  useMapEvents({
    click: (event) => {
      const { lat, lng } = event.latlng;
      console.debug(`[${lat.toFixed(5)}, ${lng.toFixed(5)}]`);
    },
    moveend: (event) => {
      const center = event.target.getCenter();
      const zoom = event.target.getZoom();
      setCenter(center);
      setZoom(zoom);
    }
  });
}