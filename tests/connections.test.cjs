const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");

const filter = (values) => ({
  options: values.map((value) => ({value})),
  value: "",
  disabled: false,
  listeners: {},
  get selectedOptions() {
    return this.options.filter((option) => option.value === this.value);
  },
  addEventListener(event, listener) {
    this.listeners[event] = listener;
  },
});

const record = filter(["", "a", "b", "unlinked"]);
const type = filter(["", "parent", "clarifies"]);
const direction = filter(["both", "outgoing", "incoming"]);
const rows = [
  {dataset: {sourceId: "a", targetId: "b", relationType: "parent"}, hidden: false},
  {dataset: {sourceId: "b", targetId: "a", relationType: "clarifies"}, hidden: false},
  {dataset: {sourceId: "a", targetId: "b", relationType: "clarifies"}, hidden: false},
];
const results = {querySelectorAll: () => rows};
const count = {textContent: ""};
const empty = {hidden: true};
const elements = {
  "#connection-record": record,
  "#connection-type": type,
  "#connection-direction": direction,
  "#connection-results": results,
  "#connection-count": count,
  "#connection-empty": empty,
};
global.document = {querySelector: (selector) => elements[selector]};
global.window = {
  location: {
    search: "?record=a&direction=outgoing",
    href: "https://atlas.test/connections.html?record=a&direction=outgoing",
  },
  history: {replaceState(_state, _title, url) { this.url = String(url); }},
  addEventListener() {},
};

vm.runInThisContext(fs.readFileSync("site/assets/connections.js", "utf8"));
const visible = () => rows.map((row) => !row.hidden);

assert.deepEqual(visible(), [true, false, true], "deep links apply focused outgoing direction");
direction.value = "incoming";
direction.listeners.change();
assert.deepEqual(visible(), [false, true, false], "direction filter follows edges into the focused record");
type.value = "clarifies";
type.listeners.change();
assert.deepEqual(visible(), [false, true, false], "relation type narrows the focused neighborhood");
record.value = "unlinked";
record.listeners.change();
assert.deepEqual(visible(), [false, false, false], "unlinked records show no unrelated edges");
assert.equal(empty.hidden, false, "the empty state appears when a record has no links");
assert.equal(direction.disabled, false, "direction remains available for a focused record");

console.log("Connections focus and filters behave as expected.");
