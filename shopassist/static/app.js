const q = (s) => document.querySelector(s);
const sessionId = sessionStorage.getItem("shopassist_session_id") || crypto.randomUUID();
sessionStorage.setItem("shopassist_session_id", sessionId);
const on = (id) => {
  document.querySelectorAll(".node").forEach((n) => n.classList.remove("on"));
  if (id) q(id).classList.add("on");
};
const travel = (n, label, back) => {
  const d = q("#d" + n),
    t = q("#t" + n);
  d.className = "dot" + (back ? " back" : "");
  void d.offsetWidth;
  d.classList.add(back ? "ret" : "go");
  t.textContent = label;
  t.classList.add("show");
  setTimeout(() => t.classList.remove("show"), 2200);
};
const add = (role, text, note) => {
  const m = document.createElement("div");
  m.className = "msg " + role;
  m.textContent = text;
  if (note) {
    const s = document.createElement("small");
    s.textContent = note;
    m.appendChild(s);
  }
  q("#chat").appendChild(m);
  q("#chat").scrollTop = 1e9;
  return m;
};
q("#f").addEventListener("submit", async (e) => {
  e.preventDefault();
  const text = q("#box").value.trim();
  if (!text) return;
  q("#box").value = "";
  add("user", text);
  on("#n-browser");
  travel(1, "POST /chat", false);
  setTimeout(() => {
    on("#n-server");
    travel(2, "POST /v1/messages", false);
    setTimeout(() => on("#n-claude"), 900);
  }, 900);
  const r = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: sessionId, text }),
  });
  const data = await r.json();
  travel(2, "reply", true);
  setTimeout(() => {
    on("#n-server");
    travel(1, "JSON", true);
    setTimeout(() => {
      on("#n-browser");
      add("assistant", data.reply, "input tokens: " + data.input_tokens);
    }, 900);
  }, 900);
});
