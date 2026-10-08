// Natural Earth 110m land (public domain, via npm world-atlas) -> equirectangular SVG path
const fs=require('fs');const topo=require('topojson-client');
const t=JSON.parse(fs.readFileSync('node_modules/world-atlas/land-110m.json','utf8'));
const land=topo.feature(t,t.objects.land);
const W=720,H=360;
const px=(lon,lat)=>[ (lon+180)/360*W, (90-lat)/180*H ];
function ringArea(r){let a=0;for(let i=0;i<r.length-1;i++){a+=r[i][0]*r[i+1][1]-r[i+1][0]*r[i][1];}return Math.abs(a/2);}
let d='';let kept=0,dropped=0;
const geoms=land.type==='FeatureCollection'?land.features.map(f=>f.geometry):[land.geometry];
for(const g of geoms){
  const polys=g.type==='Polygon'?[g.coordinates]:g.coordinates;
  for(const poly of polys){
    for(const ring of poly){
      const pts=ring.map(([lon,lat])=>px(lon,lat));
      if(ringArea(pts)<3.5){dropped++;continue;}
      // simplify: drop points closer than 0.6 units to previous kept
      const out=[pts[0]];
      for(let i=1;i<pts.length;i++){const p=pts[i],q=out[out.length-1];if(Math.hypot(p[0]-q[0],p[1]-q[1])>=1.15||i===pts.length-1)out.push(p);}
      if(out.length<4){dropped++;continue;}
      d+='M'+out.map(p=>p[0].toFixed(1)+' '+p[1].toFixed(1)).join('L')+'Z';kept++;
    }
  }
}
fs.writeFileSync('world.json',JSON.stringify({w:W,h:H,d,source:'Natural Earth 110m land (public domain), via world-atlas@2'}));
console.log('rings kept',kept,'dropped',dropped,'path bytes',d.length);
