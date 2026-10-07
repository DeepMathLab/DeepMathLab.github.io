"use strict";

const menu = document.querySelector(".menu-toggle");
const navigation = document.querySelector("#navigation");
function closeMenu() {
  menu.setAttribute("aria-expanded", "false");
  navigation.classList.remove("is-open");
}
menu.addEventListener("click", () => {
  const open = menu.getAttribute("aria-expanded") !== "true";
  menu.setAttribute("aria-expanded", String(open));
  navigation.classList.toggle("is-open", open);
});
navigation.querySelectorAll("a").forEach(link => link.addEventListener("click", closeMenu));
document.addEventListener("keydown", event => {
  if (event.key === "Escape" && menu.getAttribute("aria-expanded") === "true") {
    closeMenu();
    menu.focus();
  }
});

const search = document.querySelector("#publication-search");
const year = document.querySelector("#publication-year");
const publications = [...document.querySelectorAll(".publication")];
const empty = document.querySelector(".no-results");
const status = document.querySelector("#result-status");
function filterPublications() {
  const terms = search.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
  let count = 0;
  publications.forEach(item => {
    const matches = terms.every(term => item.dataset.search.includes(term)) &&
      (year.value === "all" || year.value === item.dataset.year);
    item.hidden = !matches;
    if (matches) count++;
  });
  empty.hidden = count > 0;
  status.textContent = document.documentElement.lang === "ko" ? `${count}편의 논문` : `${count} ${count === 1 ? "publication" : "publications"}`;
}
search.addEventListener("input", filterPublications);
year.addEventListener("change", filterPublications);

const sections = [...document.querySelectorAll("main section[id]")];
if ("IntersectionObserver" in window) {
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      navigation.querySelectorAll("a").forEach(link => {
        if (link.getAttribute("href") === `#${entry.target.id}`) link.setAttribute("aria-current", "location");
        else link.removeAttribute("aria-current");
      });
    });
  }, { rootMargin: "-20% 0px -55% 0px" });
  sections.forEach(section => observer.observe(section));
}
