package org.example;


import org.apache.mahout.cf.taste.common.TasteException;
import org.apache.mahout.cf.taste.impl.model.file.FileDataModel;
import org.apache.mahout.cf.taste.model.DataModel;

import java.io.IOException;
import java.net.URISyntaxException;

public class Main {
    public static DataModel getDataModel() throws URISyntaxException, IOException {
        String csvFilePath = "data/ratings.csv";
        var loader = new ResourceLoader();
        return new FileDataModel(loader.getFileFromResource(csvFilePath));
    }

    public static void main(String[] args) throws URISyntaxException, IOException, TasteException {
        DataModel model = getDataModel();

        System.out.println("== Euclidean Distance Item Based Recommender ==");

        MovieItemBasedRecommender.recommend(MovieItemBasedRecommender.getEuclideanDistanceRecommender(model),1, 10);
        Evaluator.evaluate(MovieItemBasedRecommender::getEuclideanDistanceRecommender, model);

        System.out.println("== Pearson Correlation Item Based Recommender ==");

        MovieItemBasedRecommender.recommend(MovieItemBasedRecommender.getPearsonCorrelationRecommender(model),1, 10);
        Evaluator.evaluate(MovieItemBasedRecommender::getEuclideanDistanceRecommender, model);

        System.out.println("== The First SVD Recommender ==");

        MovieSVDRecommender.recommend(MovieSVDRecommender.getFirstSvdRecommender(model),1, 10);
        Evaluator.evaluate(MovieSVDRecommender::getFirstSvdRecommender, model);

        System.out.println("== The Second SVD Recommender ==");

        MovieSVDRecommender.recommend(MovieSVDRecommender.getSecondSvdRecommender(model),1, 10);
        Evaluator.evaluate(MovieSVDRecommender::getSecondSvdRecommender, model);
    }
}
