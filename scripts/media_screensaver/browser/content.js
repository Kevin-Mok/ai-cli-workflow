/* Geometry only: page content and URLs never cross the extension boundary. */
function validRect(rect) {
  if (!rect || ![rect.x, rect.y, rect.width, rect.height].every(Number.isFinite)
      || rect.width < 0 || rect.height < 0
      || [rect.x, rect.y, rect.width, rect.height].some(n => Math.abs(n) > 1000000)) {
    throw new Error("uncertain frame geometry");
  }
  return rect;
}

function clipRect(rect, clip) {
  validRect(rect);
  validRect(clip);
  const x = Math.max(rect.x, clip.x);
  const y = Math.max(rect.y, clip.y);
  const right = Math.min(rect.x + rect.width, clip.x + clip.width);
  const bottom = Math.min(rect.y + rect.height, clip.y + clip.height);
  return right > x && bottom > y ? {x, y, width:right-x, height:bottom-y} : null;
}

function mapFrameRects(rects, frame, viewport) {
  validRect(frame);
  validRect(viewport);
  return rects.map(rect => clipRect(rect, viewport)).filter(Boolean)
    .map(rect => clipRect({x:frame.x+rect.x, y:frame.y+rect.y,
      width:rect.width, height:rect.height}, frame)).filter(Boolean);
}

function findElements(root, selector, dom = globalThis.chrome?.dom) {
  if (typeof dom?.openOrClosedShadowRoot !== "function") throw new Error("shadow inspection unavailable");
  const found = [...root.querySelectorAll(selector)];
  for (const element of root.querySelectorAll("*")) {
    const shadow = dom.openOrClosedShadowRoot(element);
    if (shadow) found.push(...findElements(shadow,selector,dom));
  }
  return found;
}

function assertUntransformed(style) {
  if (style.transform !== "none" || (style.zoom && !["1","normal"].includes(style.zoom))) {
    throw new Error("uncertain transformed geometry");
  }
}

function isPlayingVideo(video) {
  return !video.paused && !video.ended && video.readyState >= 2
    && video.videoWidth > 0 && video.videoHeight > 0;
}

const mediaGeometry = {validRect, clipRect, mapFrameRects, findElements, assertUntransformed, isPlayingVideo};
if (typeof module !== "undefined") module.exports = mediaGeometry;
globalThis.MediaScreensaverGeometry = mediaGeometry;

