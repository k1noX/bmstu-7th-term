package org.example;

import org.apache.mahout.cf.taste.common.TasteException;
import org.apache.mahout.cf.taste.impl.recommender.GenericItemBasedRecommender;
import org.apache.mahout.cf.taste.impl.similarity.EuclideanDistanceSimilarity;
import org.apache.mahout.cf.taste.impl.similarity.PearsonCorrelationSimilarity;
import org.apache.mahout.cf.taste.model.DataModel;
import org.apache.mahout.cf.taste.recommender.RecommendedItem;
import org.apache.mahout.cf.taste.similarity.ItemSimilarity;

import java.util.List;

public class MovieItemBasedRecommender {
    public static GenericItemBasedRecommender getPearsonCorrelationRecommender(DataModel model) throws TasteException {
        ItemSimilarity similarity = new PearsonCorrelationSimilarity(model);
        return new GenericItemBasedRecommender(model, similarity);
    }

    public static GenericItemBasedRecommender getEuclideanDistanceRecommender(DataModel model) throws TasteException {
        ItemSimilarity similarity = new EuclideanDistanceSimilarity(model);
        return new GenericItemBasedRecommender(model, similarity);
    }

    public static void recommend(GenericItemBasedRecommender recommender, long userId, int numRecommendations) {
        try {
            List<RecommendedItem> recommendations = recommender.recommend(userId, numRecommendations);

            System.out.println("Recommendations for user " + userId + ":");
            for (RecommendedItem recommendation : recommendations) {
                System.out.println("MovieId: " + recommendation.getItemID() + ", Score: " + recommendation.getValue());
            }
        } catch (TasteException e) {
            e.printStackTrace();
        }
    }
}
