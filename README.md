# Assistente de Investimentos com RPA + n8n + IA

Fork de [digitalinnovationone/dio-lab-assistente-investimentos-rpa-n8n](https://github.com/digitalinnovationone/dio-lab-assistente-investimentos-rpa-n8n).

Projeto do desafio "Criando um Processo de RPA com N8N e Python" (Bootcamp Santander 2026, DIO).

## O que faz

1. Um script Python (Google Colab + BeautifulSoup) faz web scraping da página de clientes publicada no GitHub Pages.
2. O script envia a lista de clientes para um webhook do n8n (POST).
3. O n8n busca o CSV de investimentos, normaliza os dados e cruza perfil e saldo de cada cliente com os produtos compatíveis.
4. Uma LLM (OpenAI) escreve um e-mail curto e diferente para cada cliente, sem prometer ganhos.
5. Um If valida o e-mail: os válidos seguem para o Gmail; os inválidos vão para uma lista de revisão.
6. O Respond to Webhook devolve o status ao script.

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `rpa/rpa_extrair_clientes.py` | Script de RPA para o Colab |
| `rpa/` (notebook original) | Notebook original da DIO |
| `n8n/workflow.json` | Workflow exportado do n8n |
| `docs/index.html` e `docs/data.csv` | Página de clientes e CSV de investimentos (GitHub Pages) |
| `README.md` | Esta documentação |

## Fluxo no n8n

Webhook > Busca CSV investimentos (HTTP Request) > Normaliza CSV (Code) > Match e mensagem (Code) > OpenAI e-mail > Normaliza resposta LLM (Code) > E-mail válido? (If) > Gmail ou Lista inválidos > Respond to Webhook

## Como rodar

1. Importe `n8n/workflow.json` no n8n (Workflows > Import from file).
2. As URLs já apontam para a página e o CSV publicados pela DIO no GitHub Pages ([clientes](https://digitalinnovationone.github.io/dio-lab-assistente-investimentos-rpa-n8n/) e [data.csv](https://digitalinnovationone.github.io/dio-lab-assistente-investimentos-rpa-n8n/data.csv)). Se ativar o GitHub Pages neste fork, troque pelas URLs próprias.
3. No script, cole a URL do webhook do n8n em `N8N_WEBHOOK_URL`.
4. Configure as credenciais da OpenAI e do Gmail (use um e-mail só para automações).
5. Clique em executar o workflow e depois rode o script no Colab com a URL de teste. Para rodar direto, ative o workflow e use a URL de produção.

## Decisões técnicas

- **Webhook com Respond to Webhook:** o script recebe a confirmação do fim do processamento.
- **CSV lido como texto e normalizado em Code:** converte o mínimo em número e guarda a rentabilidade como texto (há valores como `IPCA+6.0%` e `Variável`), com um campo numérico separado só para ordenar.
- **Match por perfil e saldo mínimo, maior rentabilidade primeiro:** só sugere o que o cliente consegue investir; se nada couber, a mensagem orienta a falar com o assessor.
- **Dados limpos antes da IA:** o prompt recebe apenas nome, perfil, saldo e produto sugerido.
- **Prompt com restrição de conformidade:** não prometer ganhos nem garantir rentabilidade.
- **Saída da LLM em JSON (subject e body):** um Code garante os campos `to`, `subject` e `html` para o Gmail e tem fallback se o JSON vier quebrado.
- **Resiliência:** Retry on Fail no HTTP Request e na OpenAI; o Gmail continua em caso de erro para não travar a fila.
- **Validação de e-mail por regex:** evita tentativas de envio para endereços inválidos e separa esses casos para ação manual (telefone, WhatsApp).

## Evidências

Adicione aqui prints ou um vídeo curto da execução, clicando em cada node para mostrar a saída de cada etapa.
