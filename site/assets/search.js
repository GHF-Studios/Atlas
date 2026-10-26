(() => {
  const input = document.querySelector("#atlas-search");
  const results = document.querySelector("#atlas-search-results");
  if (!input || !results) return;

  const count = document.querySelector("#atlas-search-count");
  const tabs = Array.from(document.querySelectorAll('[role="tab"][data-kind]'));
  const base = document.querySelector('meta[name="atlas-base"]')?.content || "/";
  const params = new URLSearchParams(window.location.search);
  const validKinds = new Set(tabs.map((tab) => tab.dataset.kind));
  let activeKind = validKinds.has(params.get("kind")) ? params.get("kind") : "all";
  let records = [];

  input.value = params.get("q") || "";

  const render = () => {
    const query = input.value.trim().toLocaleLowerCase();
    const matches = records.filter((record) => {
      const kindMatches = activeKind === "all" || record.kind === activeKind;
      const textMatches = !query ||
        `${record.title} ${record.kind} ${record.claim_status} ${record.body}`
          .toLocaleLowerCase()
          .includes(query);
      return kindMatches && textMatches;
    });

    results.replaceChildren();
    count.textContent = `${matches.length} ${matches.length === 1 ? "record" : "records"}`;

    if (!matches.length) {
      const empty = document.createElement("p");
      empty.className = "empty-state";
      empty.textContent = "No records match this search. Try another type or a broader phrase.";
      results.append(empty);
    }

    for (const record of matches) {
      const row = document.createElement("article");
      row.className = "record-card search-result";
      const eyebrow = document.createElement("p");
      eyebrow.className = "eyebrow";
      eyebrow.textContent = `${record.kind.replace(/-/g, " ")} · ${record.claim_status.replace(/-/g, " ")}`;
      const heading = document.createElement("h2");
      const link = document.createElement("a");
      link.href = `${base}${record.url}`;
      link.textContent = record.title;
      heading.append(link);
      const summary = document.createElement("p");
      const configuredSummary = record.summary;
      summary.textContent = typeof configuredSummary === "string" && configuredSummary.trim()
        ? configuredSummary
        : record.body.split("\n\n", 1)[0].slice(0, 320);
      row.append(eyebrow, heading, summary);
      results.append(row);
    }

    const next = new URL(window.location.href);
    if (query) next.searchParams.set("q", input.value.trim());
    else next.searchParams.delete("q");
    if (activeKind !== "all") next.searchParams.set("kind", activeKind);
    else next.searchParams.delete("kind");
    window.history.replaceState({}, "", next);
  };

  const selectTab = (selected, moveFocus = false) => {
    activeKind = selected.dataset.kind;
    for (const tab of tabs) {
      const active = tab === selected;
      tab.setAttribute("aria-selected", String(active));
      tab.tabIndex = active ? 0 : -1;
    }
    results.setAttribute("aria-labelledby", selected.id);
    if (moveFocus) selected.focus();
    render();
  };

  for (const tab of tabs) {
    tab.addEventListener("click", () => selectTab(tab));
    tab.addEventListener("keydown", (event) => {
      const index = tabs.indexOf(tab);
      let nextIndex = index;
      if (event.key === "ArrowRight") nextIndex = (index + 1) % tabs.length;
      else if (event.key === "ArrowLeft") nextIndex = (index - 1 + tabs.length) % tabs.length;
      else if (event.key === "Home") nextIndex = 0;
      else if (event.key === "End") nextIndex = tabs.length - 1;
      else return;
      event.preventDefault();
      selectTab(tabs[nextIndex], true);
    });
  }

  input.addEventListener("input", render);

  fetch(`${base}atlas.json`)
    .then((response) => {
      if (!response.ok) throw new Error("Atlas search index is unavailable.");
      return response.json();
    })
    .then((data) => {
      records = data.records;
      const selectedTab = tabs.find((tab) => tab.dataset.kind === activeKind) || tabs[0];
      selectTab(selectedTab);
    })
    .catch(() => {
      count.textContent = "Search unavailable";
      results.textContent = "The record index could not be loaded. Use Connections to follow the authored record links.";
    });
})();
