# Academic Methodology & Mathematical Formulations

## 1. Classical NLP Baseline Formulations
The conventional baseline computes the Term Frequency-Inverse Document Frequency (TF-IDF) representation of the Job Description ($d_j$) and Candidate Resume ($d_r$):

$$\text{TF-IDF}(t, d) = \text{TF}(t, d) \times \log\left(\frac{1 + N}{1 + \text{DF}(t)}\right) + 1$$

Cosine similarity between the resulting sparse vectors:

$$\text{Sim}_{\text{TF-IDF}}(d_j, d_r) = \frac{\mathbf{v}_{d_j} \cdot \mathbf{v}_{d_r}}{\|\mathbf{v}_{d_j}\| \|\mathbf{v}_{d_r}\|}$$

Lexical Keyword Overlap is calculated via Jaccard index over extracted skill sets:

$$J(S_j, S_r) = \frac{|S_j \cap S_r|}{|S_j \cup S_r|}$$

## 2. Transformer Semantic Embeddings
Dense sentence embeddings are produced using a Siamese bi-encoder network (Sentence-BERT architecture):

$$\mathbf{u} = \text{Encoder}(d_j), \quad \mathbf{v} = \text{Encoder}(d_r)$$

Contextual similarity is calculated via normalized dot product:

$$\text{Sim}_{\text{Semantic}}(d_j, d_r) = \frac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\| \|\mathbf{v}\|}$$

Multi-sectional semantic matching calculates weighted affinity across text partitions:

$$\text{Score}_{\text{Semantic}} = 0.35 \cdot \text{Sim}_{\text{overall}} + 0.35 \cdot \text{Sim}_{\text{skills}} + 0.20 \cdot \text{Sim}_{\text{exp}} + 0.10 \cdot \text{Sim}_{\text{proj}}$$

## 3. Grounded LLM Information Extraction
To prevent hallucination, the model operates under an evidence-grounding constraint:

$$\forall q \in Q_{\text{req}}, \quad \text{Status}(q) = \begin{cases} \text{"Found"}, & \text{if } \exists s \in D_{\text{resume}} \text{ s.t. } s \models q \\ \text{"Not found in resume"}, & \text{otherwise} \end{cases}$$

## 4. Multi-Criteria Composite Scoring
The overall candidate score $S_{\text{overall}}$ is calculated as:

$$S_{\text{overall}} = \sum_{i=1}^{6} w_i \cdot s_i$$

Where:
- $w_1 = 0.35$ (Required Skills Match)
- $w_2 = 0.15$ (Preferred Skills Match)
- $w_3 = 0.10$ (Education Level)
- $w_4 = 0.15$ (Work Experience Timeline)
- $w_5 = 0.10$ (Project Relevance)
- $w_6 = 0.15$ (Transformer Semantic Fit)

Subject to $\sum_{i=1}^6 w_i = 1.0$.

## 5. Information Retrieval Evaluation Metrics
- **Precision@K**:
  $$P@K = \frac{|\text{Top } K \text{ retrieved} \cap \text{Relevant}|}{K}$$

- **Discounted Cumulative Gain (DCG@K)**:
  $$\text{DCG}@K = \sum_{i=1}^K \frac{2^{\text{rel}_i} - 1}{\log_2(i + 1)}$$

- **Normalized Discounted Cumulative Gain (NDCG@K)**:
  $$\text{NDCG}@K = \frac{\text{DCG}@K}{\text{IDCG}@K}$$

- **Mean Reciprocal Rank (MRR)**:
  $$\text{MRR} = \frac{1}{|Q|} \sum_{i=1}^{|Q|} \frac{1}{\text{rank}_i}$$
