const fs = require("node:fs");
const path = require("node:path");
const crypto = require("node:crypto");

const root = path.resolve(__dirname, "..");
const source = path.join(root, "node_modules", "@google", "model-viewer");
const target = path.join(root, "web", "vendor");
fs.mkdirSync(target, { recursive: true });
const assets = [
  ["dist/model-viewer.min.js", "model-viewer.min.js"],
  ["LICENSE", "model-viewer-LICENSE.txt"],
];
const files = assets.map(([from, to]) => {
  const bytes = fs.readFileSync(path.join(source, from));
  fs.writeFileSync(path.join(target, to), bytes);
  return { file: to, bytes: bytes.length, sha256: crypto.createHash("sha256").update(bytes).digest("hex") };
});
fs.writeFileSync(path.join(target, "provenance.json"), JSON.stringify({
  package: "@google/model-viewer", version: "4.3.1",
  upstream: "https://github.com/google/model-viewer",
  license: "Apache-2.0", files,
}, null, 2) + "\n");
console.log("Prepared local viewer and license; no CDN is needed at runtime.");
