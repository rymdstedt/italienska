const fs=require('fs');
const html=fs.readFileSync(process.argv[2],'utf8');
const js=html.match(/<script>([\s\S]*)<\/script>/)[1];
const data=js.slice(js.indexOf('var LEVELS'), js.indexOf('/* ---------- Index'));
eval(data.replace('var LEVELS','global.LEVELS'));
function audioKey(t){var h=0x811c9dc5;for(var i=0;i<t.length;i++){h^=t.charCodeAt(i);h=Math.imul(h,0x01000193)>>>0;}return ('0000000'+h.toString(16)).slice(-8);}
const texts=new Set(["Ciao! Benvenuta al corso di italiano."]);
LEVELS.forEach(l=>l.lessons.forEach(x=>x.items.forEach(a=>texts.add(a[0].split('|')[0]))));
const out={}; for(const t of texts){const k=audioKey(t); if(out[k]&&out[k]!==t) throw new Error('collision '+t); out[k]=t;}
fs.writeFileSync(process.argv[3],JSON.stringify(out,null,1));
console.log(Object.keys(out).length,'phrases');
