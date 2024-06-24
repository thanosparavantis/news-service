"use client";

import ReactTimeAgo from "react-time-ago";
import "@/app/utility/timeAgoInit";

export default function SummaryPreview({item}) {
  return (
    <div className="p-5 flex flex-col justify-between gap-3 bg-white rounded shadow border text-sm md:flex-row">
      <div className="text-gray-900">
        {item.headline}
      </div>
      <div className="flex-shrink-0 text-right text-gray-600">
        <ReactTimeAgo date={item.timestamp} locale="el-GR" className=""/>
      </div>
    </div>
  )
}