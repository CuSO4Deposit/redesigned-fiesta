/* Turn Goldmark footnotes ([^1]) into Tufte/Graphics-Press sidenotes.
 *
 * Goldmark renders a footnote as a <sup> reference in the body plus an entry
 * in a .footnotes list at the end of the page; CSS alone cannot move a specific
 * note next to its marker, so we do it here: for each reference, clone its
 * definition into a <span class="sidenote"> right after the marker, and drop
 * the endnotes block. Graphics Press styles/number/toggles the result.
 */
(function () {
  function run() {
    var refs = Array.prototype.slice.call(
      document.querySelectorAll("a.footnote-ref[href^='#fn:']"),
    );
    if (refs.length === 0) return;

    refs.forEach(function (ref, index) {
      var id = decodeURIComponent(ref.getAttribute("href").slice(1));
      var definition = document.getElementById(id);
      if (!definition) return;

      var clone = definition.cloneNode(true);
      Array.prototype.forEach.call(
        clone.querySelectorAll("a.footnote-backref"),
        function (backref) {
          backref.parentNode.removeChild(backref);
        },
      );

      var html = clone.innerHTML.trim();
      var wrapped = /^<p>([\s\S]*)<\/p>$/.exec(html);
      if (wrapped) html = wrapped[1];

      var n = index + 1;
      var marker = ref.closest("sup") || ref;

      var label = document.createElement("label");
      label.className = "sidenote-toggle sidenote-number";
      label.setAttribute("for", "sidenote-" + n);

      var toggle = document.createElement("input");
      toggle.type = "checkbox";
      toggle.id = "sidenote-" + n;
      toggle.className = "sidenote-toggle";
      toggle.setAttribute("aria-hidden", "true");

      var note = document.createElement("span");
      note.className = "sidenote";
      note.innerHTML = html;

      marker.parentNode.insertBefore(label, marker);
      marker.parentNode.insertBefore(toggle, marker);
      marker.parentNode.insertBefore(note, marker);
      marker.parentNode.removeChild(marker);
    });

    var endnotes = document.querySelector(".footnotes");
    if (endnotes) endnotes.parentNode.removeChild(endnotes);
  }

  if (document.readyState !== "loading") run();
  else document.addEventListener("DOMContentLoaded", run);
})();
