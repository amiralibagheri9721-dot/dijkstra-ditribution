const map = L.map('map').setView([32,53], 5);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {}).addTo(map);

let markers = [];
let lines = [];

const nodes_coords = {
"Tehran":[35.6892,51.3890],"Mashhad":[36.2605,59.6168],"Isfahan":[32.6525,51.6776],
"Tabriz":[38.0700,46.2969],"Shiraz":[29.6100,52.5311],"Ahvaz":[31.3183,48.6706],
"Qom":[34.6416,50.8746],"Kermanshah":[34.3142,47.0650],"Urmia":[37.5553,45.0728],
"Zahedan":[29.4963,60.8629],"Rasht":[37.2808,49.5832],"Yazd":[31.8974,54.3569],
"Arak":[34.0917,49.7010],"Kerman":[30.2839,57.0788],"Bandar Abbas":[27.1964,56.2873],
"Hamedan":[34.7980,48.5150],"Sanandaj":[35.3095,46.9980],"Khorramabad":[33.4878,48.3558],
"Birjand":[32.8663,59.2211],"Sari":[36.5633,53.0601],"Bojnurd":[37.4747,57.3349],
"Gorgan":[36.8436,54.4390],"Zanjan":[36.6736,48.4787],"Qazvin":[36.2688,50.0041],
"Kashan":[33.9850,51.4576],"Ardabil":[38.2498,48.2933],"Babol":[36.5383,52.6780],
"Shahrekord":[32.3266,50.8571],"Dezful":[32.3830,48.3989],"Khoy":[38.5500,44.9500],
"Bushehr":[28.9234,50.8203]
};

async function fetchCenters(){
    const res = await fetch("https://YOUR_RENDER_URL/compute"); // ← آدرس Render خودت
    const data = await res.json();

    markers.forEach(m=>map.removeLayer(m));
    lines.forEach(l=>map.removeLayer(l));
    markers=[]; lines=[];

    data.centers.forEach(c=>{
        let m = L.circleMarker([c.lat,c.lon],{color:'red',radius:10}).addTo(map).bindPopup(c.name);
        markers.push(m);
    });

    const centers_coords = data.centers.map(c=>[c.lat,c.lon]);
    for(const city in nodes_coords){
        let cityLatLon = nodes_coords[city];
        let minDist = Infinity, nearest = null;
        centers_coords.forEach(c=>{
            const d = Math.sqrt(Math.pow(cityLatLon[0]-c[0],2)+Math.pow(cityLatLon[1]-c[1],2));
            if(d<minDist){minDist=d; nearest=c;}
        });
        let line = L.polyline([cityLatLon, nearest], {color:'blue', weight:2}).addTo(map);
        lines.push(line);
    }

    document.getElementById("weightedDistance").innerText = "میانگین فاصله وزنی: "+data.weighted_distance.toFixed(2);
}