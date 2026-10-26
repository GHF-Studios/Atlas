(() => {
  const input = document.querySelector("#atlas-search");
  const results = document.querySelector("#atlas-search-results");
  const base = document.querySelector('meta[name="atlas-base"]')?.content || "/";
  if (!input || !results) return;

  fetch(\`${base}atlas.json\`)
    .then((response) => {
      if (!response.ok) throw new Error("Atlas search index is unavailable.");
      return response.json();
    })
    .then(({ records }) => {
      input.addEventListener("input", () => {
        const query = input.value.trim().toLocaleLowerCase();
        results.replaceChildren();
        if (!query) return;
        const matches = records.filter((record) =>
          \`${record.title} ${record.kind} ${record.claim_status} ${record.body}\`
            .toLocaleLowerCase()
            .includes(query),
        ).slice(0, 12);
        if (!matches.length) {
          const empty = document.createElement("p");
          empty.textContent = "No matching records.";
          results.append(empty);
          return;
        }
        for (const record of matches) {
          const row = document.createElement("div");
          row.className = "search-result";
          const link = document.createElement("a");
          link.href = \`${base}${record.url}\`;
          link.textContent = record.title;
          const type = document.createElement("small");
          type.textContent = \`${record.kind} · ${record.claim_status}\`;
          row.append(link, type);
          results.append(row);
        }
      });
    })
    .catch(() => {
      input.disabled = true;
      input.placeholder = "Search unavailable; browse the map instead.";
    });
})();

