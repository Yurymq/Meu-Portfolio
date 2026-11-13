const form = document.querySelector("#analysis-form");
const button = document.querySelector("#submit-button");
const status = document.querySelector("#status");
const results = document.querySelector("#results");

const candidateItems = [
  {
    id: "demo-01",
    description: "Estojo azul com duas canetas encontrado perto da biblioteca.",
    category: "Material escolar",
  },
  {
    id: "demo-02",
    description: "Fone de ouvido preto deixado em uma sala de aula.",
    category: "Eletrônico",
  },
  {
    id: "demo-03",
    description: "Chaveiro com três chaves encontrado no pátio.",
    category: "Chave/Carteira",
  },
];

function createElement(tag, className, text) {
  const element = document.createElement(tag);
  if (className) element.className = className;
  if (text !== undefined) element.textContent = text;
  return element;
}

function renderMatches(matches) {
  const container = document.querySelector("#matches");
  container.replaceChildren();
  if (!matches.length) {
    container.append(createElement("p", "hint", "Nenhum registro de exemplo foi enviado para comparação."));
    return;
  }
  for (const match of matches) {
    const card = createElement("article", "match");
    const head = createElement("div", "match-head");
    head.append(
      createElement("span", "", match.category),
      createElement("span", "", `${match.score}/100`),
    );
    card.append(
      head,
      createElement("p", "", match.description),
      createElement("small", "", match.reason),
    );
    container.append(card);
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const description = document.querySelector("#description").value.trim();
  if (description.length < 12) {
    status.textContent = "Escreva uma descrição com pelo menos 12 caracteres.";
    return;
  }

  button.disabled = true;
  button.textContent = "Analisando...";
  status.textContent = "Consultando o modelo de IA e comparando os registros de exemplo.";
  results.hidden = true;

  try {
    const response = await fetch("/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ description, candidate_items: candidateItems }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Não foi possível analisar a descrição.");

    document.querySelector("#category").textContent = data.category;
    document.querySelector("#normalized").textContent = data.normalized_description;
    const keywords = document.querySelector("#keywords");
    keywords.replaceChildren();
    for (const keyword of data.keywords) keywords.append(createElement("span", "chip", keyword));
    renderMatches(data.matches || []);
    results.hidden = false;
    status.textContent = "Análise concluída. Revise as sugestões antes de tomar qualquer decisão.";
  } catch (error) {
    status.textContent = error.message;
  } finally {
    button.disabled = false;
    button.textContent = "Analisar descrição";
  }
});
