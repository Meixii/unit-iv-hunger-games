/* EvoSim CMS Admin: Vanilla JS schema-driven content editor */
"use strict";

const $ = (id) => document.getElementById(id);

function el(tag, props = {}, ...children) {
  const node = document.createElement(tag);
  for (const [key, value] of Object.entries(props)) {
    if (value === undefined || value === null || value === false) continue;
    if (key === "class") node.className = value;
    else if (key === "text") node.textContent = value;
    else if (key.startsWith("on")) node.addEventListener(key.slice(2), value);
    else node.setAttribute(key, value === true ? "" : value);
  }
  for (const child of children) if (child) node.append(child);
  return node;
}

function getPath(obj, dotPath) {
  return dotPath.split(".").reduce((o, k) => (o == null ? undefined : o[k]), obj);
}

function setPath(obj, dotPath, value) {
  const keys = dotPath.split(".");
  let node = obj;
  for (let i = 0; i < keys.length - 1; i++) {
    if (node[keys[i]] == null) node[keys[i]] = /^\d+$/.test(keys[i + 1]) ? [] : {};
    node = node[keys[i]];
  }
  node[keys[keys.length - 1]] = value;
}

async function api(path, opts = {}) {
  const res = await fetch(path, {
    method: opts.method || "GET",
    headers: opts.body ? { "Content-Type": "application/json" } : undefined,
    body: opts.body ? JSON.stringify(opts.body) : undefined,
  });
  let json = null;
  try {
    json = await res.json();
  } catch {}
  if (!res.ok) {
    const err = new Error(json?.error || `Request failed (${res.status})`);
    err.status = res.status;
    err.details = json?.details;
    throw err;
  }
  return json;
}

let schema = null;
let currentKey = null;
let data = null;
let dirty = false;
let buildPollInterval = null;

function showToast(msg) {
  const t = $("toast");
  t.textContent = msg;
  t.hidden = false;
  setTimeout(() => { t.hidden = true; }, 3000);
}

function setDirty(isDirty) {
  dirty = isDirty;
  $("dirty-note").hidden = !dirty;
  $("save-btn").disabled = !dirty;
}

/* ------------------------------------------------------------- auth check */

async function init() {
  setupTheme();
  setupEvents();

  try {
    const session = await api("/api/session");
    if (session.signedIn) {
      showApp();
    } else {
      showLogin();
    }
  } catch {
    showLogin();
  }
}

function showLogin() {
  $("login-view").hidden = false;
  $("app-view").hidden = true;
}

async function showApp() {
  $("login-view").hidden = true;
  $("app-view").hidden = false;
  schema = await api("/api/schema");
  renderNav();
  const firstKey = Object.keys(schema)[0];
  if (firstKey) selectCollection(firstKey);
}

function setupEvents() {
  $("login-form").onsubmit = async (e) => {
    e.preventDefault();
    const password = $("login-password").value;
    try {
      await api("/api/login", { method: "POST", body: { password } });
      $("login-error").hidden = true;
      showApp();
    } catch (err) {
      $("login-error").textContent = err.message;
      $("login-error").hidden = false;
    }
  };

  $("logout-btn").onclick = async () => {
    await api("/api/logout", { method: "POST" });
    showLogin();
  };

  $("save-btn").onclick = saveCurrent;
  $("rebuild-btn").onclick = triggerRebuild;
  $("build-close").onclick = () => { $("build-panel").hidden = true; };
  $("error-dismiss").onclick = () => { $("error-panel").hidden = true; };

  $("nav-search").oninput = (e) => {
    const q = e.target.value.toLowerCase();
    document.querySelectorAll(".nav-item").forEach((item) => {
      item.hidden = !item.textContent.toLowerCase().includes(q);
    });
  };
}

function setupTheme() {
  $("cms-theme-toggle").onclick = () => {
    const next = document.documentElement.dataset.theme === "light" ? "dark" : "light";
    document.documentElement.dataset.theme = next;
    try { localStorage.setItem("cms-theme", next); } catch {}
  };
}

/* ---------------------------------------------------------------- nav */

function renderNav() {
  const nav = $("collection-nav");
  nav.innerHTML = "";
  for (const [key, def] of Object.entries(schema)) {
    const a = el("a", {
      class: `nav-item ${key === currentKey ? "active" : ""}`,
      href: `#${key}`,
      text: def.label,
      onclick: (e) => {
        e.preventDefault();
        selectCollection(key);
      },
    });
    nav.append(a);
  }
}

/* ------------------------------------------------------------- editor */

async function selectCollection(key) {
  if (dirty && !confirm("You have unsaved changes. Discard them?")) return;
  currentKey = key;
  renderNav();
  setDirty(false);
  $("error-panel").hidden = true;

  const def = schema[key];
  $("collection-title").textContent = def.label;
  $("collection-desc").textContent = def.description;

  const form = $("editor-form");
  form.innerHTML = "<p>Loading content...</p>";

  try {
    data = await api(`/api/content/${key}`);
    renderForm();
  } catch (err) {
    form.innerHTML = `<p class="error">Failed to load content: ${err.message}</p>`;
  }
}

