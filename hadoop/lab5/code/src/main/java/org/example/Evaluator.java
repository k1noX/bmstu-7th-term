package org.example;

import org.apache.mahout.cf.taste.common.TasteException;
import org.apache.mahout.cf.taste.eval.RecommenderBuilder;
import org.apache.mahout.cf.taste.eval.RecommenderEvaluator;
import org.apache.mahout.cf.taste.impl.eval.AverageAbsoluteDifferenceRecommenderEvaluator;
import org.apache.mahout.cf.taste.model.DataModel;
import org.apache.mahout.common.RandomUtils;

public class Evaluator {
    public static void evaluate(RecommenderBuilder builder, DataModel model) throws TasteException {
        double sum = 0;
        for (int i = 0; i < 10; i++) {
            RandomUtils.useTestSeed();
            RecommenderEvaluator evaluator = new AverageAbsoluteDifferenceRecommenderEvaluator();
            double score = evaluator.evaluate(builder, null, model, 0.7, 1.0);
            sum += score;
        }
        double averageScore = sum / 10.f;
        System.out.println("Score: " + String.valueOf(averageScore));
    }
}
