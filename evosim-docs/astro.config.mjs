import { defineConfig } from "astro/config";
import { readFileSync } from "node:fs";

// Canonical URL lives in content/site.json so the CMS owns it too.
const site = JSON.parse(readFileSync(new URL("./content/site.json", import.meta.url), "utf-8"));

export default defineConfig({
  site: site.seo?.canonicalUrl || "http://localhost:4321",
  server: {
    port: 4321,
    host: true,
  },
});
