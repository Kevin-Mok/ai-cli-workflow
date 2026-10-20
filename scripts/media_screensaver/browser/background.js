/* A persistent native port and one-second traffic keep the MV3 worker alive. */
if (typeof module === "undefined") importScripts("content.js");
const geometry = typeof module !== "undefined" ? require("./content.js") : globalThis.MediaScreensaverGeometry;

function desktopBounds(metrics, window, zoom) {
  const scale = metrics.devicePixelRatio/zoom;
  if (!Number.isFinite(scale) || zoom <= 0 || scale < 0.25 || scale > 8) throw new Error("uncertain display scaling");
  return geometry.validRect({x:window.left*scale,y:window.top*scale,
    width:window.width*scale,height:window.height*scale});
}

function desktopRects(metrics, window, zoom, videos) {
  const numbers = [metrics.screenX,metrics.screenY,metrics.outerWidth,metrics.outerHeight,
    metrics.innerWidth,metrics.innerHeight,metrics.devicePixelRatio,zoom,
    window.left,window.top,window.width,window.height];
  if (!numbers.every(Number.isFinite) || zoom <= 0 || metrics.devicePixelRatio <= 0
      || metrics.innerWidth < 0 || metrics.innerHeight < 0) throw new Error("uncertain window geometry");
  const scale = metrics.devicePixelRatio/zoom;
  const bounds = desktopBounds(metrics,window,zoom);
  for (const [a,b] of [[metrics.screenX,window.left],[metrics.screenY,window.top],
    [metrics.outerWidth,window.width],[metrics.outerHeight,window.height]]) {
    if (Math.abs(a-b) > 2) throw new Error("window geometry changed during collection");
  }
  const border = (metrics.outerWidth-metrics.innerWidth*zoom)/2;
  const top = metrics.outerHeight-metrics.innerHeight*zoom-border;
  if (border < -2 || border > 16 || top < -2 || top > 300) throw new Error("uncertain browser chrome geometry");
  const origin = {x:(window.left+Math.max(0,border))*scale,y:(window.top+Math.max(0,top))*scale};
  return videos.map(rect => {
    geometry.validRect(rect);
    return geometry.clipRect({x:origin.x+rect.x*metrics.devicePixelRatio,y:origin.y+rect.y*metrics.devicePixelRatio,
      width:rect.width*metrics.devicePixelRatio,height:rect.height*metrics.devicePixelRatio},bounds);
  }).filter(Boolean);
}

function combineFrames(frames, snapshots, mappings) {
  const byId = new Map(frames.map(frame => [frame.frameId,frame]));
  if (!byId.has(0) || frames.length > 256) throw new Error("frame hierarchy unavailable");
  const output = [];
  for (const frame of frames) {
    const snapshot = snapshots.get(frame.frameId);
    if (!snapshot || snapshot.healthy === false || !Array.isArray(snapshot.videos)) throw new Error("frame snapshot unavailable");
    let rects = snapshot.videos.map(rect => geometry.clipRect(rect,snapshot.viewport)).filter(Boolean);
    let current = frame;
    const visited = new Set();
    while (current.frameId !== 0) {
      if (visited.has(current.frameId)) throw new Error("frame hierarchy cycle");
      visited.add(current.frameId);
      const mapping = mappings.get(current.frameId);
      const parent = byId.get(current.parentFrameId);
      if (!mapping || mapping.valid === false || !parent || mapping.parentFrameId !== current.parentFrameId) {
        throw new Error("frame position unavailable");
      }
      const viewport = snapshots.get(current.frameId).viewport;
      if (mapping.clip !== null && (Math.abs(mapping.rect.width-viewport.width) > 2
          || Math.abs(mapping.rect.height-viewport.height) > 2)) throw new Error("frame resized during collection");
      rects = geometry.mapFrameRects(rects,mapping.rect,viewport);
      if (Object.hasOwn(mapping,"clip")) rects = mapping.clip ? rects.map(rect => geometry.clipRect(rect,mapping.clip)).filter(Boolean) : [];
      rects = rects.map(rect => geometry.clipRect(rect,snapshots.get(parent.frameId).viewport)).filter(Boolean);
      current = parent;
    }
    output.push(...rects);
  }
  return output;
}

if (typeof module !== "undefined") module.exports = {desktopRects,desktopBounds,combineFrames};

