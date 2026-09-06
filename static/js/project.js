"use strict";

(() => {
  const explorer = document.getElementById("composition-explorer");
  if (explorer && typeof COMPOSE_CL_RESULTS !== "undefined") {
    const inputs = [...explorer.querySelectorAll('input[name="mechanism"]')];
    const names = {si: "SI", sd: "SD", replay: "replay", merge: "merged LoRA"};
    const datasets = [
      {id: "symbol", name: "Symbol-QA"},
      {id: "llm", name: "LLM-QA"},
      {id: "real", name: "Real-QA"}
    ];
    const update = (announce = true) => {
      const active = inputs.filter(input => input.checked).map(input => input.value);
      const key = active.join("_") || "vanilla";
      const result = COMPOSE_CL_RESULTS[key];
      let label = active.map(name => names[name]).join(" + ");
      if (active.length === 4) label = "All mechanisms combined";
      else if (!active.length) label = "Naive fine-tuning with shared LoRA";
      else if (!active.includes("merge")) label += " + shared LoRA";
      document.getElementById("selected-composition").textContent = label;
      const descriptions = datasets.map((dataset, index) => {
        const value = result.mean[index];
        const rank = 1 + Object.values(COMPOSE_CL_RESULTS).filter(other => other.mean[index] > value).length;
        document.getElementById(`${dataset.id}-value`).textContent = value.toFixed(1);
        document.getElementById(`${dataset.id}-std`).textContent = result.std[index].toFixed(1);
        document.getElementById(`${dataset.id}-rank`).textContent = `Rank ${rank} of 16`;
        document.getElementById(`${dataset.id}-bar`).style.width = `${value}%`;
        return `${dataset.name}: ${value.toFixed(1)} percent, rank ${rank} of 16`;
      });
      if (announce) document.getElementById("explorer-status").textContent = `${label}. ${descriptions.join(". ")}.`;
    };
    inputs.forEach(input => input.addEventListener("change", () => update()));
    document.getElementById("reset-composition").addEventListener("click", () => {
      inputs.forEach(input => { input.checked = true; });
      update();
    });
    update(false);
    explorer.hidden = false;
  }

  const copyButton = document.getElementById("copy-bibtex");
  const code = document.getElementById("bibtex-code");
  if (!copyButton || !code) return;
  copyButton.hidden = false;
  copyButton.addEventListener("click", async () => {
    const status = document.getElementById("copy-status");
    try {
      if (!navigator.clipboard || !window.isSecureContext) throw new Error("Clipboard unavailable");
      await navigator.clipboard.writeText(code.textContent.trim());
      copyButton.textContent = "Copied";
      status.textContent = "BibTeX copied to clipboard.";
    } catch (_error) {
      const selection = window.getSelection();
      const range = document.createRange();
      range.selectNodeContents(code);
      selection.removeAllRanges();
      selection.addRange(range);
      copyButton.textContent = "Copy BibTeX";
      status.textContent = "BibTeX selected. Press Ctrl+C or Command+C to copy.";
    }
  });
})();
