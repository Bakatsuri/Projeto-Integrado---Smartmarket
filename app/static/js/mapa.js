
document.addEventListener("DOMContentLoaded", () => {
    const map = document.querySelector("#market-map");

    if (!map) return;

    const zones = map.querySelectorAll(".map-zone");
    const mode = map.dataset.mode;

    const title = document.querySelector("#map-info-title");
    const description = document.querySelector("#map-info-text");
    const mapDescription = document.querySelector("#map-description");
    const legend = document.querySelector("#map-legend");

    const normalize = value =>
        String(value ?? "")
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "")
            .trim()
            .toLowerCase();

    // Remove "Corredor" para comparar apenas o número.
    const normalizeCorridor = value =>
        normalize(value).replace(/^corredor\s*/, "").trim();

    // MODO PRODUTO
    if (mode === "produto") {
        const corredor = normalizeCorridor(map.dataset.targetCorredor);
        const nicho = normalize(map.dataset.targetNicho);
        const lado = normalize(map.dataset.targetLado);
        const parte = normalize(map.dataset.targetParte);

        let encontrou = false;

        zones.forEach(zone => {
            const nichos = (zone.dataset.nichos || "")
                .split(",")
                .map(normalize);

            const mesmoCorredor =
                normalizeCorridor(zone.dataset.corridor) === corredor;

            const mesmoNicho =
                !nicho || nichos.includes(nicho);

            const mesmoLado =
                normalize(zone.dataset.side) === lado;

            const mesmaParte =
                normalize(zone.dataset.part) === parte;

            const corresponde =
                mesmoCorredor &&
                mesmoNicho &&
                mesmoLado &&
                mesmaParte;

            if (corresponde) {
                zone.classList.add("highlighted");
                encontrou = true;
            } else {
                zone.classList.add("dimmed");
            }
        });

        if (title) {
            title.textContent = "Localização do produto";
        }

        if (description) {
            const informacoes = [
                `Setor: ${map.dataset.targetNicho || "Não informado"}`,
                `Corredor: ${map.dataset.targetCorredor || "Não informado"}`,
                `Lado: ${map.dataset.targetLado || "Não informado"}`,
                `Parte: ${map.dataset.targetParte || "Não informada"}`
            ];

            description.textContent = informacoes.join("\n");
        }

        if (mapDescription) {
            mapDescription.textContent = encontrou
                ? "A área destacada indica a localização do produto."
                : "Não foi possível localizar essa combinação no mapa.";
        }

        if (legend) {
            legend.style.display = "none";
        }

        return;
    }

    // MODO HOME
    zones.forEach(zone => {
        zone.addEventListener("click", () => {
            zones.forEach(item => {
                item.classList.remove("selected");
            });

            zone.classList.add("selected");

            const setor = zone.dataset.sector;
            const corredor = zone.dataset.corridor;
            const lado = zone.dataset.side;
            const parte = zone.dataset.part;

            if (title) {
                title.textContent = setor || "Setor";
            }

            if (description) {
                const informacoes = [
                    `Corredor: ${corredor || "Não informado"}`
                ];

                if (lado) {
                    informacoes.push(`Lado: ${lado}`);
                }

                if (parte) {
                    informacoes.push(`Parte: ${parte}`);
                }

                description.textContent = informacoes.join("\n");
            }

            if (mapDescription) {
                mapDescription.textContent =
                    "Área selecionada no mapa do mercado.";
            }
        });
    });
});