if (typeof chrome !== "undefined" && chrome.runtime && chrome.windows) {
  let port = null;
  let busy = false;
  const scans = new Map();
  const pause = milliseconds => new Promise(resolve => setTimeout(resolve,milliseconds));
  chrome.runtime.onMessage.addListener((message,sender) => {
    if (sender.id !== chrome.runtime.id || message.kind !== "media-frame-mapping") return;
    const scan = scans.get(message.scan);
    if (!scan || sender.tab?.id !== scan.tabId) return;
    const expected = scan.parents.get(message.frameId);
    if (expected !== sender.frameId) {
      scan.conflicted = true;
      return;
    }
    const mapping = {...message.mapping,parentFrameId:sender.frameId};
    const previous = scan.mappings.get(message.frameId);
    if (previous && JSON.stringify(previous) !== JSON.stringify(mapping)) scan.conflicted = true;
    scan.mappings.set(message.frameId,mapping);
  });
  async function collectTab(tabId, window) {
    const frames = await chrome.webNavigation.getAllFrames({tabId});
    if (!frames || !frames.length || frames.length > 256) throw new Error("frame hierarchy unavailable");
    const results = await chrome.scripting.executeScript({target:{tabId,allFrames:true},
      func:() => globalThis.__mediaScreensaverSnapshot?.() || null});
    const snapshots = new Map(results.map(item => [item.frameId,item.result]));
    for (const frame of frames) {
      if (!snapshots.get(frame.frameId)?.healthy) throw new Error("frame cannot be inspected");
    }
    const scanId = crypto.randomUUID();
    const scan = {tabId,parents:new Map(),mappings:new Map(),conflicted:false};
    const children = new Map();
    const emissions = [];
    for (const frame of frames) {
      if (frame.frameId === 0) continue;
      const token = crypto.randomUUID();
      scan.parents.set(frame.frameId,frame.parentFrameId);
      if (!children.has(frame.parentFrameId)) children.set(frame.parentFrameId,[]);
      children.get(frame.parentFrameId).push({token,frameId:frame.frameId});
      emissions.push({token,frameId:frame.frameId});
    }
    scans.set(scanId,scan);
    try {
      await Promise.all([...children].map(([frameId,list]) => chrome.tabs.sendMessage(tabId,
        {kind:"media-map-configure",scan:scanId,children:list},{frameId})));
      await Promise.all(emissions.map(({frameId,token}) => chrome.tabs.sendMessage(tabId,
        {kind:"media-map-emit",scan:scanId,token},{frameId})));
      if (emissions.length) await pause(150);
      if (scan.conflicted) throw new Error("frame association uncertain");
      const videos = combineFrames(frames,snapshots,scan.mappings);
      const zoom = await chrome.tabs.getZoom(tabId);
      const metrics = snapshots.get(0).metrics;
      return {videos:desktopRects(metrics,window,zoom,videos),bounds:desktopBounds(metrics,window,zoom)};
    } finally {
      scans.delete(scanId);
    }
  }
  function connect() {
    if (port) return;
    try {
      port = chrome.runtime.connectNative("org.kevin.media_screensaver");
      port.onMessage.addListener(() => {});
      port.onDisconnect.addListener(() => {
        void chrome.runtime.lastError;
        port = null;
        setTimeout(connect,1000);
      });
    } catch (_) {
      port = null;
      setTimeout(connect,1000);
    }
  }
  async function tick() {
    if (busy) return;
    connect();
    if (!port) return;
    busy = true;
    const state = {version:1,healthy:true,windows:[]};
    try {
      const windows = await chrome.windows.getAll({populate:true,windowTypes:["normal","popup"]});
      await Promise.all(windows.map(async window => {
        const record = {id:window.id,state:window.state,
          bounds:{x:0,y:0,width:0,height:0},videos:[]};
        state.windows.push(record);
        if (window.state === "minimized") return;
        const active = window.tabs?.find(tab => tab.active);
        if (!active) throw new Error("active tab unavailable");
        const result = await Promise.race([collectTab(active.id,window),
          new Promise((_,reject) => setTimeout(() => reject(new Error("browser collection timed out")),2000))]);
        record.bounds = result.bounds;
        record.videos = result.videos.map(rect => ({playing:true,rect}));
      }));
    } catch (_) {
      state.healthy = false;
      state.windows = [];
    }
    try {
      port?.postMessage(state);
    } catch (_) {
      port = null;
    } finally {
      busy = false;
    }
  }
  connect();
  void tick();
  setInterval(() => void tick(),1000);
}
