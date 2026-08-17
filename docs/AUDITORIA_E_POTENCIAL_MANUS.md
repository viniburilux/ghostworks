# Leitura estratégica — ghostworks

**Data:** 17 de agosto de 2026  |  **Repositório:** [ghostworks](https://github.com/viniburilux/ghostworks)  |  **Autor:** Manus AI

> Este documento é uma auditoria de inventário e potencial. Ele não altera o código existente e não afirma que funcionalidades foram executadas ou validadas quando isso não aparece na evidência observada.

## Síntese executiva

Repositório público 'ghostworks' contém um projeto de pesquisa/protótipo para detecção e síntese de inteligência territorial baseada em embeddings de satélite (TTI). Inclui: README com arquitetura e casos de estudo, um serializer Python para transformar outputs do pipeline em JSON para agentes Gemma, um prompt de sistema para Gemma, um notebook demo (Colab) e várias imagens ilustrativas. Não há evidência de pipeline completo para gerar embeddings, nem de dados de saída serializados, testes automatizados, CI/CD ou artefatos de produção.

## Domínio e propósito aparente

Análise territorial por detecção de transformações em larga escala usando embeddings satelitais (AlphaEarth) e a métrica Territorial Transformation Index (TTI). Domínio: monitoramento ambiental, análise de risco territorial e apoio a políticas públicas; integração pretendida com agentes LLM (família Gemma) e infra Google (Earth Engine, Vertex AI).

## Indicadores do snapshot

| Indicador | Valor |
|---|---:|
| Arquivos contabilizados | 14 |
| Tamanho no snapshot | 33319689 bytes |
| Último commit observado | effc0fbfda5aa5018624e5ef4b9a95701482b171	2026-05-29T19:14:18+00:00	Reposition: Problem-solving narrative & consolidated case studies |
| Prioridade sugerida | alta |

## Evidências observadas

- README.md descreve a arquitetura (AlphaEarth → GhostWorks Pipeline → Serializer → Gemma agent) e lista componentes incluídos (ghostworks_serializer.py, ghostworks_gemma_prompt.py, ghostworks_intelligence_demo.ipynb).
- ghostworks_serializer.py está presente no repositório e contém várias funções de sumarização (_summarize_trajectory, _summarize_outliers, _summarize_clusters) e metadados REGION_METADATA para casos como 'aral_sea' e 'matopiba'.
- ghostworks_gemma_prompt.py contém o SYSTEM_PROMPT completo e instruções de uso (exemplo de chamada com transformers/pipe e formato esperado do bloco <territorial_data>).
- ghostworks_intelligence_demo.ipynb contém um notebook de demo que orienta montagem em Colab/Drive, instala pacotes (google-cloud-aiplatform, google-genai) e exemplifica o fluxo: carregar sessão → serializar → alimentar Gemma/Vertex.
- Imagens de casos (ex.: images/aralsea_case.png, images/matopiba_case.png) e figura de arquitetura (images/architecture.png) estão no repositório, totalizando grande parte do tamanho do repo (~31 MB).
- Metadados do repositório: criado 2026-04-17, último commit 2026-05-29 com mensagem de reposicionamento; repositório público (isPrivate=false), sem estrelas nem forks.
- LICENSE indicada no README (CC-BY 4.0).

## Ativos e capacidades

- Serializer estrutural (ghostworks_serializer.py) capaz de ler CSVs e sumarizar trajetórias STT, outliers, clusters e regiões similares em JSON contextual.
- Prompt de sistema (ghostworks_gemma_prompt.py) padronizado para agente Gemma com instruções rígidas de output e ancoragem em métricas TTI e benchmarks.
- Notebook demo orientando execução em Colab/Google Drive e integração com Vertex AI / Gemma-family (fluxo end-to-end proposto, ainda que parcialmente ilustrativo).
- Material visual e estudos de caso (imagens da Aral Sea, MATOPIBA, arquitetura) para comunicação e demonstração de resultados/insights.
- Metadados de região predefinidos (REGION_METADATA) para pelo menos dois casos de estudo com contexto descritivo.
- Documentação conceitual clara sobre TTI e referência bibliográfica (Zenodo) — apoio de base teórica/research.

## Maturidade observável

Protótipo de pesquisa / demonstração. Evidências suportam que existem componentes de serialização e templates de prompt prontos para uso, e um notebook que demonstra integração esperada. No entanto, não há código visível para geração de embeddings AlphaEarth ou pipeline de ingestão via Google Earth Engine; não há amostras de JSON de saída do pipeline, testes automatizados, arquivo de dependências (requirements.txt/pyproject) nem workflows CI/CD. Reprodutibilidade é parcial: o notebook indica passos (Colab, pip install) mas depende de credenciais e de funções/inputs que não estão fornecidos como sample. Em resumo: funcionalidade de 'orquestração/serialização + prompt' presente; processamento de dados e produção de resultados não comprovados no repositório.

## Potencial de aproveitamento

- Integração com o ecossistema LuxVerso/GhostWorks: o serializer e o prompt fornecem um padrão imediato para conectar outputs de pipelines (quando existirem) ao agente Gemma, acelerando geração de relatórios interpretáveis.
- Uso como template de pesquisa e ensino: lauda conceitual (TTI) + notebook demo permitem replicação acadêmica se fornecerem exemplos de entrada/saída adicionais.
- Produto mínimo viável (MVP) de inteligência territorial: com adição de scripts de ingestão (GEE), amostras de embeddings e CI, pode tornar-se um componente reutilizável para monitoramento ambiental via Vertex/Gemma.
- Padronização de saída JSON para agentes LLM: o serializer pode ser adotado como formato de troca entre módulos de detecção e módulos de interpretação por IA dentro do ecossistema.

## Riscos e lacunas

- Ausência de pipeline de geração de embeddings/TTI no repositório — nenhuma função visível que acesse Google Earth Engine ou AlphaEarth para produzir E(x,t). (evidência: não há arquivos .py com chamadas a gee/alphaearth, apenas referências no README e notebook).
- Falta de dados de exemplo ou JSON serializado de saída: dificulta validação do serializer e testes de ponta a ponta. (evidência: diretório não contém CSVs de sessão nem exemplos .json).
- Dependências e ambiente não formalizados: não há requirements.txt, pyproject.toml, Dockerfile ou instruções de instalação completas; notebook instala pacotes individualmente. Isso afeta reprodutibilidade. (evidência: listagem de arquivos e conteúdo do notebook).
- Ausência de testes automatizados e CI/CD: não há sinais de test suite, GitHub Actions ou similar para garantir qualidade contínua. (evidência: nenhum .github/workflows nem arquivos de teste no dossiê).
- Risco de dependência de serviços proprietários (AlphaEarth, Gemma, Vertex, Google Earth Engine) sem esclarecimento sobre acesso, custos ou licenciamento — requisito operacional e de governança. (evidência: README menciona esses serviços, sem instruções de credenciais/DRI).
- Governança de dados e proveniência fracas: não há metadados de proveniência de inputs, política de retenção, nem orientação para gestão de credenciais/keys (possível risco de vazamento se usuários seguirem o notebook sem boas práticas).
- Segurança/privacidade não tratadas: nenhum guia para manejo de chaves, tokens ou IAM; notebook pede montagem de Drive e instalação de pacotes, sem aviso de exposição de credenciais.
- Ausência de validação empírica e métricas operacionais: o README e prompts citam benchmarks (Brazil N=10k) mas não há artefatos que comprovem reprodutibilidade desses números no repo.

## Próximos passos recomendados

- Adicionar exemplos mínimos reproduzíveis: incluir um conjunto de dados de amostra (CSV ou JSON) com pequenas entradas de STT/TTI e um arquivo JSON de saída gerado pelo serializer, para permitir testes locais sem acesso a GEE/AlphaEarth.
- Publicar um arquivo de dependências e ambiente: criar requirements.txt ou pyproject.toml + instruções curtas para execução local e Colab; opcionalmente, fornecer um Dockerfile para ambiente reprodutível.
- Expor contratos e esquema JSON formal: documentar o schema de saída do serializer (tipos, campos obrigatórios/optionais) e prover exemplos (good/bad) para consumibilidade pelo agente Gemma e por outras ferramentas.
- Implementar testes unitários e integração: criar testes para funções chave do serializer (trajectória, outliers, clusters, similar_regions) e configurar CI (GitHub Actions) para rodar lint e testes em PRs.
- Adicionar scripts de integração com GEE/AlphaEarth (ou stubs claros): incluir um módulo opcional que demonstre como obter embeddings (ou, se não for possível por licenciamento, fornecer um stub/simulação e explicitar limitações legais).
- Documentar governança e segurança: adicionar seção SECURITY.md / CONTRIBUTING.md descrevendo como armazenar credenciais (usar variáveis de ambiente, Secret Manager), política de dados e avisos sobre uso de modelos proprietários e custos de nuvem.
- Incluir amostras de execução do agente Gemma: fornecer um exemplo de chamada completa (serialized_json + SYSTEM_PROMPT) com resposta esperada (exemplo fixo) para testar a integração sem acesso a Vertex/Gemma.
- Verificar/licenciar dependências proprietárias: checar permissões de redistribuição e uso de nomes/trechos de prompts referentes a AlphaEarth/Gemma; adicionar nota legal se necessário.
- Melhorar README com quickstart mínimo: passo a passo para executar demo local com os exemplos adicionados (1–2 comandos) e explicar gaps conhecidos (o que falta para produção).
- Criar um roadmap técnico (issues/milestones): priorizar implementação do pipeline de ingestão, testes, amostras de dados e hardening para produção; atribuir responsáveis e cronograma estimado.

## Método e limites

A leitura foi feita sobre um snapshot de profundidade 1 e sobre arquivos textuais selecionados por relevância estrutural, incluindo README, manifests e amostras de código. Dependências, notebooks, binários, dados grandes e integrações externas podem exigir uma rodada posterior de execução controlada. Nenhum código do repositório foi executado durante a auditoria.

**Fonte primária:** [ghostworks](https://github.com/viniburilux/ghostworks)
