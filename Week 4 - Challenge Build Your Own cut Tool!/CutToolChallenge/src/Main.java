import java.awt.*;
import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;

// Press Shift twice to open the Search Everywhere dialog and type `show whitespaces`,
// then press Enter. You can now see whitespace characters in your code.
public class Main {
    public static void main(String[] args) {

        Integer headTailLength = 5;

        String columnArgument = "";
        String fileName = "";

        String delimeter = null;
        String delimeterArg = null;
        Integer fieldValue = null;

        Boolean tail = false;
        Boolean head = false;


        for (String arg : args) {
            System.out.println("arg: " + arg);
        }

//        Extract the args
        if (args.length < 1) {
            System.out.println("Error: Please enter a file");
        } else {
            for (String arg : args) {
                // Get the file
                if (arg.contains(".csv") || arg.contains(".tsv")){
                    fileName = arg;
                }

                // Check for field/column argument
                if (arg.contains("-f")){
                    columnArgument = arg.replace("-f","").trim();
                    if (!columnArgument.isEmpty()){
                        try {
                            fieldValue = Integer.parseInt(columnArgument);
                            System.out.println("Field Value: " + fieldValue + "\n");
                        } catch(NumberFormatException e){
                            System.out.println("Error: Please specify a valid integer for the column selection");
                            throw new NumberFormatException();
                        }
                    }
                }
                // Check for  delimeter argument
                if (arg.contains("-d")){
                    delimeterArg = arg.replace("-d", "").trim();
                    System.out.println("Specified Delimeter Agrument: " + delimeterArg);
                }
                System.out.println(arg.trim().contains("tail"));
                // Check to see if head and tail constraints are in effects
                if (arg.trim().contains("tail")) {
                    tail = true;
                    System.out.println(arg.trim().contains("tail"));
                }

                if (arg.trim().contains("head")) {
                    head = true;
                    System.out.println(arg.trim().contains("head"));
                }
            }
        }

        // Check to see what the delimeter will be
        if (delimeter == null) {
            if (fileName.endsWith(".csv")) {
                delimeter = ",";
            } else if (fileName.endsWith(".tsv")) {
                delimeter = "\t";
            } else {
                System.out.printf("Error: Invalid file type");
            }
        }

        System.out.println("Delimeter: " + delimeter);
        System.out.println("\nFile with Path: " + fileName);

        // Get the number of lines in the document (so that head and tail can be used)
        String line;
        long totalLinesInFile = 0;
        int tailIteratorStart = 0;


        try (BufferedReader br = new BufferedReader(new FileReader(fileName))) {
            totalLinesInFile = br.lines().count();
            System.out.println("Total lines in the CSV: " + totalLinesInFile);
        } catch (IOException e) {
            e.printStackTrace();
        }

        // Read the file with a buffered reader
        try (BufferedReader br = new BufferedReader(new FileReader(fileName.toString()))) {

            // Resolve if it is a head or a tail command
            if (tail) {
                tailIteratorStart = (int)totalLinesInFile - headTailLength;
//                System.out.println("Tail Iterator Start: " + tailIteratorStart);
            }
            if (head) {
                // Only count the first five lines
                totalLinesInFile = 5;
            }

//            while ((line = br.readLine()) != null) {
            Integer currentLine = 0;

            while ( currentLine < totalLinesInFile) {

                Boolean ValidFieldValue;

                // Check to see if the lines have to be skipped if only reading the last five values
                if (currentLine < tailIteratorStart){
                    currentLine++;
                    continue;
                } else {
                    line = br.readLine();
                    String[] values = line.split(delimeter);

                    // Check to see if the field value is valid
                    if (fieldValue != null) {
                        if (ValidFieldValue = (fieldValue > values.length)){
                            System.out.println("Error: Column doesn't exist in the file");
                            throw new IndexOutOfBoundsException();
                        }
                    }

//                    System.out.println(currentLine);
                    currentLine++;

                    // If no field value / column given, business as usual
                    if (fieldValue == null){

//                        System.out.printf("Row: ");
                        for (String value : values) {
                            System.out.printf("%s%s", value, delimeterArg != null ? delimeterArg : "\t");

//                            System.out.printf("%-10s" + "%s", value, delimeterArg);
//                            System.out.printf("%s" + "%s", value, delimeterArg);
                        }
                        System.out.println();
                    }

                    // If fieldValue is not none, and no exception was thrown, then it is valid:
                    else {
                        // Output the colum specified in the fieldValue
                        for (int i = 0 ; i < values.length; i ++ ){
                            if (i == fieldValue) {
                                System.out.println(values[i-1]);
                            }
                        }
                    }
                }
            }
        } catch (FileNotFoundException e) {
            System.out.printf("Error: The file at path %s was not found. Please check if the file exists.\n", fileName);

        } catch (IOException e) {
            System.out.printf("Error: An I/O error occurred while reading the file at path %s. Please try again.\n", fileName);
        }
    }


    //        'C:\Users\Dave\Documents\Coding\Week 4 - Java\CutToolChallenge\testdata\fourchords.csv'
//        'C:\Users\Dave\Documents\Coding\Week 4 - Java\CutToolChallenge\testdata\sample.tsv'

    //        Get the Current Directory and the file for the path for processing.
//    String currentDir = System.getProperty("user.dir");
//        Path projectRoot = Paths.get("").toAbsolutePath();
//        System.out.println("currnet dir: " + currentDir);

//        Path fileName = Paths.get(currentDir.toString(), "testdata", "fourchords.csv");
//        Path csvFile = Paths.get(projectRoot.toString(), "testdata", "fourchords.csv");

//        Debug with the IntelliJ run
//        Path pathFileName = Paths.get(currentDir.toString(), "testdata", "fourchords.csv");
//        Path pathFileName = Paths.get(currentDir.toString(), "testdata", "sample.tsv");
//        fileName = pathFileName.toString();
}