if (typeof document !== "undefined" && typeof chrome !== "undefined" && chrome.runtime) {
  const viewport = () => ({x:0,y:0,width:innerWidth,height:innerHeight});
  function parentElementOrHost(element) {
    return element.parentElement || element.getRootNode().host || null;
  }
  function visibleRect(element, initial) {
    let result = clipRect(initial, viewport());
    for (let node = element; node && result; node = parentElementOrHost(node)) {
      const style = getComputedStyle(node);
      if (style.display === "none" || style.visibility !== "visible" || Number(style.opacity) === 0) return null;
      if (style.clipPath !== "none" || style.perspective !== "none") throw new Error("uncertain clipped video geometry");
      if (node !== element && /(hidden|clip|scroll|auto)/.test(style.overflowX + " " + style.overflowY)) {
        const box = node.getBoundingClientRect();
        result = clipRect(result, {x:box.x+node.clientLeft,y:box.y+node.clientTop,
          width:node.clientWidth,height:node.clientHeight});
      }
    }
    return result;
  }
  function videoRect(video) {
    const box = video.getBoundingClientRect();
    const style = getComputedStyle(video);
    for (let node = video; node; node = parentElementOrHost(node)) {
      assertUntransformed(getComputedStyle(node));
    }
    if (!box.width || !box.height) return null;
    const horizontal = parseFloat(style.borderLeftWidth)+parseFloat(style.borderRightWidth)
      +parseFloat(style.paddingLeft)+parseFloat(style.paddingRight);
    const vertical = parseFloat(style.borderTopWidth)+parseFloat(style.borderBottomWidth)
      +parseFloat(style.paddingTop)+parseFloat(style.paddingBottom);
    const area = {x:box.x+parseFloat(style.borderLeftWidth)+parseFloat(style.paddingLeft),
      y:box.y+parseFloat(style.borderTopWidth)+parseFloat(style.paddingTop),
      width:box.width-horizontal,height:box.height-vertical};
    if (area.width <= 0 || area.height <= 0) return null;
    if (style.objectPosition !== "50% 50%") throw new Error("uncertain video object position");
    let width = area.width, height = area.height;
    if (["contain", "scale-down", "none"].includes(style.objectFit)) {
      if (!video.videoWidth || !video.videoHeight) throw new Error("video dimensions unavailable");
      const ratio = Math.min(area.width/video.videoWidth, area.height/video.videoHeight);
      const scale = style.objectFit === "none" ? 1 : style.objectFit === "scale-down" ? Math.min(1, ratio) : ratio;
      width = video.videoWidth*scale;
      height = video.videoHeight*scale;
    }
    const pixels = clipRect({x:area.x+(area.width-width)/2,y:area.y+(area.height-height)/2,width,height},area);
    return pixels && visibleRect(video,pixels);
  }
  globalThis.__mediaScreensaverSnapshot = () => {
    try {
      if (document.pictureInPictureElement) throw new Error("picture-in-picture geometry unavailable");
      if (visualViewport && (Math.abs(visualViewport.scale-1) > 0.01
          || visualViewport.offsetLeft || visualViewport.offsetTop)) throw new Error("viewport geometry unavailable");
      const videos = [];
      for (const video of findElements(document,"video")) {
        if (!isPlayingVideo(video)) continue;
        const rect = videoRect(video);
        if (rect) videos.push(rect);
      }
      return {healthy:true,videos,viewport:viewport(),metrics:{screenX,screenY,outerWidth,outerHeight,
        innerWidth,innerHeight,devicePixelRatio}};
    } catch (_) {
      return {healthy:false,videos:[],viewport:viewport()};
    }
  };
  let pending = null;
  chrome.runtime.onMessage.addListener((message, _sender, respond) => {
    if (message.kind === "media-map-configure") {
      pending = {scan:message.scan,tokens:new Map(message.children.map(child => [child.token,child.frameId]))};
      respond(true);
    } else if (message.kind === "media-map-emit") {
      window.parent.postMessage({kind:"media-frame-position",scan:message.scan,token:message.token},"*");
      respond(true);
    }
  });
  window.addEventListener("message", event => {
    const data = event.data;
    if (!event.isTrusted || !pending || !data || data.kind !== "media-frame-position"
        || data.scan !== pending.scan || !pending.tokens.has(data.token)) return;
    const frameId = pending.tokens.get(data.token);
    let frame;
    try {
      frame = findElements(document,"iframe,frame").find(node => node.contentWindow === event.source);
    } catch (_) {
      return;
    }
    if (!frame) return;
    let mapping;
    try {
      for (let node = frame; node; node = parentElementOrHost(node)) {
        assertUntransformed(getComputedStyle(node));
      }
      const box = frame.getBoundingClientRect();
      const style = getComputedStyle(frame);
      if ([style.paddingLeft,style.paddingRight,style.paddingTop,style.paddingBottom].some(n => parseFloat(n))) {
        throw new Error("padded frame");
      }
      const rect = {x:box.x+frame.clientLeft,y:box.y+frame.clientTop,
        width:frame.clientWidth,height:frame.clientHeight};
      mapping = {valid:true,rect,clip:visibleRect(frame,rect)};
    } catch (_) {
      mapping = {valid:false};
    }
    chrome.runtime.sendMessage({kind:"media-frame-mapping",scan:data.scan,frameId,mapping}).catch(() => {});
  });
}
