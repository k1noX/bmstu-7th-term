package org.example;

import org.apache.mahout.clustering.canopy.Canopy;
import org.apache.mahout.clustering.canopy.CanopyClusterer;
import org.apache.mahout.common.distance.CosineDistanceMeasure;
import org.apache.mahout.common.distance.DistanceMeasure;
import org.apache.mahout.common.distance.EuclideanDistanceMeasure;
import org.apache.mahout.math.RandomAccessSparseVector;
import org.apache.mahout.math.Vector;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class Main {
    public static List<Vector> chooseRandomPoints(List<Vector> vectors, int k) {
        List<Vector> randomPoints = new ArrayList<Vector>();
        for (int i = 0; i < k; i++) {
            int randomN = (int) (Math.random() * (vectors.size() - 1));
            randomPoints.add(vectors.get(randomN));
        }
        return randomPoints;
    }

    public static double[][] readFile(String path) throws IOException {
        List<String> temp = new ArrayList<>();
        try (BufferedReader br = new BufferedReader(new FileReader(path))) {
            String s;
            while ((s = br.readLine()) != null) {

                temp.add(s);
            }
        }
        double[][] result = new double[temp.size()][2];
        for (int i = 0; i < temp.size(); i++) {
            int sep_idx = temp.get(i).indexOf(',');
            result[i][0] = Double.parseDouble(temp.get(i).substring(0, sep_idx));
            result[i][1] = Double.parseDouble(temp.get(i).substring(sep_idx + 1));
        }
        return result;
    }

    public static List<Vector> getPoints(double[][] raw) {
        List<Vector> points = new ArrayList<Vector>();
        for (int i = 0; i < raw.length; i++) {
            double[] fr = raw[i];
            Vector vec = new RandomAccessSparseVector(fr.length);
            vec.assign(fr);
            points.add(vec);
        }
        return points;
    }

    public static void solve(List<Vector> points, List<Vector> randomPoints, DistanceMeasure measure, String output) throws IOException {
        List<Canopy> canopies = CanopyClusterer.createCanopies(randomPoints, new EuclideanDistanceMeasure(), 3, 1.5);
        List<Vector> clusterCenters = new ArrayList<>();
        for (Canopy canopy : canopies) {
            clusterCenters.add(canopy.getCenter());
        }
        System.out.println(randomPoints);
        System.out.println(clusterCenters);
        FileWriter writer = new FileWriter(output, false);
        for (Vector vector : points) {
            double minDistance = measure.distance(vector, clusterCenters.get(0));
            int minCenterId = 0;
            for (int i = 1; i < clusterCenters.size(); i++) {
                if (minDistance > measure.distance(vector, clusterCenters.get(i))) {
                    minDistance = measure.distance(vector, clusterCenters.get(i));
                    minCenterId = i;
                }
            }
            writer.write(vector.get(0) + ", " + vector.get(1) + " : " + minCenterId + "\n");
        }
        writer.flush();
    }

    public static void main(String[] args) throws Exception {

        List<Vector> points = getPoints(readFile("/home/k1/Documents/studies/hadoop/lab6/points.txt"));
        List<Vector> randomPoints = chooseRandomPoints(points, 2);

        DistanceMeasure euclidianDistanceMeasure = new EuclideanDistanceMeasure();
        DistanceMeasure cosineDistanceMeasure = new CosineDistanceMeasure();

        solve(new ArrayList<Vector>(points), new ArrayList<Vector>(randomPoints), euclidianDistanceMeasure, "/home/k1/Documents/studies/hadoop/lab6/euclidean.txt");
        solve(new ArrayList<Vector>(points), new ArrayList<Vector>(randomPoints), cosineDistanceMeasure, "/home/k1/Documents/studies/hadoop/lab6/cosine.txt");
    }
}
