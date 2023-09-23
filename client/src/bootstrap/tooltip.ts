import { Directive } from "vue";
import { Tooltip } from "bootstrap";

export const vBsTooltip: Directive<
  HTMLElement & { tooltip?: Tooltip },
  string
> = {
  mounted: (el, binding) => {
    el.setAttribute("data-bs-toggle", "tooltip");
    el.setAttribute("title", binding.value);
    if (binding.modifiers.html) el.setAttribute("data-bs-html", "true");
    ["top", "bottom", "right", "left"].forEach((modifier) => {
      if (binding.modifiers[modifier])
        el.setAttribute("data-bs-placement", modifier);
    });
    el.tooltip = new Tooltip(el);
  },

  beforeUnmount: (el) => {
    el.addEventListener("hidden.bs.tooltip", () => {
      el.tooltip?.dispose();
    });
    el.tooltip?.hide();
  },
};
