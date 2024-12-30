
# Análise MDS

## Descrição do Notebook

Este notebook ```notebook_1.ipynb``` apresenta a aplicação de técnicas de **Multidimensional Scaling (MDS)** e **clusterização hierárquica** para dois casos de uso distintos:

1. **Distâncias geográficas entre capitais brasileiras**: O objetivo é reduzir as distâncias geográficas para um espaço bidimensional, permitindo a visualização das capitais em um "mapa" estimado, seguido de análise de agrupamento.
2. **Distâncias filogenéticas entre espécies bacterianas**: Análise similar, mas aplicada a dados de distâncias filogenéticas para explorar relações entre espécies.

---

## Dados Utilizados

### 1. Distâncias entre Capitais Brasileiras (`df_capitais`)
Este conjunto de dados contém informações sobre as distâncias geográficas (e outras métricas) entre pares de capitais brasileiras.

**Formato**:
- `nome_municipio1`, `nome_municipio2`: Capitais sendo comparadas.
- `distanciaGeo`: Distância geográfica (em metros) entre os municípios.

### 2. Distâncias Filogenéticas (`df_phylo_distances`)
Este conjunto de dados contém as distâncias filogenéticas entre pares de espécies bacterianas.

**Formato**:
- `ID1`, `ID2`: Identificadores das espécies.
- `distance`: Distância filogenética entre os pares de espécies.

---

## Técnicas Utilizadas

### 1. **Multidimensional Scaling (MDS)**
- Técnica de redução de dimensionalidade que mapeia uma matriz de distâncias em um espaço de menor dimensão (neste caso, 2D), mantendo as relações de dissimilaridade entre os pontos o mais fiel possível.
- **Objetivo**: Visualizar relações complexas em um espaço mais intuitivo.

**Aplicação nos dados**:
- **Capitais Brasileiras**: O MDS transforma as distâncias geográficas em coordenadas bidimensionais que formam um "mapa" aproximado.
- **Filogenias**: O MDS transforma as distâncias filogenéticas em um espaço 2D para explorar agrupamentos visuais entre espécies.

### 2. **Clusterização Hierárquica**
- Técnica de agrupamento que constrói uma hierarquia de clusters com base em uma métrica de dissimilaridade.
- **Método utilizado**: Ward, que minimiza a variância total dentro dos clusters.
- **Visualização**: Dendrograma, que ajuda a entender as relações hierárquicas entre elementos.

**Aplicação nos dados**:
- **Capitais Brasileiras**: Agrupamento de capitais em clusters geograficamente semelhantes.
- **Filogenias**: Identificação de grupos taxonômicos baseados nas distâncias filogenéticas.

---

## Resultados e Visualizações

### 1. **Capitais Brasileiras**
- **Mapa 2D (MDS)**: Representação aproximada da posição das capitais, respeitando as distâncias geográficas.
- **Clusters**: Identificação de grupos regionais (ex.: capitais próximas formam clusters, como as do Nordeste ou Sudeste).
- **Dendrograma**: Hierarquia de agrupamentos que reflete proximidades geográficas.

### 2. **Filogenias**
- **Mapa 2D (MDS)**: Representação bidimensional que ajuda a identificar proximidades filogenéticas.
- **Clusters**: Grupos de espécies bacterianas filogeneticamente relacionadas.
- **Dendrograma**: Relações hierárquicas entre espécies, útil para inferências taxonômicas.

---

## Validade da Análise

### Dados Geográficos (Capitais)
A análise MDS e a clusterização são altamente válidas neste contexto, pois:
- As distâncias geográficas são mensuráveis e confiáveis.
- A redução para 2D é interpretável, com as coordenadas representando posições aproximadas no mapa.
- Os clusters identificam regiões geográficas coerentes.

### Dados Filogenéticos (Espécies)
A validade é boa, mas existem limitações:
- As distâncias filogenéticas são baseadas em modelos que podem não capturar perfeitamente as relações evolutivas.
- A redução para 2D pode perder nuances importantes em datasets de alta dimensionalidade.

---

## Conclusão

Este notebook demonstra como técnicas como MDS e clusterização podem ser aplicadas a diferentes tipos de dados para obter insights visuais e interpretativos. Apesar das limitações da redução de dimensionalidade, os resultados são úteis para explorar padrões e relações em dados geográficos e filogenéticos.

**Possíveis Melhorias**:
- Explorar técnicas alternativas de redução de dimensionalidade, como t-SNE ou UMAP, especialmente para dados filogenéticos.
- Aumentar a resolução dos clusters ajustando os parâmetros de corte na análise hierárquica.

