/* Geometry tests exercise the helpers imported by the actual content/worker scripts. */
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const browser = path.join(__dirname, "../scripts/media_screensaver/browser");
assert.ok(fs.existsSync(path.join(browser, "background.js")), "browser bridge is not implemented");
const worker = require(path.join(browser, "background.js"));
const content = require(path.join(browser, "content.js"));
const vm = require("node:vm");
const posted = [];
const parentWindow = {postMessage(message) {posted.push(message);}};
let contentMessage;
const isolated = {document:{},parent:parentWindow,addEventListener() {},
  chrome:{runtime:{onMessage:{addListener(listener) {contentMessage=listener;}}}}};
isolated.window = isolated;
vm.runInNewContext(fs.readFileSync(path.join(browser,"content.js"),"utf8"),isolated);
assert.equal(isolated.parent,parentWindow,"content initialization must preserve the browser's parent WindowProxy");
contentMessage({kind:"media-map-emit",scan:"scan-1",token:"token-1"},{},()=>{});
assert.equal(JSON.stringify(posted),JSON.stringify([{kind:"media-frame-position",scan:"scan-1",token:"token-1"}]),
  "a child frame must relay identifiers to its actual parent window");

// The privileged DOM boundary exposes closed roots; traversal must recurse into them.
const video = {tag:"video"};
const innerHost = {tag:"widget"};
const outerHost = {tag:"widget"};
const root = nodes => ({querySelectorAll(selector) {
  return nodes.filter(node => selector === "*" || selector.split(",").includes(node.tag));
}});
const roots = new Map([[outerHost,root([innerHost])],[innerHost,root([video])]]);
const dom = {openOrClosedShadowRoot(element) {return roots.get(element) || null;}};
assert.deepEqual(content.findElements(root([outerHost]),"video",dom),[video]);
assert.throws(() => content.findElements(root([outerHost]),"video",{}), /shadow/i,
  "unavailable privileged shadow inspection must fail closed");
assert.throws(() => content.assertUntransformed({transform:"none",zoom:"2"}), /geometry/i,
  "CSS zoom cannot reuse unscaled iframe offsets");
assert.throws(() => content.assertUntransformed({transform:"matrix(1,0,0,1,0,0)",zoom:"1"}), /geometry/i);
assert.doesNotThrow(() => content.assertUntransformed({transform:"none",zoom:"1"}));
assert.equal(content.isPlayingVideo({paused:false,ended:false,readyState:4,videoWidth:0,videoHeight:0}),false,
  "audio-only playback inside a video element must not suppress activation");
assert.equal(content.isPlayingVideo({paused:false,ended:false,readyState:4,videoWidth:640,videoHeight:360}),true);
assert.equal(content.isPlayingVideo({paused:true,ended:false,readyState:4,videoWidth:640,videoHeight:360}),false);

assert.deepEqual(content.clipRect({x:-20,y:10,width:100,height:100},
  {x:0,y:0,width:200,height:80}), {x:0,y:10,width:80,height:70});
assert.equal(content.clipRect({x:200,y:0,width:10,height:10},
  {x:0,y:0,width:200,height:80}), null, "touching edges are invisible");
assert.throws(() => content.clipRect({x:NaN,y:0,width:1,height:1},
  {x:0,y:0,width:200,height:80}), /geometry/i);

// A nested cross-origin frame video is clipped to each ancestor's viewport.
const child = content.mapFrameRects([{x:80,y:30,width:100,height:70}],
  {x:200,y:100,width:120,height:80}, {x:0,y:0,width:120,height:80});
assert.deepEqual(child, [{x:280,y:130,width:40,height:50}]);
assert.deepEqual(content.mapFrameRects(child,
  {x:20,y:10,width:300,height:160}, {x:0,y:0,width:300,height:160}),
  [{x:300,y:140,width:20,height:30}]);

const metrics = {screenX:2048,screenY:0,outerWidth:1200,outerHeight:900,
  innerWidth:1200,innerHeight:800,devicePixelRatio:1};
const window = {left:2048,top:0,width:1200,height:900,state:"normal"};
assert.deepEqual(worker.desktopRects(metrics, window, 1,
  [{x:20,y:30,width:640,height:360}]), [{x:2068,y:130,width:640,height:360}]);
const zoomed = {...metrics,innerWidth:960,innerHeight:640,devicePixelRatio:1.25};
assert.deepEqual(worker.desktopRects(zoomed, window, 1.25,
  [{x:16,y:24,width:512,height:288}]), [{x:2068,y:130,width:640,height:360}]);
assert.deepEqual(worker.desktopRects({...metrics,innerHeight:900},
  {...window,state:"fullscreen"},1,[{x:0,y:0,width:1200,height:900}]),
  [{x:2048,y:0,width:1200,height:900}]);
assert.deepEqual(worker.desktopRects({...metrics,devicePixelRatio:1.40625},window,1,
  [{x:20,y:30,width:640,height:360}]), [{x:2908.125,y:182.8125,width:900,height:506.25}],
  "uniform X11 browser UI scaling must convert DIP origins and video pixels to native coordinates");
assert.deepEqual(worker.desktopBounds({...metrics,devicePixelRatio:1.40625},window,1),
  {x:2880,y:0,width:1687.5,height:1265.625});
assert.throws(() => worker.desktopRects({...metrics,devicePixelRatio:0},window,1,[]), /scal|geometry/i);
assert.throws(() => worker.desktopRects({...metrics,screenX:500},window,1,[]), /geometry/i);

const frames = [{frameId:0,parentFrameId:-1},{frameId:4,parentFrameId:0},
  {frameId:8,parentFrameId:4}];
const snapshots = new Map([[0,{videos:[],viewport:{x:0,y:0,width:1000,height:1000}}],
  [4,{videos:[],viewport:{x:0,y:0,width:500,height:500}}],
  [8,{videos:[{x:5,y:6,width:20,height:30}],viewport:{x:0,y:0,width:100,height:100}}]]);
const mappings = new Map([[4,{parentFrameId:0,rect:{x:100,y:200,width:500,height:500}}],
  [8,{parentFrameId:4,rect:{x:10,y:20,width:100,height:100}}]]);
assert.deepEqual(worker.combineFrames(frames,snapshots,mappings),
  [{x:115,y:226,width:20,height:30}]);
assert.throws(() => worker.combineFrames(frames,new Map([[0,snapshots.get(0)]]),mappings),
  /frame/i, "a frame without an authoritative snapshot cannot be treated as empty");
assert.throws(() => worker.combineFrames(frames,snapshots,new Map()), /frame/i);
assert.throws(() => worker.combineFrames(frames,snapshots,new Map([
  [4,{parentFrameId:0,rect:{x:100,y:200,width:250,height:500}}],
  [8,mappings.get(8)]])), /frame/i, "a resized frame cannot use an older viewport snapshot");
console.log("✅ Browser geometry checks passed");
