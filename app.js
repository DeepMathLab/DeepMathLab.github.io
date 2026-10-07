"use strict";

const root = document.documentElement;
const themeToggle = document.querySelector(".theme-toggle");
const themeMeta = document.querySelector('meta[name="theme-color"]');
function applyTheme(theme, remember = false) {
  root.dataset.theme = theme;
  if (themeMeta) themeMeta.content = theme === "dark" ? "#11141B" : "#FFFFFF";
  if (themeToggle) {
    themeToggle.hidden = false;
    themeToggle.setAttribute("aria-label", theme === "dark" ? themeToggle.dataset.labelLight : themeToggle.dataset.labelDark);
    themeToggle.title = themeToggle.getAttribute("aria-label");
    themeToggle.removeAttribute("aria-pressed");
  }
  if (remember) {
    try { localStorage.setItem("deepmathlab-theme", theme); } catch (_) { /* Preference storage is optional. */ }
  }
}
applyTheme(root.dataset.theme === "dark" ? "dark" : "light");
themeToggle?.addEventListener("click", () => applyTheme(root.dataset.theme === "dark" ? "light" : "dark", true));

const menu = document.querySelector(".menu-toggle");
const navigation = document.querySelector("#navigation");
if (menu && navigation) {
  function closeMenu(returnFocus = false) {
    menu.setAttribute("aria-expanded", "false");
    navigation.classList.remove("is-open");
    if (returnFocus) menu.focus();
  }
  menu.addEventListener("click", () => {
    const open = menu.getAttribute("aria-expanded") !== "true";
    menu.setAttribute("aria-expanded", String(open));
    navigation.classList.toggle("is-open", open);
    if (open) navigation.querySelector("a")?.focus({ preventScroll: true });
  });
  navigation.querySelectorAll("a").forEach(link => link.addEventListener("click", () => closeMenu()));
  document.addEventListener("keydown", event => {
    if (event.key === "Escape" && menu.getAttribute("aria-expanded") === "true") closeMenu(true);
  });
  document.addEventListener("pointerdown", event => {
    if (menu.getAttribute("aria-expanded") === "true" && !menu.contains(event.target) && !navigation.contains(event.target)) closeMenu();
  });
  matchMedia("(min-width: 1001px)").addEventListener("change", event => {
    if (event.matches) closeMenu();
  });
  root.classList.add("navigation-ready");
}

const geometryStage = document.querySelector(".geometry-stage");
const geometryControls = document.querySelector(".geometry-controls");
if (geometryStage && geometryControls) {
  const buttons = [...geometryControls.querySelectorAll("[data-geometry-view]")];
  const status = document.querySelector(".geometry-status");
  function setGeometryView(button) {
    geometryStage.dataset.view = button.dataset.geometryView;
    buttons.forEach(item => item.setAttribute("aria-pressed", String(item === button)));
    if (status) status.textContent = button.dataset.description;
    const title = geometryStage.querySelector("title");
    const description = geometryStage.querySelector("desc");
    if (title) title.textContent = button.textContent;
    if (description) description.textContent = button.dataset.description;
  }
  geometryControls.hidden = false;
  buttons.forEach(button => button.addEventListener("click", () => setGeometryView(button)));
  setGeometryView(buttons[0]);

  const reducedMotion = matchMedia("(prefers-reduced-motion: reduce)");
  const finePointer = matchMedia("(hover: hover) and (pointer: fine)");
  let frame = 0;
  let pointer = null;
  function resetGeometryTilt() {
    if (frame) cancelAnimationFrame(frame);
    frame = 0;
    pointer = null;
    geometryStage.style.setProperty("--tilt-x", "0deg");
    geometryStage.style.setProperty("--tilt-y", "0deg");
  }
  geometryStage.addEventListener("pointermove", event => {
    if (reducedMotion.matches || !finePointer.matches || event.pointerType === "touch") return;
    pointer = { x: event.clientX, y: event.clientY };
    if (frame) return;
    frame = requestAnimationFrame(() => {
      frame = 0;
      if (!pointer || reducedMotion.matches || !finePointer.matches) return;
      const box = geometryStage.getBoundingClientRect();
      const x = Math.max(-1, Math.min(1, (pointer.x - box.left) / box.width * 2 - 1));
      const y = Math.max(-1, Math.min(1, (pointer.y - box.top) / box.height * 2 - 1));
      geometryStage.style.setProperty("--tilt-x", `${(-y * 4).toFixed(2)}deg`);
      geometryStage.style.setProperty("--tilt-y", `${(x * 4).toFixed(2)}deg`);
    });
  }, { passive: true });
  geometryStage.addEventListener("pointerleave", resetGeometryTilt);
  reducedMotion.addEventListener("change", resetGeometryTilt);
  finePointer.addEventListener("change", resetGeometryTilt);
}

