# Bi-Clustering with Biological Context Information

Bi-Clustering Gene Expression Data with Biological Context Information

## Project Organization
--------

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    ├── data               <- The original data
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    ├── report             <- Generated analysis as LaTeX
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── src                <- Source code for use in this project.
        ├── __init__.py    <- Makes src a Python module
        │
        ├── data           <- Scripts to download or generate data
        │
        ├── features       <- Scripts to turn raw data into features for modeling
        │
        └── algorithms     <- Scripts to bicluster the data

--------


## Task

Clustering is currently the method of choice for analyzing gene expression data besides Differential Expression Analysis. In a clustering, expression profiles of genes are grouped together if they are similar, which can provide insights on (formerly unknown) gene functions by the assumption that genes that are similarly expressed are participating in the same molecular process. Genes are typically involved in multiple processes of a cell, which is not well reflected by a strict separation of genes into distinct clusters. Bi-clustering, or subspace clustering, addresses this problem by trying to find (overlapping) subspaces in the data. However, the identification of subspaces completely relies on analyzing the data set, while it is reasonable to include biological context into the analysis.

The task was to apply a bi-clustering algorithm to gene expression data and extend it to incorporate knowledge from external resources, e.g. pathway information. This way, the algorithm shall be able to better - and potentially faster - assess which genes fall into what group of clusters. [Source](https://hpi.de/plattner/teaching/winter-term-201718/trends-in-bioinformatics.html)

## Report
[Source](https://github.com/WGierke/bicluster_gene_expressions/blob/master/report/report.pdf)  

![tib_biclustering_gierke-1](https://user-images.githubusercontent.com/6676439/38811147-26e564a8-4189-11e8-8c9d-5f6201442aa7.jpg)
![tib_biclustering_gierke-2](https://user-images.githubusercontent.com/6676439/38811146-26cb6e04-4189-11e8-89b0-ec49d47aa785.jpg)
![tib_biclustering_gierke-3](https://user-images.githubusercontent.com/6676439/38811145-26b0f8bc-4189-11e8-9cfa-09608fa89412.jpg)
![tib_biclustering_gierke-4](https://user-images.githubusercontent.com/6676439/38811150-2717f5e4-4189-11e8-8c01-ab7f4f91fa01.jpg)
![tib_biclustering_gierke-5](https://user-images.githubusercontent.com/6676439/38811149-270047d2-4189-11e8-90c0-b49549651bb0.jpg)
![tib_biclustering_gierke-6](https://user-images.githubusercontent.com/6676439/38811151-27328904-4189-11e8-9a71-94056ba7902f.jpg)
