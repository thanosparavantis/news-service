import {initializeApp} from "firebase/app";
import {collection, doc, getDoc, getDocs, getFirestore, orderBy, query, where} from "firebase/firestore";
import {cache} from "react";
import {extractEmoji} from "@/app/utility/emojis";

export const firebaseOptions = {
  apiKey: process.env.FIREBASE_API_KEY,
  authDomain: process.env.FIREBASE_AUTH_DOMAIN,
  projectId: process.env.FIREBASE_PROJECT_ID,
  storageBucket: process.env.FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.FIREBASE_MESSAGING_SERVER_ID,
  appId: process.env.FIREBASE_APP_ID,
};

const app = initializeApp(firebaseOptions);
const db = getFirestore(app);

console.info("Initialize firestore");

export const getMunicipalities = cache(async () => {
  console.info("Get municipalities");

  const municipalities = [];
  const municipalitiesRef = collection(db, "municipalities");
  const snapshot = await getDocs(municipalitiesRef);

  const oneDayAgo = new Date();
  oneDayAgo.setDate(oneDayAgo.getDate() - 1);

  for (const doc of snapshot.docs) {
    const data = doc.data();

    if (data.headline === null) {
      continue;
    }

    const coordinates = [data.coordinates.latitude, data.coordinates.longitude];
    const timestamp = data.timestamp.toDate();

    municipalities.push({
      name: data.name,
      slug: doc.id,
      coordinates: coordinates,
      headline: data.headline,
      emoji: extractEmoji(data.headline),
      timestamp: timestamp,
      isActive: timestamp >= oneDayAgo,
    })
  }

  return municipalities;
});

export const getAvailableSlugs = async () => {
  console.info("Get available slugs");

  const snapshot = await getDocs(collection(db, "municipalities"));
  return snapshot.docs.map(doc => {
    return {
      slug: doc.id,
    }
  });
};

export const getMunicipalityFromSlug = cache(async (slug) => {
  console.info(`Get municipality from slug: ${slug}`);

  const snapshot = await getDoc(doc(db, "municipalities", slug));
  const data = snapshot.data();
  const summariesRef = collection(db, "municipalities", snapshot.id, "summaries");

  const oneWeekAgo = new Date();
  oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);
  const q = query(summariesRef, where("timestamp", ">=", oneWeekAgo), orderBy("timestamp", "desc"));

  const summariesSnap = await getDocs(q);

  const summaries = summariesSnap.docs.map((doc) => {
    const summary = doc.data();

    return {
      id: doc.id,
      headline: summary.headline,
      timestamp: summary.timestamp.toDate(),
    }
  });

  return {
    name: data.name,
    slug: snapshot.id,
    summaries: groupItemsByDate(summaries),
  }
});

const groupItemsByDate = ((items) => {
  const grouped = items.reduce((group, summary) => {
    const dateHeader = formatDateHeader(summary.timestamp);

    if (!group[dateHeader]) {
      group[dateHeader] = [];
    }

    group[dateHeader].push(summary);
    return group;
  }, {});

  return Object.keys(grouped).map(dateHeader => ({
    dateHeader: dateHeader,
    summaries: grouped[dateHeader],
  }));
});

const formatDateHeader = ((date) => {
  const today = new Date();
  const yesterday = new Date();
  yesterday.setDate(today.getDate() - 1);

  if (date.toDateString() === today.toDateString()) {
    return 'Σήμερα';
  } else if (date.toDateString() === yesterday.toDateString()) {
    return 'Χθες';
  } else {
    return date.toLocaleDateString('el-GR', {day: 'numeric', month: 'long', year: 'numeric'});
  }
});