const search = document.querySelector("#publication-search");
const year = document.querySelector("#publication-year");
const empty = document.querySelector(".no-results");
const resultStatus = document.querySelector("#result-status");
const resetFilters = document.querySelector(".search-clear");
const topicButtons = [...document.querySelectorAll("[data-topic-filter]")];
if (search && year && empty && resultStatus && resetFilters) {
  const publications = [...document.querySelectorAll("#publication-list .publication")];
  const allowedTopics = new Set(topicButtons.map(button => button.dataset.topicFilter));
  const allowedYears = new Set([...year.options].map(option => option.value));
  let topic = "all";
  document.querySelector(".publication-filters").hidden = false;
  document.querySelector(".publication-tools").hidden = false;
  resetFilters.hidden = false;

  function readFilterUrl() {
    const query = new URLSearchParams(location.search);
    search.value = query.get("q") || "";
    year.value = allowedYears.has(query.get("year")) ? query.get("year") : "all";
    topic = allowedTopics.has(query.get("topic")) ? query.get("topic") : "all";
  }
  function updateFilterUrl() {
    const url = new URL(location.href);
    ["q", "year", "topic"].forEach(key => url.searchParams.delete(key));
    if (search.value.trim()) url.searchParams.set("q", search.value.trim());
    if (year.value !== "all") url.searchParams.set("year", year.value);
    if (topic !== "all") url.searchParams.set("topic", topic);
    history.replaceState(null, "", url);
  }
  function filterPublications(writeUrl = true) {
    const terms = search.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
    let count = 0;
    publications.forEach(item => {
      const matches = terms.every(term => item.dataset.search.includes(term)) &&
        (year.value === "all" || year.value === item.dataset.year) &&
        (topic === "all" || topic === item.dataset.topic);
      item.hidden = !matches;
      if (matches) count++;
    });
    topicButtons.forEach(button => button.setAttribute("aria-pressed", String(button.dataset.topicFilter === topic)));
    empty.hidden = count > 0;
    resultStatus.textContent = `${count} ${count === 1 ? "publication" : "publications"}`;
    resetFilters.disabled = !search.value && year.value === "all" && topic === "all";
    if (writeUrl) updateFilterUrl();
  }
  search.addEventListener("input", () => filterPublications());
  year.addEventListener("change", () => filterPublications());
  topicButtons.forEach(button => button.addEventListener("click", () => {
    topic = button.dataset.topicFilter;
    filterPublications();
  }));
  resetFilters.addEventListener("click", () => {
    search.value = "";
    year.value = "all";
    topic = "all";
    filterPublications();
    search.focus();
  });
  window.addEventListener("popstate", () => { readFilterUrl(); filterPublications(); });
  readFilterUrl();
  filterPublications();
}

document.querySelectorAll(".copy-citation").forEach(button => {
  button.hidden = false;
  let feedbackTimer;
  button.addEventListener("click", async () => {
    const entry = button.closest(".bibtex-entry");
    const code = entry.querySelector("code");
    const status = entry.querySelector(".copy-status");
    clearTimeout(feedbackTimer);
    button.textContent = button.dataset.labelCopy;
    status.textContent = "";
    button.disabled = true;
    button.setAttribute("aria-busy", "true");
    try {
      if (!navigator.clipboard?.writeText) throw new Error("Clipboard unavailable");
      await navigator.clipboard.writeText(code.textContent);
      button.textContent = button.dataset.labelCopied;
      status.textContent = button.dataset.labelCopied;
      feedbackTimer = setTimeout(() => {
        button.textContent = button.dataset.labelCopy;
        status.textContent = "";
      }, 2500);
    } catch (_) {
      status.textContent = button.dataset.labelFailed;
      entry.querySelector("pre").focus();
      const range = document.createRange();
      range.selectNodeContents(code);
      const selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
    } finally {
      button.disabled = false;
      button.removeAttribute("aria-busy");
    }
  });
});
