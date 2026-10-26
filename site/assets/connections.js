(() => {
  const recordFilter = document.querySelector("#connection-record");
  const typeFilter = document.querySelector("#connection-type");
  const directionFilter = document.querySelector("#connection-direction");
  const results = document.querySelector("#connection-results");
  if (!recordFilter || !typeFilter || !directionFilter || !results) return;

  const rows = Array.from(results.querySelectorAll("[data-source-id]"));
  const count = document.querySelector("#connection-count");
  const empty = document.querySelector("#connection-empty");
  const params = new URLSearchParams(window.location.search);
  const validRecord = new Set(Array.from(recordFilter.options, (option) => option.value));
  const validType = new Set(Array.from(typeFilter.options, (option) => option.value));
  const validDirection = new Set(["both", "outgoing", "incoming"]);

  recordFilter.value = validRecord.has(params.get("record")) ? params.get("record") : "";
  typeFilter.value = validType.has(params.get("type")) ? params.get("type") : "";
  directionFilter.value = validDirection.has(params.get("direction"))
    ? params.get("direction")
    : "both";

  const syncUrl = () => {
    const next = new URL(window.location.href);
    if (recordFilter.value) next.searchParams.set("record", recordFilter.value);
    else next.searchParams.delete("record");
    if (typeFilter.value) next.searchParams.set("type", typeFilter.value);
    else next.searchParams.delete("type");
    if (recordFilter.value && directionFilter.value !== "both") {
      next.searchParams.set("direction", directionFilter.value);
    } else {
      next.searchParams.delete("direction");
    }
    window.history.replaceState({}, "", next);
  };

  const render = () => {
    const focus = recordFilter.value;
    const type = typeFilter.value;
    const direction = focus ? directionFilter.value : "both";
    directionFilter.disabled = !focus;
    let visible = 0;

    for (const row of rows) {
      const outgoing = row.dataset.sourceId === focus;
      const incoming = row.dataset.targetId === focus;
      const directionMatches = !focus || direction === "both" ||
        (direction === "outgoing" && outgoing) || (direction === "incoming" && incoming);
      const matches = (!focus || outgoing || incoming) &&
        (!type || row.dataset.relationType === type) && directionMatches;
      row.hidden = !matches;
      if (matches) visible += 1;
    }

    const noun = visible === 1 ? "link" : "links";
    const focusLabel = recordFilter.selectedOptions[0]?.textContent;
    count.textContent = `${visible} ${noun}${focus ? ` around ${focusLabel}` : " across all records"}`;
    empty.hidden = visible !== 0;
    syncUrl();
  };

  for (const filter of [recordFilter, typeFilter, directionFilter]) {
    filter.addEventListener("change", render);
  }

  window.addEventListener("popstate", () => {
    const next = new URLSearchParams(window.location.search);
    recordFilter.value = validRecord.has(next.get("record")) ? next.get("record") : "";
    typeFilter.value = validType.has(next.get("type")) ? next.get("type") : "";
    directionFilter.value = validDirection.has(next.get("direction"))
      ? next.get("direction")
      : "both";
    render();
  });

  render();
})();
