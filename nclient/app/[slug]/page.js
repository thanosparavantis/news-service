import {getAvailableSlugs, getMunicipalityFromSlug} from "@/app/utility/queries";
import SummaryPreview from "@/app/[slug]/summary-preview";

export const revalidate = 600;
export const dynamicParams = false;

export const generateStaticParams = async () => {
  return await getAvailableSlugs();
};

export default async function Location({params}) {
  const municipality = await getMunicipalityFromSlug(params.slug);

  return (
    <div className="mt-12 flex items-center justify-center">
      <div className="mb-5 mx-3 max-w-3xl container md:mx-0">
        <div className="my-10 text-2xl font-semibold text-gray-900 tracking-wide text-center">
          {municipality.name}
        </div>
        {municipality.summaries.length === 0 ? (
          <div className="p-5 bg-white rounded shadow border text-sm">
            Δεν βρέθηκαν πρόσφατες ειδήσεις.
          </div>
        ) : (
          <div className="flex flex-col gap-8">
            {municipality.summaries.map(({dateHeader, summaries}) => {
              return (
                <div key={dateHeader} className="flex flex-col gap-3">
                  <div className="font-semibold text-gray-600 tracking-wide">
                    {dateHeader}
                  </div>
                  <div className="flex flex-col gap-3">
                    {summaries.map((item) => {
                      return <SummaryPreview key={item.id} item={item}/>
                    })}
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </div>
    </div>
  )
}