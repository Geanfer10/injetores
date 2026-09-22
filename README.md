# Controle de Troca de Filtros dos Injetores

Painel automatizado do board "Controle de Troca de Filtros dos Injetores" (Monday.com), publicado via GitHub Pages.

## Estrutura

```
index.html                          → painel (lê data.json)
data.json                           → gerado automaticamente pelo Actions (não crie manualmente)
scripts/fetch_monday.py             → busca os dados no Monday e gera data.json
.github/workflows/update-data.yml   → roda o script periodicamente e comita o resultado
```

## Passo a passo para configurar

1. **Criar o repositório** no GitHub (ex.: `Filtros`), público ou privado — tanto faz para o Pages funcionar, desde que o plano permita Pages em repositório privado.

2. **Subir os arquivos:**
   - `index.html` e `README.md` → pode arrastar e soltar normalmente.
   - `scripts/fetch_monday.py` → crie a pasta `scripts` pelo botão "Add file → Create new file" e cole o conteúdo, ou arraste (pastas sem ponto no nome funcionam com drag-and-drop).
   - `.github/workflows/update-data.yml` → **crie manualmente** pelo "Add file → Create new file", digitando o caminho completo `.github/workflows/update-data.yml` na caixa de nome do arquivo (o GitHub cria as pastas automaticamente). Pastas que começam com ponto não sobem por arrastar e soltar.

3. **Adicionar o secret do token do Monday:**
   - Settings → Secrets and variables → Actions → New repository secret
   - Nome: `MONDAY_API_TOKEN`
   - Valor: o mesmo token usado no painel de Geradores (ou gere um novo em Monday → Avatar → Administração → API)

4. **Ativar o GitHub Pages:**
   - Settings → Pages → Source: "Deploy from a branch" → branch `main`, pasta `/ (root)`

5. **Rodar o workflow pela primeira vez:**
   - Aba "Actions" → selecione "Atualizar dados do Monday" → "Run workflow"
   - Isso gera o `data.json` inicial. Sem rodar isso pelo menos uma vez, o painel mostra erro de carregamento.

6. **Acessar o painel** em `https://SEU-USUARIO.github.io/NOME-DO-REPOSITORIO/` (leva 1–2 minutos após ativar o Pages).

## Frequência de atualização

Por padrão o workflow roda automaticamente às 08h e 14h (horário de Brasília). Para mudar, edite a linha `cron` em `.github/workflows/update-data.yml`. Também dá para rodar manualmente a qualquer momento pela aba Actions.
