import {config} from "@fortawesome/fontawesome-svg-core";
import "@fortawesome/fontawesome-svg-core/styles.css";
import dynamic from "next/dynamic";
import {getMunicipalities} from "@/app/utility/queries";

config.autoAddCss = false;

export const revalidate = 600;

const ClientLeafletMap = dynamic(() => import("@/app/components/leaflet-map"), {
  ssr: false
});

export default async function Home() {
  const municipalities = await getMunicipalities();

  return (
    <main>
      <ClientLeafletMap municipalities={municipalities}/>
    </main>
  );
}
