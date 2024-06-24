import {useMap} from "react-leaflet";
import {useEffect, useMemo} from "react";
import LeafletPopup from "@/app/components/leaflet-popup";
import {createRoot} from "react-dom/client";
import L from "leaflet";
import "leaflet-canvas-markers";
import {createEmojiMarker} from "@/app/utility/emojis";
import {useRouter} from "next/navigation";


export default function LeafletMunicipality({municipality}) {
  const map = useMap();
  const router = useRouter();

  const marker = useMemo(() => {
    const canvasMarker = L.canvasMarker(municipality.coordinates, {
      radius: 10,
      img: {
        url: createEmojiMarker(municipality.emoji, municipality.isActive),
        size: [16, 16],
      }
    });

    canvasMarker.bindPopup(() => {
      const div = document.createElement("div");
      const root = createRoot(div);

      root.render(<LeafletPopup
        municipality={municipality}
        handleNavigation={() => router.push(`/${municipality.slug}`)}
      />)

      return div;
    })

    return canvasMarker;
  }, [municipality, router]);

  useEffect(() => {
    marker.addTo(map);
    return () => marker.removeFrom(map);
  }, [map, marker]);

  return null;
}