function renderForm() {
  const form = $("editor-form");
  form.innerHTML = "";
  const def = schema[currentKey];

  if (!def.fields || def.fields.length === 0) {
    form.append(el("p", { text: "No editable fields defined for this section." }));
    return;
  }

  for (const field of def.fields) {
    form.append(renderField(field, data, ""));
  }
}

function renderField(field, contextData, prefix) {
  const fullPath = prefix ? `${prefix}.${field.name}` : field.name;
  const currentVal = getPath(contextData, field.name);

  const group = el("div", { class: "form-group" });
  group.append(el("label", { text: field.label }));
  if (field.description) {
    group.append(el("p", { class: "field-desc", text: field.description }));
  }

  if (field.type === "text" || field.type === "url") {
    const input = el("input", {
      type: field.type === "url" ? "url" : "text",
      value: currentVal || "",
      oninput: (e) => {
        setPath(contextData, field.name, e.target.value);
        setDirty(true);
      },
    });
    group.append(input);
  } else if (field.type === "number") {
    const input = el("input", {
      type: "number",
      value: currentVal !== undefined ? currentVal : "",
      oninput: (e) => {
        setPath(contextData, field.name, Number(e.target.value));
        setDirty(true);
      },
    });
    group.append(input);
  } else if (field.type === "textarea") {
    const area = el("textarea", {
      text: currentVal || "",
      oninput: (e) => {
        setPath(contextData, field.name, e.target.value);
        setDirty(true);
      },
    });
    group.append(area);
  } else if (field.type === "select") {
    const sel = el("select", {
      onchange: (e) => {
        setPath(contextData, field.name, e.target.value);
        setDirty(true);
      },
    });
    for (const opt of field.options) {
      sel.append(el("option", { value: opt.value, text: opt.label, selected: currentVal === opt.value }));
    }
    group.append(sel);
  } else if (field.type === "list") {
    group.append(renderList(field, currentVal || [], contextData));
  }

  return group;
}

function renderList(field, listItems, contextData) {
  const container = el("div", { class: "list-container" });
  const itemsWrap = el("div", { class: "list-items" });

  function refresh() {
    itemsWrap.innerHTML = "";
    listItems.forEach((item, index) => {
      const itemBox = el("div", { class: "list-item" });
      const header = el("div", { class: "list-item-header" });

      let title = `Item ${index + 1}`;
      if (field.itemLabel) {
        title = field.itemLabel.replace(/\{(\w+)\}/g, (_, k) => item[k] || "");
      }
      header.append(el("span", { class: "list-item-title", text: title }));

      const delBtn = el("button", {
        type: "button",
        class: "btn btn-ghost btn-mini",
        text: "Remove",
        onclick: () => {
          listItems.splice(index, 1);
          setPath(contextData, field.name, listItems);
          setDirty(true);
          refresh();
        },
      });
      header.append(delBtn);
      itemBox.append(header);

      if (field.itemFields) {
        for (const subField of field.itemFields) {
          itemBox.append(renderField(subField, item, ""));
        }
      }
      itemsWrap.append(itemBox);
    });
  }

  refresh();
  container.append(itemsWrap);

  const addBtn = el("button", {
    type: "button",
    class: "btn btn-ghost btn-mini",
    text: "+ Add Entry",
    onclick: () => {
      const newItem = JSON.parse(JSON.stringify(field.newItem || {}));
      listItems.push(newItem);
      setPath(contextData, field.name, listItems);
      setDirty(true);
      refresh();
    },
  });
  container.append(addBtn);

  return container;
}

/* ------------------------------------------------------------- actions */

async function saveCurrent() {
  $("error-panel").hidden = true;
  $("save-btn").disabled = true;

  try {
    await api(`/api/content/${currentKey}`, {
      method: "PUT",
      body: { value: data },
    });
    setDirty(false);
    showToast("Changes saved successfully!");
  } catch (err) {
    $("save-btn").disabled = false;
    $("error-panel").hidden = false;
    const list = $("error-list");
    list.innerHTML = "";
    if (err.details) {
      for (const d of err.details) list.append(el("p", { text: d }));
    } else {
      list.append(el("p", { text: err.message }));
    }
  }
}

async function triggerRebuild() {
  const panel = $("build-panel");
  const output = $("build-output");
  panel.hidden = false;
  output.textContent = "Starting site build...";

  try {
    await api("/api/rebuild", { method: "POST" });
    if (buildPollInterval) clearInterval(buildPollInterval);
    buildPollInterval = setInterval(pollBuildStatus, 1000);
  } catch (err) {
    output.textContent = `Build failed to trigger: ${err.message}`;
  }
}

async function pollBuildStatus() {
  try {
    const res = await api("/api/rebuild/status");
    $("build-output").textContent = res.tail || "Building...";
    if (!res.running) {
      clearInterval(buildPollInterval);
      buildPollInterval = null;
      if (res.lastCode === 0) {
        showToast("Site build completed successfully!");
      } else {
        showToast("Build exited with errors.");
      }
    }
  } catch {
    clearInterval(buildPollInterval);
    buildPollInterval = null;
  }
}

window.addEventListener("DOMContentLoaded", init);
