/* Recorded task-level successive halving. No model training or invented scores. */
(() => {
  "use strict";
  const data = window.COMPOSE_CL_TSH;
  const root = document.getElementById("tsh-explorer");
  if (!root || !data) return;

  const matrix = document.getElementById("tsh-matrix");
  const progress = document.getElementById("tsh-progress");
  const play = document.getElementById("tsh-play");
  const count = document.getElementById("tsh-count");
  const stageText = document.getElementById("tsh-stage");
  const taskOutput = document.getElementById("tsh-task");
  const status = document.getElementById("tsh-status");
  const datasetButtons = [...root.querySelectorAll("[data-tsh-dataset]")];
  const checkpoints = [...root.querySelectorAll("[data-tsh-task]")];
  const reducedMotion = matchMedia("(prefers-reduced-motion: reduce)");
  const boundaries = [0, 10, 20, 50, 100];
  const stageDuration = 5500;
  const duration = stageDuration * (boundaries.length - 1);
  const cells = [];
  let dataset = "symbol_qa";
  let task = 0;
  let elapsed = 0;
  let playing = !reducedMotion.matches;
  let visible = false;
  let frame = null;
  let previousTime = null;
  let renderedState = "";

  function element(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  const header = element("div", "tsh-row tsh-column-heads");
  header.setAttribute("role", "row");
  for (const text of ["Anchors", "Shared LoRA", "Merged LoRA"]) {
    const cell = element("div", "", text);
    cell.setAttribute("role", "columnheader");
    header.append(cell);
  }
  matrix.append(header);
  const anchorNames = [[1, "Weight", "weight-anchor"], [2, "Function", "function-anchor"], [4, "Data", "data-anchor"]];
  for (const mask of [0, 1, 2, 4, 3, 5, 6, 7]) {
    const row = element("div", "tsh-row");
    row.setAttribute("role", "row");
    const label = element("div", "tsh-anchor-label");
    label.setAttribute("role", "rowheader");
    if (!mask) label.textContent = "No anchors";
    const names = anchorNames.filter(([bit]) => mask & bit);
    names.forEach(([, name, className], index) => {
      if (index) label.append(element("i", "tsh-plus", "+"));
      label.append(element("span", className, name));
    });
    row.append(label);
    for (const merge of [false, true]) {
      const cell = element("div", "tsh-candidates");
      cell.setAttribute("role", "cell");
      cell.dataset.anchors = mask;
      cell.dataset.merge = merge;
      const dots = element("div", "tsh-dots");
      dots.setAttribute("aria-hidden", "true");
      const candidates = data.candidates.filter(candidate => candidate.anchors === mask && candidate.merge === merge);
      const items = candidates.map(candidate => {
        const dot = element("span", "tsh-dot");
        dot.dataset.candidate = candidate.id;
        dot.title = candidate.label;
        dots.append(dot);
        return {candidate, dot};
      });
      const number = element("span", "tsh-cell-count");
      number.setAttribute("aria-hidden", "true");
      const remaining = element("strong", "", candidates.length);
      number.append(remaining, document.createTextNode(` / ${candidates.length}`));
      cell.append(dots, number);
      row.append(cell);
      cells.push({cell, items, remaining, description: `${names.map(([, name]) => name).join(" + ") || "No anchors"}, ${merge ? "merged" : "shared"} LoRA`});
    }
    matrix.append(row);
  }

  function render() {
    const integerTask = Math.min(100, Math.floor(task));
    progress.value = integerTask;
    progress.style.setProperty("--progress", `${task}%`);
    taskOutput.value = integerTask;
    const stages = data.datasets[dataset].stages;
    const completed = stages.filter(stage => stage.task <= integerTask);
    const current = completed.at(-1);
    const survivors = new Set(current ? current.survivors : data.candidates.map(candidate => candidate.id));
    progress.setAttribute("aria-valuetext", `Task ${integerTask} of 100, ${survivors.size} candidates remain`);
    const state = `${dataset}:${current ? current.task : 0}`;
    if (state === renderedState) return;
    renderedState = state;
    count.textContent = survivors.size;
    stageText.textContent = integerTask >= 100 ? "10 finalists complete the full task sequence." : current ?
      `Top ${survivors.size} retained after task ${current.task}. Next: task ${stages[completed.length].task}.` : "All candidates start together.";
    for (const {cell, items, remaining, description} of cells) {
      const alive = items.filter(({candidate}) => survivors.has(candidate.id)).length;
      remaining.textContent = alive;
      cell.classList.toggle("is-empty", !alive);
      cell.setAttribute("aria-label", `${description}: ${alive} of ${items.length} candidates remain`);
      for (const {candidate, dot} of items) {
        const eliminated = !survivors.has(candidate.id);
        dot.classList.toggle("is-eliminated", eliminated);
        dot.title = `${candidate.label}: ${eliminated ? "eliminated" : "remaining"}`;
      }
    }
    for (const button of checkpoints) {
      button.setAttribute("aria-pressed", Number(button.dataset.tshTask) === (current ? current.task : 0));
    }
    status.textContent = `${data.datasets[dataset].label}. ${survivors.size} candidates remain. ${stageText.textContent}`;
  }

  function taskToTime(value) {
    if (value >= 100) return duration;
    const index = boundaries.findIndex((boundary, i) => i < 4 && value < boundaries[i + 1]);
    return (index + (value - boundaries[index]) / (boundaries[index + 1] - boundaries[index])) * stageDuration;
  }

  function tick(now) {
    frame = null;
    if (!playing || !visible || document.hidden) return;
    if (previousTime !== null) elapsed = Math.min(duration, elapsed + now - previousTime);
    previousTime = now;
    const index = Math.min(3, Math.floor(elapsed / stageDuration));
    const fraction = (elapsed - index * stageDuration) / stageDuration;
    task = boundaries[index] + fraction * (boundaries[index + 1] - boundaries[index]);
    render();
    if (elapsed >= duration) setPlaying(false);
    else frame = requestAnimationFrame(tick);
  }

  function schedule() {
    if (frame !== null) cancelAnimationFrame(frame);
    frame = null;
    previousTime = null;
    if (playing && visible && !document.hidden) frame = requestAnimationFrame(tick);
  }

  function setPlaying(value) {
    playing = value;
    root.classList.toggle("is-playing", value);
    play.querySelector("span").textContent = value ? "Pause" : "Play";
    play.setAttribute("aria-label", value ? "Pause pruning animation" : "Play pruning animation");
    schedule();
  }

  function seek(value) {
    task = Math.max(0, Math.min(100, value));
    elapsed = taskToTime(task);
    render();
  }

  progress.addEventListener("input", () => { setPlaying(false); seek(Number(progress.value)); });
  for (const button of checkpoints) button.addEventListener("click", () => {
    setPlaying(false);
    seek(Number(button.dataset.tshTask));
  });
  for (const button of datasetButtons) button.addEventListener("click", () => {
    dataset = button.dataset.tshDataset;
    for (const option of datasetButtons) option.setAttribute("aria-pressed", option === button);
    render();
  });
  play.addEventListener("click", () => {
    if (!playing && task >= 100) seek(0);
    setPlaying(!playing);
  });
  document.getElementById("tsh-restart").addEventListener("click", () => {
    seek(0);
    setPlaying(true);
  });
  document.addEventListener("visibilitychange", schedule);
  reducedMotion.addEventListener("change", event => { if (event.matches) setPlaying(false); });
  root.hidden = false;
  document.getElementById("tsh-fallback").hidden = true;
  render();
  setPlaying(playing);
  new IntersectionObserver(entries => {
    visible = entries[0].isIntersecting;
    schedule();
  }, {threshold: 0}).observe(root);
})();
