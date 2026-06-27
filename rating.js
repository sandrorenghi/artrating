const W = {
  museumA:50, museumB:30, museumC:15, museumD:5,
  galleryA:25, galleryB:15, galleryC:8, galleryD:3,
  prizeA:30, prizeB:15, prizeC:7,
  fairA:5, fairB:3, fairC:1,
  leader:10, movement:10, cr:10, found:10, privColl:8,
  curIntl:15, curNaz:8,
  mono:0.1, cat:0.1, solo:0.1, group:0.1,
  auction1:0.000005, auction3:0.000005,
  fakes:-1,
  search:0.000002, citCritiche:2, citMedia:1, citSocial:0.3
};

function calcRating(a) {
  const museumPts  = (a.museumA||[]).length*W.museumA + (a.museumB||[]).length*W.museumB + (a.museumC||[]).length*W.museumC + (a.museumD||[]).length*W.museumD;
  const galleryPts = (a.galleryA||[]).length*W.galleryA + (a.galleryB||[]).length*W.galleryB + (a.galleryC||[]).length*W.galleryC + (a.galleryD||[]).length*W.galleryD;
  const prizePts   = (a.prizeA||[]).length*W.prizeA + (a.prizeB||[]).length*W.prizeB + (a.prizeC||[]).length*W.prizeC;
  const fairPts    = (a.fairA||[]).length*W.fairA + (a.fairB||[]).length*W.fairB + (a.fairC||[]).length*W.fairC;
  const docPts     = (a.leader==='si'?W.leader:0) + (a.movement?W.movement:0) + (a.cr==='si'?W.cr:0) + (a.found==='si'?W.found:0) + (a.privColl==='si'?W.privColl:0) + (a.cur==='intl'?W.curIntl:a.cur==='naz'?W.curNaz:0);
  const expoPts    = (a.mono||0)*W.mono + (a.cat||0)*W.cat + (a.solo||0)*W.solo + (a.group||0)*W.group;
  const mktPts     = (a.auction1||0)*W.auction1*1000000 + (a.auction3||0)*W.auction3*1000000 + (a.fakes||0)*W.fakes;
  const webPts     = (a.search||0)*W.search + (a.citCritiche||0)*W.citCritiche + (a.citMedia||0)*W.citMedia + (a.citSocial||0)*W.citSocial;
  const total = museumPts+galleryPts+prizePts+fairPts+docPts+expoPts+mktPts+webPts;
  return { total:Math.round(total), museumPts, galleryPts, prizePts, fairPts, docPts, expoPts, mktPts, webPts };
}

function stars(r) {
  if(r>=3000) return '★★★★★';
  if(r>=1500) return '★★★★☆';
  if(r>=800)  return '★★★☆☆';
  if(r>=300)  return '★★☆☆☆';
  return '★☆☆☆☆';
}

function clusterLabel(r) {
  if(r>=3000) return {label:'Premier League', cls:'cl-premier'};
  if(r>=1500) return {label:'Serie A', cls:'cl-a'};
  if(r>=800)  return {label:'Serie B', cls:'cl-b'};
  if(r>=300)  return {label:'Serie C', cls:'cl-c'};
  return {label:'Emergente', cls:'cl-em'};
}

function fmtM(n) {
  if(n>=1000) return '€'+Math.round(n/1000)+'B';
  if(n>=1)    return '€'+n.toLocaleString('it-IT',{maximumFractionDigits:1})+'M';
  return '€'+(n*1000).toLocaleString('it-IT',{maximumFractionDigits:0})+'K';
}

function fmtPts(n) { return Math.round(n).toLocaleString('it-IT'); }
