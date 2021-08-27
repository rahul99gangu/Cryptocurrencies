# Cryptocurrencies
Cryptocurrencies analysis with unsupervised machine learning

The focus of this project was to use unsupervised machine learning to examine cryptocurrency data. The following steps were taken:
* The data was first preprocessed by being cleaned, encoded, and scaled to more appropriately work with the algorithms.
* We then used Principle Component Analysis (PCA) to reduce the dimensions of the dataframe, for further analysis.
* The K-means algorithm was then used to create an elbow curve plot. This allowed us to find the best value for k, and thus the best number of clusters for the available data.

<img width="761" alt="Elbow Curve" src="https://user-images.githubusercontent.com/82982480/131166595-e02f8bbf-38d2-4170-a60a-a0f33fbc42e9.png">

* Lastly we visualized the data. First we created a 3D scatter plot using the PCA data. Then we transformed data for "Total Coin Supply" and "Total Coins Mined", which we then used to create a 2D scatter plot.
<img width="761" alt="3d scattered plot" src="https://user-images.githubusercontent.com/82982480/131166657-78403652-eef0-40fb-b4fa-1ce37eb1b7aa.png">

<img width="757" alt="2D Scattered Plot" src="https://user-images.githubusercontent.com/82982480/131166615-85c4b724-faf8-44f5-827f-4beef3698006.png">
