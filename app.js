"use strict";

const menu = document.querySelector(".menu-toggle");
const navigation = document.querySelector("#navigation");
if (menu && navigation) {
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
}

const search = document.querySelector("#publication-search");
const year = document.querySelector("#publication-year");
const empty = document.querySelector(".no-results");
const status = document.querySelector("#result-status");
if (search && year && empty && status) {
  const publications = [...document.querySelectorAll(".publication")];
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
  filterPublications();
}
