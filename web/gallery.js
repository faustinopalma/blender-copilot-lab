const viewer = document.querySelector("#viewer");
const status = document.querySelector("#status");
const rotate = document.querySelector("#rotate");
const reducedMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;
let current = null;
let rotating = !reducedMotion;

function rotation() {
  viewer.autoRotate = rotating;
  rotate.textContent = rotating ? "Pause rotation" : "Resume rotation";
  rotate.setAttribute("aria-pressed", String(rotating));
}

function message(text, error = false) {
  status.textContent = text;
  status.classList.toggle("error", error);
}

function reset() {
  viewer.cameraOrbit = "35deg 55deg auto";
  viewer.cameraTarget = "auto auto auto";
  viewer.fieldOfView = "auto";
  viewer.resetTurntableRotation();
}

function select(subject) {
  if (current?.slug === subject.slug && viewer.loaded) {
    reset();
    message("Live 3D ready. Drag to explore every side.");
    return;
  }
  current = subject;
  message("Loading actual 3D geometry… the poster is a temporary preview.");
  document.querySelector("#title").textContent = subject.title;
  document.querySelector("#description").textContent = subject.brief;
  viewer.alt = `${subject.title}. Drag to orbit, scroll to zoom, right-drag to pan.`;
  viewer.poster = `../output/gallery/${subject.slug}.png`;
  reset();
  viewer.src = `../output/gallery/${subject.slug}.glb`;
  document.querySelector("#glb").href = viewer.src;
  document.querySelector("#blend").href = `../output/gallery/${subject.slug}.blend`;
  document.querySelector("#still").href = viewer.poster;
  document.querySelector("#meta").textContent =
    `${subject.objects} Blender objects · ${subject.exported_meshes} exported mesh objects · ` +
    `${(subject.glb_bytes / 1048576).toFixed(2)} MiB · GLB 2.0`;
  for (const button of document.querySelectorAll(".subject")) {
    button.setAttribute("aria-pressed", String(button.dataset.slug === subject.slug));
  }
  const url = new URL(location.href);
  url.searchParams.set("subject", subject.slug);
  history.replaceState(null, "", url);
}

rotate.addEventListener("click", () => { rotating = !rotating; rotation(); });
document.querySelector("#reset").addEventListener("click", reset);
viewer.addEventListener("load", () => {
  if (current && viewer.src.endsWith(`${current.slug}.glb`)) {
    message("Live 3D ready. Drag to explore every side.");
  }
});
viewer.addEventListener("error", () => message(
  "3D loading failed. Check WebGL support, the local server, and the GLB file. The poster is not an interactive model.", true));
try {
  let timer;
  try {
    await Promise.race([
      customElements.whenDefined("model-viewer"),
      new Promise((_, reject) => {
        timer = setTimeout(() => reject(new Error("Local 3D viewer did not initialize")), 15000);
      }),
    ]);
  } finally {
    clearTimeout(timer);
  }
  rotation();
  const response = await fetch("gallery.json");
  if (!response.ok) throw new Error(`Gallery data returned HTTP ${response.status}`);
  const subjects = await response.json();
  if (!Array.isArray(subjects) || subjects.length !== 10) throw new Error("Expected ten exported subjects");
  const container = document.querySelector("#subjects");
  for (const subject of subjects) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "subject";
    button.dataset.slug = subject.slug;
    const image = document.createElement("img");
    image.src = `../output/gallery/${subject.slug}-preview.png`;
    image.alt = "";
    image.loading = "lazy";
    const title = document.createElement("span");
    title.textContent = subject.title;
    button.append(image, title);
    button.addEventListener("click", () => select(subject));
    container.append(button);
  }
  const requested = new URLSearchParams(location.search).get("subject");
  select(subjects.find(subject => subject.slug === requested) || subjects[0]);
} catch (error) {
  message(`Gallery unavailable: ${error.message}. Serve the repository over HTTP, not file://.`, true);
}
