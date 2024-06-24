"use client";

import {useEffect, useMemo, useState} from "react";
import {MapContainer, TileLayer} from "react-leaflet";

import "leaflet/dist/leaflet.css";
import LeafletEventListener from "@/app/components/leaflet-event-listener";
import "@/app/utility/timeAgoInit";
import LeafletMunicipality from "@/app/components/leaflet-municipality";

export default function LeafletMap({municipalities}) {
  const [center, setCenter] = useState(() => {
    const mapData = localStorage.getItem("MapData");

    if (mapData) {
      const mapProperties = JSON.parse(mapData);
      return mapProperties.center;
    }

    return [37.9838, 23.7275];
  })

  const [zoom, setZoom] = useState(() => {
    const mapData = localStorage.getItem("MapData");

    if (mapData) {
      const mapProperties = JSON.parse(mapData);
      return mapProperties.zoom;
    }

    return 8;
  })

  const mapPropertiesStr = useMemo(() => {
    return JSON.stringify({
      center: center, zoom: zoom
    });
  }, [center, zoom]);

  useEffect(() => {
    const mapData = localStorage.getItem("MapData");

    if (mapData !== mapPropertiesStr) {
      localStorage.setItem("MapData", mapPropertiesStr);
    }
  }, [mapPropertiesStr]);

  const municipalityMarkers = useMemo(() => {
    return municipalities.map((municipality) => <LeafletMunicipality key={municipality.slug} municipality={municipality}/>);
  }, [municipalities]);

  return (
    <MapContainer
      preferCanvas={true}
      center={center}
      zoom={zoom}
      zoomControl={false}
      className="h-screen"
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {municipalityMarkers}
      <LeafletEventListener setCenter={setCenter} setZoom={setZoom}/>
    </MapContainer>
  )
}

