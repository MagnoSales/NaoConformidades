# NaoConformidades
Dashbord com Streamlit

# Configuração de Requirements para o Projeto

Este projeto pode ser configurado de três formas diferentes no `requirements.txt`, dependendo do ambiente em que será executado e da necessidade de estabilidade ou flexibilidade.

---

## 1. Versão **Fixa** (para desenvolvimento local)
```txt
pandas==2.2.3
streamlit==1.44.1
plotly==5.24.1
numpy==1.26.4

✅ Quando usar:
Desenvolvimento local.
Precisa de reprodutibilidade (garantir que todos rodem com as mesmas versões).
Evita surpresas com mudanças de versão.

2. Versão Mínima (para máxima atualização)
pandas
streamlit
plotly
numpy

✅ Quando usar:
Deploy em ambientes gerenciados (ex.: Streamlit Cloud).
Quer sempre as versões mais recentes e compatíveis.
Aceita mudanças automáticas sem travar versões.

3. Versão Híbrida (recomendada para deploy)
streamlit==1.44.1
plotly==5.24.1
pandas
numpy

✅ Quando usar:
Deploy em ambientes gerenciados (ex.: Streamlit Cloud).
Quer sempre as versões mais recentes e compatíveis.
Aceita mudanças automáticas sem travar versões.


