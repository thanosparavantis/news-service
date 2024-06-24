import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faArrowRight} from "@fortawesome/free-solid-svg-icons";
import ReactTimeAgo from "react-time-ago";

export default function LeafletPopup({municipality, handleNavigation}) {

  return (
    <div className="flex flex-col gap-3 px-5 py-3">
      <div className="text-sm font-bold tracking-wide text-gray-900">
        {municipality.name}
      </div>
      <div className="text-sm text-gray-600 whitespace-pre-line">
        {municipality.headline ? municipality.headline : "Δεν υπάρχει διαθέσιμη περιγραφή."}
      </div>
      {municipality.timestamp && (
        <div className="flex flex-wrap justify-between font-semibold text-xs">
          <button
            onClick={handleNavigation}
            className="flex items-center flex-grow gap-1 text-app-link hover:underline"
          >
            Περισσότερα
            <FontAwesomeIcon icon={faArrowRight} size="sm"/>
          </button>
          <div className="text-gray-600">
            <ReactTimeAgo date={municipality.timestamp} locale="el-GR"/>
          </div>
        </div>
      )}
    </div>
  )
}