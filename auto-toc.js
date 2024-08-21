let tocScript = document.createElement("script");
tocScript.src =
  "https://cdnjs.cloudflare.com/ajax/libs/tocbot/4.27.4/tocbot.min.js";
document.body.appendChild(tocScript);
let toc = document.createElement("div");
toc.classList.add("toc");
document.body.insertBefore(toc, document.body.firstChild);

document.addEventListener("DOMContentLoaded", () => {
  Array.from(document.querySelectorAll("h2")).forEach((el) => {
    el.id = el.innerHTML;
  });

  tocbot.init({
    tocSelector: ".toc",
    contentSelector: "body",
    headingSelector: "h2, h3",
  });
});
