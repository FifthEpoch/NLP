For this week's work:
* Reviewed current literatures in a specific area of NLP–Natural Language Inference (NLI)
* Read latest public opinions on the popularization of generative natural language models like ChatGPT
* Identified a research question that is worth pursuing for the next 3 weeks
* Tested the ClaimBuster and ChatGPT APIs and collected data for the proposed experiment

Below is an introduction of the research problem, and the approaches I plan on using in my experiment. 

## Introduction

Recently, Microsoft released an early version of an AI-integrated Bing search engine where a newer, not-yet released version of ChatGPT is used alongside another model developed by Microsoft called Prometheus, a model that has access to the Bing search index and select the data sources that gets processed by ChatGPT [1]. With the combined intelligence of the two models, search results are displayed in the traditional view of a list of links with corresponding descriptions and also a natural language summary with inline outgoing links where appropriate. As the waitlist to access the new Bing search engine grows, people with early access to the feature are voicing their concerns surrounding incorrect summary of information, and sometimes even making up information in the process. This uncertainty in the truthfulness of text output, though not a unique problem to Bing, is especially problematic due to the expectation from users that they are receiving information that is truthful to its web source. 

With the rise of misinformation and disinformation in the news, there has been an increased research focus on fact-checking systems using large language models with high performance. Verifying claims can be difficult as it involves locating textual proof and applying claim-evidence entailment for validation. Most recent work has been done to design and test machine learning models that score sentences as evidence in a document [2, 3]. However, much simpler sentence scoring techniques that do not involve any updates to the parameters in a LM have also been shown to have promising performance [4]. This type of approach has the potential of requiring less computations compared to approaches where entailment is computed using another GPT model, while remaining effective in determining a claim entails the evidence provided. 

In this work, we extend the fact-checking technique involving perplexity shown in [4] in the task of fact-checking in the search result summary scenario by introducing a model that locates the most likely evidence to support the claim in a source document. In a typical fact-checking system, a claim and an evidence pair is provided, and the system classifies the claim as entailing or non-entailing to the evidence provided. The evidence is usually a short statement that contains one to two sentences. In the case of aggregating search results in a natural language summary format, the evidence comes in the form of a document that might contain tens or hundreds of sentences. Given an evidence that contains many sentences, the perplexity-based classifier might have a more difficult time distinguishing claims that entail or do not entail the evidence. Therefore it might be useful to automate the process of locating potential sentence-sized evidence before applying the perplexity-based classifier. 

## Approach

The focus of the experiments is to understand if perplexity can be used to retrieve individual sentences from the evidence document that best supports a claim. 

### Dataset
A dataset of claims and corresponding evidence documents is needed in this experiment. A subset of the Wikipedia dataset (specifically, random samples from the “20220301.en” dataset processed by HuggingFace) to be our evidence documents. To obtain a corresponding set of generated claims, we used a prompt which instructs a GPT model to generate wikipedia-style descriptions of each wikipedia article title we have sampled for the evidence dataset. 

### Evidence Retrieval
To retrieve the evidence sentence(s) that best support a given claim, perplexity is calculated per sentence in the evidence document based on the word orders in the generated claim. The sentence(s) with the lowest perplexity score(s) can be selected as the best evidence for the claim.

### Evaluation
The effectiveness of perplexity in retrieving the best evidence sentences for a given claim can be evaluated by manually evaluating if the best evidence sentence(s) support the generated claim.

__A quick note__ There might be a more streamlined way to evaluate. I am searching in more literatures to find out how others are performing evaluations without relying solely on human evaluations. I will be reading [4] on a new dataset that provides gold sentences for selected subject matters in the next day of two to find out how they were able to determine which sentence actually supports a claim.

### Baselines
To compare the effectiveness of perplexity-based retrieval to other methods, additional baselines can be implemented. For example, we can compare the simple perplexity-based retrieval approach against a model that might require more computation but is a common approach, such as the linear regression model as described in [2].

### Analysis
The results of the experiment can be analyzed to understand the effectiveness of perplexity-based retrieval compared to the baselines. Additional analysis can also be done to identify the strengths and weaknesses of the approach and to provide insights for future work.

## References

>[1] O’Donnell, B.. ew Bing with ChatGPT brings the power of AI to Microsoft's signature search engine. Feb 8, 2023. USA Today.
> 
>(article: https://www.usatoday.com/story/tech/2023/02/08/bing-ai-waitlist-chat-gpt/11210865002/)

>[2] Yoneda, T. et el.. UCL Machine Reading Group: Four Factor Framework For Fact Finding (HexaF). (2018). Proceedings of the First Workshop on Fact Extraction and VERification (FEVER), pages 97–102. Brussels, Belgium.
> 
>(paper content: https://aclanthology.org/W18-5515.pdf)

>[3] Yang, F. et el.. Improving Evidence Retrieval with Claim-Evidence Entailment. (2021). Proceedings of Recent Advances in Natural Language Processing, pages 1553–1558. https://doi.org/10.26615/978-954-452-072-4_174.
> 
>(paper content: https://aclanthology.org/2021.ranlp-1.174.pdf)

>[4] Lee, N., Bang, Y., et al.. Towards Few-Shot Fact-Checking via Perplexity. (2021).
> 
>(paper content: https://arxiv.org/pdf/2103.09535.pdf)

>[5] Thorne, J. et al. FEVER: a large-scale dataset for Fact Extraction and VERification. (2018). Proceedings of NAACL-HLT 2018, pages 809–819. New Orleans, Louisiana.
> 
>(paper content: https://aclanthology.org/N18-1074.pdf)
