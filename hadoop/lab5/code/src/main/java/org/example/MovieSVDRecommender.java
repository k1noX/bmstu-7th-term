package org.example;

import org.apache.mahout.cf.taste.common.TasteException;
import org.apache.mahout.cf.taste.impl.recommender.svd.ALSWRFactorizer;
import org.apache.mahout.cf.taste.impl.recommender.svd.SVDRecommender;
import org.apache.mahout.cf.taste.model.DataModel;
import org.apache.mahout.cf.taste.recommender.RecommendedItem;

import java.util.List;

public class MovieSVDRecommender {

    public static SVDRecommender getFirstSvdRecommender(DataModel model) throws TasteException {
        return new SVDRecommender(model, new ALSWRFactorizer(model, 10, 0.05, 10));
    }

    public static SVDRecommender getSecondSvdRecommender(DataModel model) throws TasteException {
        return new SVDRecommender(model, new ALSWRFactorizer(model, 10, 0.1, 10));
    }

    public static void recommend(SVDRecommender recommender, long userId, int numRecommendations) {
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
