// netlify/functions/icu.js
// Proxy ICU API — VeloCoach AI v12
// Variables d'environnement Netlify requises : ICU_API_KEY, ICU_ATHLETE_ID

const ATHLETE_ID = process.env.ICU_ATHLETE_ID || '45440995';
const API_KEY    = process.env.ICU_API_KEY;
const BASE       = 'https://intervals.icu/api/v1';

function auth() {
  return 'Basic ' + Buffer.from('API_KEY:' + API_KEY).toString('base64');
}

async function icuFetch(path) {
  const res = await fetch(BASE + path, {
    headers: { 'Authorization': auth(), 'Accept': 'application/json' }
  });
  if (!res.ok) throw new Error(`ICU ${res.status}: ${path}`);
  return res.json();
}

function isoWeek(date) {
  const d = new Date(date);
  d.setHours(0,0,0,0);
  d.setDate(d.getDate() + 3 - (d.getDay() + 6) % 7);
  const week1 = new Date(d.getFullYear(), 0, 4);
  return 1 + Math.round(((d - week1) / 86400000 - 3 + (week1.getDay() + 6) % 7) / 7);
}

exports.handler = async (event) => {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Content-Type': 'application/json'
  };

  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: '' };
  }

  if (!API_KEY) {
    return { statusCode: 500, headers, body: JSON.stringify({ error: 'ICU_API_KEY manquante dans les variables Netlify' }) };
  }

  try {
    const today     = new Date();
    const todayStr  = today.toISOString().slice(0, 10);
    const d30ago    = new Date(today); d30ago.setDate(today.getDate() - 30);
    const d30str    = d30ago.toISOString().slice(0, 10);
    const d14ago    = new Date(today); d14ago.setDate(today.getDate() - 14);
    const d14str    = d14ago.toISOString().slice(0, 10);

    // Appels parallèles
    const [wellnessArr, activitiesArr] = await Promise.all([
      icuFetch(`/athlete/${ATHLETE_ID}/wellness?oldest=${d30str}&newest=${todayStr}`),
      icuFetch(`/athlete/${ATHLETE_ID}/activities?oldest=${d14str}&newest=${todayStr}&activity_type=Ride`)
    ]);

    // Trier wellness du plus récent au plus ancien
    const wellness = [...wellnessArr].sort((a, b) => b.id.localeCompare(a.id));

    // Trouver l'entrée wellness avec données HRV valides
    const latestHRV = wellness.find(w => w.hrv && w.hrv > 0) || wellness[0];

    // CTL/ATL/TSB depuis l'entrée la plus récente
    const latest = wellness[0] || {};
    const ctl   = latest.ctl   || 0;
    const atl   = latest.atl   || 0;
    const tsb   = +(ctl - atl).toFixed(1);
    const ramp  = latest.rampRate || 0;

    // Activités : enrichir avec kJ, découplage, etc.
    const acts = activitiesArr.slice(0, 10).map(a => ({
      id:     a.id,
      date:   a.start_date_local?.slice(0, 10),
      name:   a.name,
      kj:     Math.round((a.icu_joules || 0) / 1000),
      tss:    a.icu_training_load || 0,
      np:     a.icu_weighted_avg_watts || 0,
      dist:   +((a.distance || 0) / 1000).toFixed(1),
      elev:   Math.round(a.total_elevation_gain || 0),
      dec:    +(a.decoupling || 0).toFixed(2),
      ef:     +(a.icu_efficiency_factor || 0).toFixed(3),
      vi:     +(a.icu_variability_index || 0).toFixed(3),
      hr:     Math.round(a.average_heartrate || 0),
      hrmax:  Math.round(a.max_heartrate || 0),
      dur:    (() => {
        const s = a.moving_time || 0;
        const h = Math.floor(s / 3600);
        const m = Math.floor((s % 3600) / 60);
        return h > 0 ? h + 'h' + String(m).padStart(2,'0') : m + 'min';
      })(),
      type:   (() => {
        const np = a.icu_weighted_avg_watts || 0;
        const ftp = 222;
        const pct = np / ftp;
        if (pct >= 1.05) return 'A';
        if (pct >= 0.88) return 'SS';
        if (pct >= 0.76) return 'Z2';
        return 'R';
      })()
    }));

    // Semaine ISO courante
    const weekNum = isoWeek(todayStr);

    // KJ semaine en cours (lundi ISO → aujourd'hui)
    const mondayOfWeek = new Date(today);
    mondayOfWeek.setDate(today.getDate() - (today.getDay() + 6) % 7);
    const mondayStr = mondayOfWeek.toISOString().slice(0, 10);
    const kjWeek = activitiesArr
      .filter(a => a.start_date_local >= mondayStr)
      .reduce((s, a) => s + Math.round((a.icu_joules || 0) / 1000), 0);

    // Wellness 14 jours pour graphes CTL/ATL
    const wellnessChart = wellness.slice(0, 14).reverse().map(w => ({
      date:  w.id,
      ctl:   +(w.ctl || 0).toFixed(1),
      atl:   +(w.atl || 0).toFixed(1),
      tsb:   +((w.ctl || 0) - (w.atl || 0)).toFixed(1),
      hr:    w.restingHR || null,
      hrv:   w.hrv || null,
      sdnn:  w.hrvSDNN || null,
      sleep: w.sleepSecs || null,
      score: w.sleepScore || null,
      readiness: w.readiness || null
    }));

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        ok: true,
        syncTime: new Date().toISOString(),
        // Forme du jour
        ctl, atl, tsb, ramp: +(ramp).toFixed(2),
        weekNum,
        kjWeek,
        // Santé du jour
        hrv:       latestHRV?.hrv || null,
        sdnn:      latestHRV?.hrvSDNN || null,
        restingHR: latest.restingHR || null,
        readiness: latest.readiness || null,
        vo2max:    latest.vo2max || null,
        sleepSecs: latest.sleepSecs || null,
        sleepScore: latest.sleepScore || null,
        // Historique
        wellness:  wellnessChart,
        acts
      })
    };

  } catch (err) {
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: err.message })
    };
  }
};
