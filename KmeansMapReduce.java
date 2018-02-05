import java.util.*;
import java.io.BufferedReader;
import java.io.DataInput;
import java.io.DataOutput;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.regex.Pattern;
import java.io.PrintWriter;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.Writable;
import org.apache.hadoop.io.WritableComparable;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.Reducer.Context;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;


public class  KmeansMapReduce{
	
	public static ArrayList<ArrayList<Double>> inputList = new ArrayList<ArrayList<Double>>();
	public static int numberOfClusters = 5;
	public static ArrayList<ArrayList<Double>> centroidList = new ArrayList<ArrayList<Double>>();
	public static int iterations = 0;
	public static HashMap<Integer, String> clusterMap = new HashMap<Integer, String>();
	
	public static class KmeansMapper extends Mapper<LongWritable, Text, IntWritable, Text> {
	
		@Override
		public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
			
			String line = value.toString();
			if(!line.equals("")){
				IntWritable clusterNumber = new IntWritable(-1);
				String[] geneExp =line.split("\\s+");
				double minDistance = Double.MAX_VALUE;
				
				for(int i=0; i< numberOfClusters; i++){
					double sum =0.0;
					for(int j=0; j<centroidList.get(0).size(); j++){
						sum += Math.pow((centroidList.get(i).get(j) - Double.parseDouble(geneExp[j+2])) , 2);
					}
					double distance = Math.sqrt(sum);
					if(distance < minDistance){
						minDistance = distance;
						clusterNumber = new IntWritable(i);
					}
				}
				Text geneId = new Text(geneExp[0]);

				int clno = clusterNumber.get();
				if(clusterMap.containsKey(clno)){
					String genevalue = clusterMap.get(clno);
					genevalue = genevalue.concat(";").concat(geneId.toString());
					clusterMap.put(clno, genevalue);
				}
				else{
					clusterMap.put(clno, geneId.toString());
				}
				
				context.write(clusterNumber, geneId);
			}
			
		}
	}
	
	
	public static class KmeansReducer extends Reducer<IntWritable,Text,IntWritable,Text> {
	 @Override
	 public void reduce(IntWritable key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
		
		java.util.Iterator<Text> valuesIterator = values.iterator();
		int arraySize = inputList.get(0).size()-2;
		double sumArray[] = new double[arraySize];
		
		int countOfPoints =0;	
		while(valuesIterator.hasNext()){
			countOfPoints++;
			Text point = valuesIterator.next();
			for(int i=2; i< inputList.get(Integer.parseInt(point.toString())-1).size(); i++){
				sumArray[i-2] += inputList.get(Integer.parseInt(point.toString())-1).get(i);
			}
		}
			
		String centroid = new String();
		String delimiter = ";";
		for(int i=0; i< arraySize; i++){
			double mean = sumArray[i]/countOfPoints;
			if(i<arraySize-1){				
				centroid = centroid.concat(String.valueOf(mean)).concat(delimiter);
			}else{
				centroid = centroid.concat(String.valueOf(mean));
			}
			
		}
		
		Text result= new Text(centroid);
		context.write(key,result);
	 }
 }
	
	
	
	
	public static void main(String[] args) throws Exception {
	
		FileReader fileReader = new FileReader("new_dataset_1.txt");
		BufferedReader bufferedReader = new BufferedReader(fileReader);
		//FileSystem fs = FileSystem.get(configuration);
		//Path path = new Path("/home/hadoop/cho.txt");
		//BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(fs.open(path)));
		
		
		String line = bufferedReader.readLine();
		while(line!=null){
			String[] words=line.split("\\s+");
			ArrayList<Double> currentRowList = new ArrayList<Double>();
			for(int i=0; i< words.length; i++ ){				
				currentRowList.add(Double.parseDouble(words[i]));
			}
			inputList.add(currentRowList);
			line = bufferedReader.readLine();
		}


		boolean hasConverged = false;

		String outputFile = "output20";
		while(hasConverged == false)// || iterations==10) VERRRYY VERRRYR IMPORTANT
		{

				System.out.println("iterations "+iterations);

				if(iterations==0){
					// Random random = new Random();
					// for(int i=0; i<numberOfClusters; i++){
					// 	int  n = random.nextInt(inputList.size());
					// 	System.out.println("random no. "+n);
					// 	ArrayList<Double> tempList = new ArrayList<Double>();
					// 	for(int j=2; j< inputList.get(n).size(); j++){
					// 		tempList.add(inputList.get(n).get(j));	
					// 	}
					// 	centroidList.add(tempList);
					// }
					
					ArrayList<Double> tempList = new ArrayList<Double>();
						for(int j=2; j< inputList.get(37).size(); j++){
							tempList.add(inputList.get(37).get(j));	
						}
						centroidList.add(tempList);
						
					tempList = new ArrayList<Double>();
						for(int j=2; j< inputList.get(23).size(); j++){
							tempList.add(inputList.get(23).get(j));	
						}
						centroidList.add(tempList);
					
					tempList = new ArrayList<Double>();
						for(int j=2; j< inputList.get(51).size(); j++){
							tempList.add(inputList.get(51).get(j));	
						}
						centroidList.add(tempList);
						
					tempList = new ArrayList<Double>();
						for(int j=2; j< inputList.get(55).size(); j++){
							tempList.add(inputList.get(55).get(j));	
						}
						centroidList.add(tempList);
					
					tempList = new ArrayList<Double>();
						for(int j=2; j< inputList.get(35).size(); j++){
							tempList.add(inputList.get(35).get(j));	
						}
						centroidList.add(tempList);
					 
				}
			
				Configuration configuration = new Configuration();
				Job job = Job.getInstance(configuration, "kmeans map reduce");
	
		    	job.setJarByClass(KmeansMapReduce.class);
		    	job.setMapperClass(KmeansMapper.class);
		    	job.setReducerClass(KmeansReducer.class);
		    	job.setOutputKeyClass(IntWritable.class);
		    	job.setOutputValueClass(Text.class);
				FileInputFormat.addInputPath(job, new Path(args[0]));
		    	FileOutputFormat.setOutputPath(job, new Path(args[1]+iterations));			    	
				job.waitForCompletion(true);				
				
				Runtime runtime = Runtime.getRuntime();
			    Process process2;
			    /*if(iterations!=0)
				{
					System.out.println("Inside If");
					process2 = runtime.exec("hadoop fs -rm -r /output101");
				}*/
				
				Process process = runtime.exec("hadoop fs -cat /"+outputFile+""+iterations+"/part-*");
				BufferedReader stdInput = new BufferedReader(new InputStreamReader(process.getInputStream()));
				BufferedReader stdError = new BufferedReader(new InputStreamReader(process.getErrorStream()));
				

				String line1 = new String();
				ArrayList<ArrayList<Double>> newCentroidList = new ArrayList<ArrayList<Double>>();
				while((line1 = stdInput.readLine()) != null){
					String[] words=line1.split("\\s+");
					String[] geneValues=words[1].split(";");
					ArrayList<Double> currentCentroidList = new ArrayList<Double>();
					for(int i=0; i< geneValues.length; i++ ){				
						currentCentroidList.add(Double.parseDouble(geneValues[i]));
					}
					newCentroidList.add(currentCentroidList);				
				}

				int i;
				loop :for(i=0; i<numberOfClusters; i++){
					for(int j=0; j<newCentroidList.get(0).size(); j++){
						if(!centroidList.get(i).get(j).equals(newCentroidList.get(i).get(j))){
							break loop;
						}	
					}
				}

				
				if(i==numberOfClusters){
					hasConverged = true;
					System.out.println();
					System.out.println("clusters are as follows:");
					System.out.println();
					for(int k=0; k< clusterMap.size(); k++){
						String values[] = clusterMap.get(k).split(";");
						System.out.println(Arrays.toString(values));
						System.out.println();
					}
				}

				if(hasConverged!=true)
				{
					centroidList.clear();
					for(i=0; i<numberOfClusters; i++){
						centroidList.add(newCentroidList.get(i));	
					}
				}
			
				iterations++;	    
     	}
	     	    
    }

}